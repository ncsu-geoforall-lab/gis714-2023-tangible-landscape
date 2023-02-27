#!/usr/bin/env python3

"""
Test for Python functions in files
"""

import os
import shutil
import subprocess
import unittest


def is_python_file(path):
    """Return True if path is a Python file"""
    return os.path.isfile(path) and path.endswith(".py")


class TestFunctionsInFiles(unittest.TestCase):
    """Test to go through files and use"""

    path = "activities/"

    # name of or path to the main GRASS GIS executable and Python executable
    executable = "grass"
    python = "python3"

    # path to the existing location to use (assuming CI environment)
    location_path = "nc_spm_08_grass7"
    mapset_name = "test"
    mapset_path = os.path.join(location_path, mapset_name)

    def setUp(self):
        """Creates a mapset used in the tests"""
        subprocess.check_call([self.executable, "-c", self.mapset_path, "-e"])

    def tearDown(self):
        """Deletes the mapset"""
        shutil.rmtree(self.mapset_path, ignore_errors=True)

    def test_files_run(self):
        """Check that files run"""
        for filename in os.listdir(self.path):
            full_path = os.path.join(self.path, filename)
            if not is_python_file(full_path):
                continue
            return_code = subprocess.call(
                [self.executable, self.mapset_path, "--exec", self.python, full_path]
            )
            self.assertEqual(
                return_code, 0, msg=("Running {filename} failed".format(**locals()))
            )
            return_code = subprocess.call(
                [self.executable, self.mapset_path, "--exec", self.python, full_path]
            )
            self.assertEqual(
                return_code,
                0,
                msg=(
                    "Running {filename} the second time failed"
                    ' (maybe missing env=env or env["GRASS_OVERWRITE"] = "1"'.format(
                        **locals()
                    )
                ),
            )


if __name__ == "__main__":
    unittest.main()
