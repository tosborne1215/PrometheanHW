#!/usr/bin/python2.7

from multiprocessing import Process, Queue, Pool


class FileSearchManager(object):

    def __init__(self):
        pass

    def find(self, pattern):
        pass

    def create_pool(self):
        pass

    def create_queue_from_dir(self):
        pass

    def get_results_from_worker(self):
        pass

    def check_file_exists(self, file_name):
        pass

    def compile_expression(self, expression):
        pass

    def get_results():
        pass


class FileSearchWorker(object):

    def __init__(self):
        pass

    def search_file(self, file_name):
        pass


class GraphIt(object):

    def __init__(self):
        pass

    def build_graph(self, data):
        pass


if __name__ == '__main__':
    subprocesses = list()
    filesQueue = Queue()
    results = dict()
