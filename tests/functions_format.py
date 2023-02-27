#!/usr/bin/env python3

"""
Test for required internal structure of Python files
"""

import os
import re
import unittest


def is_python_file(path):
    """Return True if path is a Python file"""
    return os.path.isfile(path) and path.endswith(".py")


def get_all_python_files(directory):
    """Return Python files in a directory as pairs filename, full_path"""
    result = []
    for filename in os.listdir(directory):
        full_path = os.path.join(directory, filename)
        if not is_python_file(full_path):
            continue
        result.append((filename, full_path))
    return result


class TestContentOfFiles(unittest.TestCase):
    """Test to go through files and check internal structure"""

    path = "activities/"

    def test_files_have_main_part(self):
        """Check that files contain __name__ == ..."""
        for filename, full_path in get_all_python_files(self.path):
            with open(full_path) as file_handle:
                content = file_handle.read()
            self.assertRegex(
                content,
                r"\nif __name__ == .__main__.:",
                msg=(
                    "File {full_path} does not contain"
                    " the 'if __name__...' part".format(**locals())
                ),
            )

    def test_files_have_a_run_function(self):
        """Check that files contain at least one run_... function"""
        for filename, full_path in get_all_python_files(self.path):
            with open(full_path) as file_handle:
                content = file_handle.read()
            self.assertRegex(
                content,
                r"\ndef run_.+\(",
                msg=(
                    "File {full_path} does not contain any functions"
                    " with the 'run_' prefix".format(**locals())
                ),
            )

    def test_files_have_env_passed_to_functions(self):
        """Check that files contain at least one env=env assignment"""
        for filename, full_path in get_all_python_files(self.path):
            with open(full_path) as file_handle:
                content = file_handle.read()
            # only search starting with first function to avoid any explanatory
            # comments at the beginning
            # (still counting commented out ones as valid)
            content = re.split(r"\ndef run_.+\(", content)[1]
            # Assuming there is a char before and after the assignment
            # which will be fullfiled in all cases
            # (likely whitespace before and comma after)
            self.assertRegex(
                content,
                r"[^a-zA-Z0-9_]env\s*=\s*env[^a-zA-Z0-9_]",
                msg=(
                    "File {full_path} does not contain assignment env=env"
                    " which points to environment not being passed to"
                    " the run_command() function and its friends"
                    " (env is mandatory parameter for run_... functions"
                    " and env is the name of the paramter of run_command()"
                    " function)".format(**locals())
                ),
            )


if __name__ == "__main__":
    unittest.main()
