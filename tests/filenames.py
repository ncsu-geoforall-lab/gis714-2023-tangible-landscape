#!/usr/bin/env python3

"""Test filenames"""

import os
import unittest
from pathlib import Path


class TestFunctionsInFiles(unittest.TestCase):
    """Test to go through files and use"""

    path = "activities/"
    allow_files = [
        "advanced_example.json",
        "advanced_example.py",
        "simple_example.py",
        "simple_example.json",
    ]
    forbid_words = ["template", "example"]

    def test_filenames(self):
        """Check that files are named properly"""
        for filename in os.listdir(self.path):
            not_allowed = " ."
            for character in not_allowed:
                name = Path(filename).stem
                self.assertNotIn(
                    character,
                    name,
                    msg=(
                        f"The name '{filename}' contains '{character}', "
                        f"however characters '{not_allowed}' are not allowed "
                        "(replace it, e.g., by underscore)"
                    ),
                )

            if filename in self.allow_files:
                continue

            for expr in [r".*test_?[0-9]+\..*", r"^test\."]:
                self.assertNotRegex(
                    filename,
                    expr,
                    msg=(
                        f"The name '{filename}' seems like a local experiment"
                        " (use more descriptive name for this activity)"
                    ),
                )
            for word in self.forbid_words:
                self.assertNotIn(
                    word,
                    filename,
                    msg=(
                        f"The name '{filename}' contains the word '{word}'"
                        " (find a more fitting name for this activity)"
                    ),
                )


if __name__ == "__main__":
    unittest.main()
