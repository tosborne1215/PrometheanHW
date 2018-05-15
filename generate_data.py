from faker import Faker
from shutil import rmtree
import os
import random
import string
import sys

seed = 12345678

fake = Faker()
fake.seed(seed)
random.seed(a=seed)


def generate_unique_word():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))


def get_key_word():
    return generate_unique_word()


def generate_huge_line():
    pass


def generate_huge_file(root, name):
    gig = 1024 * 1024 * 1024  # 1GB
    fname = os.path.join(root, name)
    with open(fname, 'wb') as fout:
        fout.write(os.urandom(gig))


def generate_file(root, name, keyword):
    keyword_occurences = 0
    fname = os.path.join(root, name)
    with open(fname, "w+") as f:
        for i in range(0, 500):
            if random.randint(0, 10) == 1:
                f.write(os.linesep)
            if random.randint(0, 10) == 2:
                f.write(keyword)
                keyword_occurences += 1
            f.write(fake.text())

    return keyword_occurences


def generate_deep_folder(root, depth=500, create_random_files=False):
    last_file_name = None
    for i in range(0, depth):
        if last_file_name is None:
            last_file_name = root

        if create_random_files:
            random_files = random.randint(0, 500)
            if random_files in [1, 2, 3, 4, 5, 6, 7, 8]:
                for i2 in range(0, random_files + 1):
                    random_name = generate_unique_word()
                    occurences = generate_file(
                        last_file_name, random_name, random_name)
                    print("The file: {} has the keyword: {} occuring {} times".format(
                        random_name, random_name, occurences))

        last_file_name = os.path.join(last_file_name, str(i))
        os.mkdir(last_file_name)
    return last_file_name


if __name__ == '__main__':
    root_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "data")
    old_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(old_limit + 500)
    rmtree(root_path, ignore_errors=True)
    sys.setrecursionlimit(old_limit)
    os.mkdir(root_path)

    deep_path_root = os.path.join(root_path, "deep_path_root")
    os.mkdir(deep_path_root)
    deep_dir = generate_deep_folder(deep_path_root)
    deep_file_name = generate_unique_word()
    # using the name as the keyword for the file. It will be randomly included
    occurences = generate_file(deep_dir, deep_file_name, deep_file_name)
    print("The file: {} has the keyword: {} occuring {} times".format(
        deep_file_name, deep_file_name, occurences))

    # A file exists at the bottom of this but it should be too deep
    too_deep_path_root = os.path.join(root_path, "too_deep_path_root")
    os.mkdir(too_deep_path_root)
    deepest_dir = generate_deep_folder(too_deep_path_root, old_limit + 10)
    too_deep_file_name = generate_unique_word()
    # using the name as the keyword for the file. It will be randomly included
    occurences = generate_file(
        deepest_dir, too_deep_file_name, too_deep_file_name)
    print("The file: {} has the keyword: {} occuring {} times".format(
        too_deep_file_name, too_deep_file_name, occurences))

    # Complex dir has many files scattered around
    complex_dir = os.path.join(root_path, "complex_dir_root")
    os.mkdir(complex_dir)
    deep_complex_dir = generate_deep_folder(
        complex_dir, 500, create_random_files=True)
