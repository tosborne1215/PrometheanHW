#!/usr/bin/python2.7

import unittest
import os
import re
import shutil
from time import sleep
from multiprocessing import Queue
from app import FileSearchManager, FileSearchWorker, GraphIt
import random
from generate_data import setUp as setUpDirs


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
        input_expr = "Tim"
        input_directory = os.path.join(self.data_folder, "shallow")
        self.manager.find(input_expr, input_directory)

        self.assertIsNotNone(self.manager.get_results())

    def test_none_dir_input(self):
        input_expr = "Tim"
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
        input_expr = "Tim"
        compiled_expr = self.manager.compile_expression(input_expr)

        self.assertIsNotNone(compiled_expr)

    def test_compile_none_expr(self):
        input_expr = None

        with self.assertRaisesRegexp(ValueError, "Regex is None"):
            self.manager.compile_expression(input_expr)

    # This test should throw an exception
    def test_create_queue(self):
        input_directory = os.path.join(self.data_folder, "shallow")
        self.manager.create_queue_from_dir(input_directory)
        queue = self.manager.manager_queue

        self.assertIsInstance(queue, type(self.manager.manager.Queue()))
        self.assertGreaterEqual(queue.qsize, 1)

    def test_create_queue_from_none_dir(self):
        with self.assertRaisesRegexp(ValueError, "Input dir is None"):
            self.manager.create_queue_from_dir(None)

    # This test should throw an exception
    def test_create_queue_from_non_existent_dir(self):
        input_directory = os.path.join(
            self.data_folder, "shallow", "doesnt_exist")

        self.manager.create_queue_from_dir(input_directory)
        self.assertIs(self.manager.manager_queue.qsize(), 0)

    # This test should emit a warning but still provide some results
    def test_create_queue_from_too_large_dir(self):
        input_directory = os.path.join(
            self.data_folder, "too_deep_path_root")

        with self.assertRaisesRegexp(RuntimeError, "maximum recursion depth exceeded"):
            self.manager.create_queue_from_dir(input_directory)

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
        input_expr = "ZWIJVV6CMF"
        input_directory = os.path.join(self.data_folder, "deep_path_root")
        result = self.manager.find(input_expr, input_directory)

        self.assertIsNotNone(result)
        self.assertGreaterEqual(len(result.keys()), 1)

    def test_hard_regex_on_find(self):
        input_expr = "1.*M"
        input_directory = os.path.join(self.data_folder, "complex_dir_root")
        result = self.manager.find(input_expr, input_directory)
        self.assertIsNotNone(result)
        self.assertGreater(len(result.keys()), 20)

    def test_find_in_many_files(self):
        input_expr = "1RIQUQ7LVM"
        input_directory = os.path.join(self.data_folder, "complex_dir_root")
        result = self.manager.find(input_expr, input_directory)
        self.assertIsNotNone(result)
        self.assertGreater(len(result.keys()), 20)

    def test_get_results_without_find(self):
        self.assertEquals(self.manager.get_results(), {})

    def test_get_results_with_find(self):
        input_expr = "Tim"
        input_directory = os.path.join(self.data_folder, "shallow")
        self.manager.find(input_expr, input_directory)

        self.assertIsNotNone(self.manager.get_results())
        self.assertGreater(len(self.manager.get_results().keys()), 0)

    def test_create_pool(self):
        self.manager.pattern = "Tim"
        input_directory = os.path.join(
            self.data_folder, "shallow", "simple_file")
        self.manager.manager_queue.put(input_directory)
        self.manager.create_pool()
        while self.manager.manager_queue.qsize() != 0:
            sleep(1)
        # print(multiprocessing.active_children())
        self.assertEqual(0, self.manager.manager_queue.qsize())

    def test_create_pool_no_pattern(self):
        with self.assertRaisesRegexp(ValueError, "No pattern to look for. Call find first."):
            self.manager.create_pool()


class FileSearchWorkerTest(unittest.TestCase):

    def setUp(self):
        my_queue = Queue()
        result_queue = Queue()
        pattern = "Tim"
        self.worker = FileSearchWorker(my_queue, pattern, result_queue)
        self.data_folder = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "data")

    # technically it is checked before now
    def test_search_nonexistent_file(self):
        input_directory = os.path.join(
            self.data_folder, "nonexistent")
        pattern = re.compile("Tim")
        with self.assertRaisesRegexp(ValueError, "file_name does not exist"):
            self.worker.search_file(input_directory, pattern)

    def test_search_fname(self):
        input_file = os.path.join(
            self.data_folder, "shallow", "simple_file")
        pattern = re.compile("Tim")
        results = self.worker.search_file(input_file, pattern)
        self.assertIsNotNone(results)
        self.assertGreater(results[1], 2)


class GraphItTest(unittest.TestCase):
    def setUp(self):
        self.graph = GraphIt()

    def tearDown(self):
        self.graph.file_name
        os.remove(self.graph.file_name)

    def test_format_data(self):
        pass

    def test_format_from_none_data(self):
        pass

    def test_format_from_large_data(self):
        pass

    def test_output_graph(self):
        pass

    def test_file_name_output(self):
        pass


if __name__ == '__main__':
    setUpDirs()
    unittest.main()
