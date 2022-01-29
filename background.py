# This file is modified from https://www.reddit.com/r/learnpython/comments/83rvgv/comment/dvl0gdp/
import os
import sys
import logging
import subprocess
import time
import database
import actions
import datetime
import conditions
from threading import Thread
from queue import Queue
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PyQt5.QtCore import QDir, QFileInfo


file_queue = Queue()
pathnames = database.get_folders_list()

class QueueEventHandler(FileSystemEventHandler):
    '''Watches a specific folder and raises events on_created and on_deleted'''

    def on_created(self, event):
        '''
    Handles on_created event. Checks that created thing is a file (not a folder) and adds it to a file_queue
    :param event:
    :return:
    '''
        super(QueueEventHandler, self).on_created(event)
        if not event.is_directory:
            logging.info("New file: {}".format(event.src_path))
            file_queue.put_nowait(event.src_path)
            logging.info("Put {} into file queue".format(event.src_path))
            queue_mgr.process_file_queue()

    def on_deleted(self, event):
        '''
    Handles on_deleted event. Just notes to logger when a file is deleted.
    :param event:
    :return:
    '''
        super(QueueEventHandler, self).on_deleted(event)
        if not event.is_directory:
            logging.info("Deleted file: %s", event.src_path)


class QueueManager(object):
    '''Manager class for taking files off the file_queue and pushing them into wherever'''
    attn_str = "===[ {} ]==="

    def __init__(self, file_queue: Queue, logger: logging.Logger):
        self.thread = Thread(target=self._process_file_queue)
        self.file_queue = file_queue
        self.logger = logger or logging.getLogger(__name__)

    def process_file_queue(self):
        '''Method checks if there is already a thread running or alive processing the queue and if not, creates a new
        one '''
        if not self.thread or not self.thread.is_alive():
            self.thread = Thread(target=self._process_file_queue)
            self.logger.info(self.attn_str.format("START processing"))
            self.thread.start()

    def _process_file_queue(self):
        '''Main method run as a separate thread which pops files off the file_queue and pushes data into whereever'''
        while not file_queue.empty():
            try:
                # Get file off Queue
                file = file_queue.get()
                self.logger.info("Processing file {}".format(file))
                file_info = QFileInfo(file)
                directory_of_file = file_info.dir().path()
                # CHECK IF YOUR FILE IS PART OF THE FOLDERS WHICH FORG IS WORKING ON OR NOT.
                for ppaatthh in pathnames:
                    if str(ppaatthh) in str(directory_of_file):
                        list_of_rules = database.get_rules_list(ppaatthh)
                        for rule in list_of_rules:
                            conditions_of_rule = database.get_rules_info(rule)
                            if conditions_of_rule[1] == 'Size':
                                conditions_of_rule[3] = float(conditions_of_rule[3])
                                if conditions_of_rule[2] == 'is':
                                    size_of_file = conditions.human_size(os.path.getsize(file))
                                    if size_of_file == conditions_of_rule[3] == 0:
                                        conditions.run_task(conditions_of_rule[7], file)
                                    elif size_of_file == conditions_of_rule[3]:
                                        conditions.run_task(conditions_of_rule[7], file)
                                elif conditions_of_rule[2] == 'greater than':
                                    size_of_file = conditions.human_size(os.path.getsize(file))
                                    if size_of_file > conditions_of_rule[3]:
                                        conditions.run_task(conditions_of_rule[7], file)
                                elif conditions_of_rule[2] == 'less than':
                                    size_of_file = conditions.human_size(os.path.getsize(file))
                                    if size_of_file < conditions_of_rule[3]:
                                        conditions.run_task(conditions_of_rule[7], file)
                            elif conditions_of_rule[1] == 'Extension':
                                if conditions_of_rule[2] == 'is':
                                    if file.endswith(conditions_of_rule[4]):
                                        conditions.run_task(conditions_of_rule[7], file)
                                elif conditions_of_rule[2] == 'is not':
                                    if file.endswith(conditions_of_rule[4]):
                                        pass
                                    else:
                                        conditions.run_task(conditions_of_rule[7], file)
                            elif conditions_of_rule[1] == 'Date Added':
                                dt = datetime.datetime.strptime(conditions_of_rule[5], '%Y-%m-%d')
                                new_dt = int(dt.strftime('%Y%m%d'))
                                file_date = int(
                                    datetime.datetime.fromtimestamp(os.path.getctime(file)).strftime('%Y%m%d'))
                                if conditions_of_rule[2] == 'is':
                                    if new_dt == file_date:
                                        conditions.run_task(conditions_of_rule[7], file)
                                if conditions_of_rule[2] == 'is before':
                                    if new_dt > file_date:
                                        conditions.run_task(conditions_of_rule[7], file)
                                if conditions_of_rule[2] == 'is after':
                                    if new_dt < file_date:
                                        conditions.run_task(conditions_of_rule[7], file)

                #### INSERT CODE HERE TO DO WORK ####

            except Exception as e:

                # If exception, log and do whatever
                self.logger.error(str(e))

                #### ANY CODE YOU WANT HERE IN CASE OF EXCEPTION ####

        self.logger.info(self.attn_str.format("END of file queue"))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    queue_mgr = QueueManager(file_queue, logging.getLogger())
    event_handler = QueueEventHandler()
    observer = Observer()
    for pathname in set(pathnames):
        observer.schedule(event_handler, pathname, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
