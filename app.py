#!/usr/bin/python2.7

from multiprocessing import Pool, Manager
import os
import re
import sys
import time
import matplotlib.pyplot as plt
import numpy as np

# Utilizes 2 managed queues. One for input one for results
# It will create a cool of workers when find is called.
# This class could alternatively inherit from Manager


class FileSearchManager(object):

    def __init__(self, workers=4):
        self.results = dict()
        self.workers = workers
        self.pattern = None
        self.manager = Manager()
        self.manager_queue = self.manager.Queue()
        self.result_queue = self.manager.Queue()

    # This is the function call that starts it all.
    # It compiles the expression, creates the queue, creates the pool
    # and then waits until the queue is empty.
    # Lastly it will return the results.
    def find(self, pattern, dir):
        self.results = dict()
        self.pattern = self.compile_expression(pattern)
        self.create_queue_from_dir(dir)
        self.create_pool()

        # Rest while the queue is emptied.
        while self.manager_queue.qsize() != 0:
            time.sleep(.1)

        return self.get_results()

    # Creates a process pool and creates a FileSearchWorker for each process
    def create_pool(self):
        if self.pattern is None:
            raise ValueError("No pattern to look for. Call find first.")

        self.pool = Pool(self.workers)
        # This will create a task for each worker
        [self.pool.apply_async(FileSearchWorker,
                               (self.manager_queue, self.pattern, self.result_queue,)) for i in range(self.workers)]

    # Creates a managed queue from the directory and will stop recursing
    # When we approach the depth limit
    def create_queue_from_dir(self, root_dir):

        try:
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
        except RuntimeError:
            print("Runtime error was thrown, but if we have data continue on.")

    # Check if the file is a dir
    def check_is_dir(self, dir_name):
        return os.path.isdir(dir_name) if dir_name is not None else False

    # Check if the file exists
    def check_file_exists(self, file_name):
        return os.path.exists(file_name) if file_name is not None else False

    # Compiles the regex and does some error checking
    def compile_expression(self, expression):
        if expression is None:
            raise ValueError("Regex is None")
        try:
            return re.compile(expression)
        except re.error:
            raise ValueError("Regex does not compile")

    # Empties the result Queue and formats into a dict
    def get_results(self):
        while not self.result_queue.empty():
            result = self.result_queue.get()
            if result[0] in self.results.keys():
                self.results[result[0]] = self.results.get(
                    result[0]) + result[1]
            else:
                self.results[result[0]] = result[1]
        return self.results


# This object could be static or alternatively inherit from Process
# Since I chose to use a process pool inheritting was unnecessary.
class FileSearchWorker(object):
    buffer = 1024 * 1024

    def __init__(self, queue, pattern, output_queue):

        while not queue.empty():
            item = queue.get()
            # Leaving this here because it is useful to see
            # that all workers are processing
            print(os.getpid(), "PID")
            result = self.search_file(item, pattern)
            output_queue.put(result)

    # Takes a file and runs the expression against it.
    # It returns a tuple containing the file_name and matches
    def search_file(self, file_name, pattern):
        if not os.path.exists(file_name):
            raise ValueError("file_name does not exist")
        matches = 0
        with open(file_name) as f:
            while True:
                data = f.read(self.buffer)
                if not data:
                    break
                matches += len(re.findall(pattern, data))

        return (file_name, matches)


# Basically a matplotlib wrapper
class GraphIt(object):

    def __init__(self, file_name="graph"):
        self.file_name = file_name

    def format_data(self, data):
        vals = list()
        labels = list()
        for label in data.keys():
            vals.append(data.get(label))
            # get the last element which is the fname. Otherwise
            # the chart will look horrible
            labels.append(label.split(os.pathsep)[-1])
        return (labels, vals)

    def output_graph(self, labels, data):

        y_pos = np.arange(len(labels))
        plt.bar(y_pos, data, align='center', alpha=0.5)
        plt.xticks(y_pos, labels)
        plt.ylabel('Mathces')
        plt.title('File Name')

        plt.show()


if __name__ == '__main__':
    if len(sys.argv) == 3:
        file = None
        pattern = None

        if os.path.exists(sys.argv[1]):
            file = sys.argv[1]
            pattern = sys.argv[2]
        elif os.path.exists(sys.argv[2]):
            file = sys.argv[2]
            pattern = sys.argv[1]
        else:
            raise ValueError(
                "The first 2 arguments do not contain a file that exists")

        manager = FileSearchManager()
        results = manager.find(pattern, file)
        plt.rcdefaults()

        try:
            grapher = GraphIt()
            cdata = grapher.format_data(results)
            grapher.output_graph(cdata[0], cdata[1])
            print("Graph Created: ", grapher.file_name)
        except ImportError:
            print(
                "I used matplotlib and unfortunately that has dependencies you dont have installed.")
    else:
        raise ValueError(
            "The script expects 2 parameters. A path to a dir or file and a pattern")
