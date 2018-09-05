import os
import unittest

TEST_DIRECTORY_PREFIX = 'tests'
bad_folders = ['env', '.git', '__pycache__', '.idea']


def get_test_dirs(root_path, test_dirs):
    for obj in os.listdir(root_path):
        path = os.path.join(root_path, obj)
        if os.path.isdir(path):
            if obj not in bad_folders:
                if obj.startswith(TEST_DIRECTORY_PREFIX):
                    test_dirs.append(path)
                else:
                    get_test_dirs(path, test_dirs)
    return test_dirs


def test_all():
    dirs = get_test_dirs(os.path.dirname(os.path.abspath(__file__)), [])
    for test_dir in dirs:
        suite = unittest.TestLoader().discover(test_dir)
        unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == "__main__":
    test_all()
