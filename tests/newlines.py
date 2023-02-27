#!/usr/bin/env python3

"""
Test for required internal structure of Python files
"""

import os
import unittest


def is_tested_file(path):
    """Return True if path is a relevant for testing"""
    if os.path.isfile(path):
        name, extension = os.path.splitext(path)
        if extension in (".py", ".json"):
            return True
    return False


def get_all_tested_files(directory):
    """Return relevant files in a directory as pairs filename, full_path"""
    result = []
    for filename in os.listdir(directory):
        full_path = os.path.join(directory, filename)
        if not is_tested_file(full_path):
            continue
        result.append((filename, full_path))
    return result


class TestContentOfFiles(unittest.TestCase):
    """Test to go through files and check newlines"""

    path = "activities/"

    def test_files_have_unix_line_endings(self):
        """Check that files do not contain CRLF or CR"""
        for filename, full_path in get_all_tested_files(self.path):
            with open(full_path, "rb") as file_handle:
                content = file_handle.read()
            self.assertNotIn(
                b"\r\n",
                content,
                msg=(
                    "File {full_path} contains"
                    r" Windows newlines (CRLF, \r\n),"
                    r" unix newlines (LF, \n) are required"
                    " (use your text editor function to change line endings"
                    " to unix newlines)".format(**locals())
                ),
            )
            self.assertNotIn(
                b"\r",
                content,
                msg=(
                    "File {full_path} contains"
                    r" Old Mac newlines (CR, \r\n),"
                    r" unix newlines (LF, \n) are required"
                    " (use your text editor function to change line endings"
                    " to unix newlines)".format(**locals())
                ),
            )


if __name__ == "__main__":
    unittest.main()
