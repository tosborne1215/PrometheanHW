#!/usr/bin/python2.7

from multiprocessing import Process, Queue, Pool


if __name__ == '__main__':
    subprocesses = list()
    filesQueue = Queue()
    results = dict()
