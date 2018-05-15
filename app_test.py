#!/usr/bin/python2.7

import unittest
import os
import sys
import re
from multiprocessing import Queue
from app import FileSearchManager, FileSearchWorker, GraphIt


class FileSearchManagerTest(unittest.TestCase):
    manager = None
    data_folder = None

    def setUp(self):
        self.manager = FileSearchManager()
        self.data_folder = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "data")

    def tearDown(self):
        pass

    # This test should throw an exception
    def test_invalid_expression_input(self):
        input_expr = "[Hey!ThisIsntAPattern["
        input_directory = os.path.join(self.data_folder, "shallow")

        with self.assertRaisesRegexp(ValueError, "Regex does not compile"):
            self.manager.find(input_expr, input_directory)

    def test_valid_input(self):
        input_expr = "/Tim/"
        input_directory = os.path.join(self.data_folder, "shallow")
        self.manager.find(input_expr, input_directory)

        self.assertIsNotNone(self.manager.get_results())

    def test_none_dir_input(self):
        input_expr = "/Tim/"
        input_directory = None

        with self.assertRaisesRegexp(ValueError, "Input dir is None"):
            self.manager.find(input_expr, input_directory)

    def test_none_expr_input(self):
        input_expr = None
        input_directory = os.path.join(self.data_folder, "shallow")

        with self.assertRaisesRegexp(ValueError, "Regex is None"):
            self.manager.find(input_expr, input_directory)

    def test_compile_invalid_expr(self):
        input_expr = "[Hey!ThisIsntAPattern["

        with self.assertRaisesRegexp(ValueError, "Regex does not compile"):
            self.manager.compile_expression(input_expr)

    def test_compile_valid_expr(self):
        input_expr = "/Tim/"
        compiled_expr = self.manager.compile_expression(input_expr)

        self.assertIsNotNone(compiled_expr)

    def test_compile_none_expr(self):
        input_expr = None

        with self.assertRaisesRegexp(ValueError, "Regex is None"):
            self.manager.compile_expression(input_expr)

    # This test should throw an exception
    def test_create_queue(self):
        input_directory = os.path.join(self.data_folder, "shallow")
        queue = self.manager.create_queue_from_dir(input_directory)

        self.assertIsInstance(queue, type(Queue()))
        self.assertGreaterEqual(queue.qsize, 1)

    def test_create_queue_from_none_dir(self):
        with self.assertRaisesRegexp(ValueError, "Input dir is None"):
            self.manager.create_queue_from_dir(None)

    # This test should throw an exception
    def test_create_queue_from_invalid_file(self):
        input_directory = os.path.join(
            self.data_folder, "shallow", "simple_file")

        with self.assertRaisesRegexp(ValueError, "Input dir is not dir"):
            self.manager.create_queue_from_dir(input_directory)

    # This test should throw an exception
    def test_create_queue_from_non_existent_dir(self):
        input_directory = os.path.join(
            self.data_folder, "shallow", "doesnt_exist")

        with self.assertRaisesRegexp(ValueError, "Input dir doesnt exist"):
            self.manager.create_queue_from_dir(input_directory)

    # This test should emit a warning but still provide some results
    def test_create_queue_from_too_large_dir(self):
        input_directory = os.path.join(
            self.data_folder, "too_deep_path_root")

        with self.assertRaisesRegexp(RuntimeError, "maximum recursion depth exceeded"):
            self.manager.create_queue_from_dir(input_directory)

    # should throw an exception
    def test_create_queue_from_too_long_fname(self):
        self.assertIsNone("", "No assertion")

    def test_check_file_exists(self):
        input_directory = os.path.join(
            self.data_folder, "too_deep_path_root")
        result = self.manager.check_file_exists(input_directory)

        self.assertIs(result, True)

    def test_check_file_not_exists(self):
        input_directory = os.path.join(
            self.data_folder, "nonexistent")
        result = self.manager.check_file_exists(input_directory)

        self.assertIs(result, False)

    def test_check_file_none_exists(self):
        input_directory = None
        result = self.manager.check_file_exists(input_directory)

        self.assertIs(result, False)

    def test_check_is_dir(self):
        input_directory = os.path.join(
            self.data_folder, "too_deep_path_root")
        result = self.manager.check_is_dir(input_directory)

        self.assertIs(result, True)

    def test_check_is_dir_when_is_file(self):
        input_directory = os.path.join(
            self.data_folder, "shallow", "simple_file")
        result = self.manager.check_is_dir(input_directory)

        self.assertIs(result, False)

    def test_check_is_dir_when_none(self):
        input_directory = None
        result = self.manager.check_is_dir(input_directory)

        self.assertIs(result, False)

    def test_find_on_deep_dir(self):
        input_expr = "/Tim/"
        input_directory = os.path.join(self.data_folder, "deep_dir_root")
        self.manager.find(input_expr, input_directory)

        self.assertIsNotNone(self.manager.get_results())
        self.assertGreater(len(self.manager.get_results().keys()), 1)

    def test_find_in_many_files(self):
        input_expr = "/Tim/"
        input_directory = os.path.join(self.data_folder, "complex_dir_root")
        self.manager.find(input_expr, input_directory)

        self.assertIsNotNone(self.manager.get_results())
        self.assertGreater(len(self.manager.get_results().keys()), 20)

    def test_get_results_without_find(self):
        self.assertIsNone(self.manager.get_results())

    def test_get_results_with_find(self):
        input_expr = "/Tim/"
        input_directory = os.path.join(self.data_folder, "shallow")
        self.manager.find(input_expr, input_directory)

        self.assertIsNotNone(self.manager.get_results())
        self.assertGreater(len(self.manager.get_results().keys()), 0)

    def test_create_pool(self):
        self.assertIsNone("", "No assertion")


class FileSearchWorkerTest(unittest.TestCase):

    def setUp(self):
        self.worker = FileSearchWorker()
        self.data_folder = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "data")

    def test_search_large_file(self):
        self.assertIsNone("", "No assertion")

    # technically it is checked before now,
    # but maybe it should check it anyway?
    def test_search_nonexistent_file(self):
        self.assertIsNone("", "No assertion")

    def test_search_fname_too_long(self):
        self.assertIsNone("", "No assertion")

    def test_search_fname(self):
        input_file = os.path.join(
            self.data_folder, "shallow", "simple_file")
        pattern = re.compile("/Tim/")
        results = self.worker.search_file(input_file, pattern)
        self.assertIsNotNone(results)
        self.assertGreater(results[1], 2)


class GraphItTest(unittest.TestCase):

    def test_build_graph(self):
        self.assertIsNone("", "No assertion")

    def test_build_graph_from_none_data(self):
        self.assertIsNone("", "No assertion")

    def test_build_graph_from_large_data(self):
        self.assertIsNone("", "No assertion")


if __name__ == '__main__':
    unittest.main()
