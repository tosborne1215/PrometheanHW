#!/usr/bin/python2.7

import unittest
import os
import sys
from app import FileSearchManager, FileSearchWorker, GraphIt


class FileSearchManagerTest(unittest.TestCase):
    manager = None
    data_folder = None

    def setUp(self):
        self.manager = FileSearchManager()
        self.data_folder = root_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "data")

    def tearDown(self):
        pass

    def test_invalid_input():
        pass

    def test_valid_input():
        pass

    def test_create_pool():
        pass

    def test_create_queue():
        pass

    def test_create_queue_from_no_dir(self):
        pass

    def test_create_queue_from_too_large_dir(self):
        pass

    def test_create_queue_from_too_long_fname(self):
        pass

    def test_check_file_exists(self):
        pass

    def test_check_file_not_exists(self):
        pass

    def test_find_on_deep_dir(self):
        pass

    def test_find_in_many_files(self):
        pass

    def test_get_results(self):
        pass


class FileSearchWorkerTest(unittest.TestCase):

    def test_search_large_file(self):
        pass

    # technically it is checked before now,
    # but maybe it should check it anyway?
    def test_search_nonexistent_file(self):
        pass

    def test_search_fname_too_long(self):
        pass


class GraphItTest(unittest.TestCase):

    def test_build_graph(self):
        pass

    def test_build_graph_from_none_data(self):
        pass

    def test_build_graph_from_large_data(self):
        pass


if __name__ == '__main__':
    unittest.main()
