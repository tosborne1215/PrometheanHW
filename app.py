#!/usr/bin/python2.7

from multiprocessing import Process, Queue, Pool, Manager
import os
import re
import time


class FileSearchManager(object):

    def __init__(self, workers=4):
        self.results = dict()
        self.workers = workers
        self.pattern = None
        self.manager = Manager()
        self.manager_queue = self.manager.Queue()
        self.result_queue = self.manager.Queue()

    def find(self, pattern, dir):
        self.results = dict()
        self.pattern = self.compile_expression(pattern)
        self.create_queue_from_dir(dir)
        self.create_pool()

        while self.manager_queue.qsize() != 0:
            time.sleep(.1)

        return self.get_results()

    def create_pool(self):
        if self.pattern is None:
            raise ValueError("No pattern to look for. Call find first.")
        self.pool = Pool(self.workers)
        self.pool.apply_async(FileSearchWorker,
                              (self.manager_queue, self.pattern, self.result_queue,))

    def create_queue_from_dir(self, root_dir):
        if root_dir is None:
            raise ValueError("Input dir is None")
        # Its a dir
        if self.check_file_exists(root_dir) and self.check_is_dir(root_dir):
            for file in os.listdir(root_dir):
                self.create_queue_from_dir(os.path.join(root_dir, file))
        # Its a file
        elif self.check_file_exists(root_dir):
            self.manager_queue.put(root_dir)
        # It doesnt exist and that is ok
        else:
            pass

    def check_progress_worker(self):
        pass

    def check_is_dir(self, dir_name):
        return os.path.isdir(dir_name) if dir_name is not None else False

    def check_file_exists(self, file_name):
        return os.path.exists(file_name) if file_name is not None else False

    def compile_expression(self, expression):
        if expression is None:
            raise ValueError("Regex is None")
        try:
            return re.compile(expression)
        except re.error:
            raise ValueError("Regex does not compile")

    def get_results(self):
        while not self.result_queue.empty():
            result = self.result_queue.get()
            if result[0] in self.results.keys():
                self.results[result[0]] = self.results.get(
                    result[0]) + result[1]
            else:
                self.results[result[0]] = result[1]
        return self.results


class FileSearchWorker(Process):
    buffer = 1024 * 1024

    def __init__(self, queue, pattern, output_queue):

        while not queue.empty():
            item = queue.get()
            print(os.getpid(), "got")
            result = self.search_file(item, pattern)
            output_queue.put(result)

    def search_file(self, file_name, pattern):
        matches = 0
        with open(file_name) as f:
            while True:
                data = f.read(self.buffer)
                if not data:
                    break
                matches += len(re.findall(pattern, data))

        return (file_name, matches)


class GraphIt(object):

    def __init__(self):
        pass

    def build_graph(self, data):
        pass


if __name__ == '__main__':
    pass
