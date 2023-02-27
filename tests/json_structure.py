#!/usr/bin/env python3

"""
Test for JSON format in activities
"""

import json
import os
import unittest


def is_json_file(path):
    """Return True if path is a JSON file"""
    return os.path.isfile(path) and path.endswith(".json")


def is_python_file(path):
    """Return True if path is a Python file"""
    return os.path.isfile(path) and path.endswith(".py")


def get_all_json_files(directory):
    """Return JSON files in a directory as pairs filename, full_path"""
    result = []
    for filename in os.listdir(directory):
        full_path = os.path.join(directory, filename)
        if not is_json_file(full_path):
            continue
        result.append((filename, full_path))
    return result


def get_all_python_files(directory):
    """Return Python files in a directory as pairs filename, full_path"""
    result = []
    for filename in os.listdir(directory):
        full_path = os.path.join(directory, filename)
        if not is_python_file(full_path):
            continue
        result.append((filename, full_path))
    return result


class TestContentOfJsonFiles(unittest.TestCase):
    """Test to go through files and check internal structure and content"""

    path = "activities/"
    config_example_names = ["advanced_example.json", "simple_example.json"]
    text_items = ["title", "analyses", "author", "instructions"]
    main_config_file = "config.json"

    def test_files_have_expected_content(self):
        """Check that files contain required pieces"""
        for filename, full_path in get_all_json_files(self.path):
            with open(full_path) as file_handle:
                try:
                    content = json.load(file_handle)
                except json.JSONDecodeError as err:  # noqa: F841
                    self.fail(
                        "File {full_path} is not properly formatted JSON: {err}".format(
                            **locals()
                        )
                    )
                self.assertIn(
                    "tasks",
                    content,
                    msg=("tasks key not in {full_path} file".format(**locals())),
                )
                tasks = content["tasks"]
                self.assertIsInstance(
                    tasks,
                    list,
                    msg="tasks must be a list (of tasks), not {provided_type}".format(
                        provided_type=type(tasks)
                    ),
                )
                self.assertTrue(
                    tasks, msg="tasks list must contain at least one item (task)"
                )
                for task in tasks:
                    self.assertIsInstance(
                        task,
                        dict,
                        msg="task must be a dictionary, not {provided_type}".format(
                            provided_type=type(tasks)
                        ),
                    )
                    self.assertTrue(task, msg="task must be a non-empty dictionary")
                    self.assertIn(
                        "layers",
                        task,
                        msg=(
                            "layers key not in a task in {full_path} file".format(
                                **locals()
                            )
                        ),
                    )
                    for item_key in self.text_items:
                        self.assertIn(
                            item_key,
                            task,
                            msg=f"task needs to have {item_key} (fix {filename})",
                        )
                        item = task[item_key]
                        self.assertIsInstance(
                            item,
                            str,
                            msg=(
                                f"{item_key} must be str (string of characters), "
                                f"not {type(item)} (fix {filename})"
                            ),
                        )
                        self.assertTrue(
                            item, msg=f"{item_key} must not be empty (fix {filename})"
                        )

                    layers = task["layers"]
                    self.assertIsInstance(
                        layers,
                        list,
                        msg=f"layers must be a list (of layers), not {type(layers)}",
                    )
                    self.assertTrue(
                        layers, msg="layers list must contain at least one item (layer)"
                    )
                    for layer in layers:
                        self.assertIsInstance(
                            layer,
                            list,
                            msg=f"layer must be a list (a command), not {type(layer)}",
                        )
                        self.assertTrue(
                            layer,
                            msg="layer must contain at least one item (module name)",
                        )

    def test_python_file_exists(self):
        """Check that referenced file exists"""
        for filename, full_path in get_all_json_files(self.path):
            with open(full_path) as file_handle:
                content = json.load(file_handle)
                for task in content["tasks"]:
                    python_file = task["analyses"]
                    if not os.path.isfile(os.path.join(self.path, python_file)):
                        self.fail(
                            "File {full_path} refers to {python_file}"
                            " which does not exist".format(**locals())
                        )

    def test_python_filename_matches_json(self):
        """Check that filenames match if there is one task in a JSON file"""
        for filename, full_path in get_all_json_files(self.path):
            if filename == self.main_config_file:
                # Skip checking the main config file.
                continue
            with open(full_path) as file_handle:
                content = json.load(file_handle)
                tasks = content["tasks"]
                # name match makes sense only for files with one task
                if len(tasks) == 1:
                    python_file = tasks[0]["analyses"]
                    python_file_no_ext = os.path.splitext(python_file)[0]
                    json_file_no_ext = os.path.splitext(filename)[0]
                    self.assertEqual(
                        python_file_no_ext,
                        json_file_no_ext,
                        msg=(
                            f"Python filename {python_file}"
                            " does not match JSON filename {filename}"
                            " (required for files with only one task)".format(
                                **locals()
                            ),
                        ),
                    )
                # else skip the test

    def test_files_not_in_root(self):
        """Check that no Python and JSON files are in the root directory"""
        # There is no code for ignoring (allowing) some files,
        # but we don't need any now.
        files = get_all_python_files(".")
        # files is list of tuples and we print it as is,
        # so the readability is not ideal.
        self.assertEqual(
            len(files),
            0,
            msg=(
                "There should be no Python files in the root (main) directory, "
                f"but the following .py files are there: {files} "
                "All Python files for activities should be in the activities directory."
            ),
        )
        files = get_all_json_files(".")
        self.assertEqual(
            len(files),
            0,
            msg=(
                "There should be no JSON config files in the root (main) directory, "
                f"but the following .json files are there: {files} "
                "All JSON files for activities should be in the activities directory."
            ),
        )

    def test_python_file_in_json(self):
        """Check that all Python files are referenced by a JSON config file"""
        for python_filename, python_full_path in get_all_python_files(self.path):
            file_mentioned = False
            for json_filename, json_full_path in get_all_json_files(self.path):
                with open(json_full_path) as file_handle:
                    content = json.load(file_handle)
                    for task in content["tasks"]:
                        if python_filename == task["analyses"]:
                            file_mentioned = True
                            break
                if file_mentioned:
                    break
            self.assertTrue(
                file_mentioned,
                msg=(
                    "Python file {python_filename} is not referenced"
                    " by any JSON configuration".format(**locals())
                ),
            )

    def test_configuration_is_not_from_template(self):
        """Check that configuration is different from provided examples or templates"""
        for example in self.config_example_names:
            self.configuration_is_not_from_template(example)

    def configuration_is_not_from_template(self, example):
        """Run comparison for one example or template file"""
        with open(os.path.join(self.path, example)) as file_handle:
            # assuming we have exactly one task in the template
            template_task = json.load(file_handle)["tasks"][0]
        for filename, full_path in get_all_json_files(self.path):
            # do not check the template itself and main config
            if filename in (example, self.main_config_file):
                continue
            with open(full_path) as file_handle:
                content = json.load(file_handle)
            for task in content["tasks"]:
                for key in self.text_items:
                    self.assertNotEqual(
                        task[key],
                        template_task[key],
                        msg=(
                            "Value of {key} in a task in {filename} matches"
                            " value from the example file {example}."
                            " {key} value should be different"
                            " from the provided example."
                            " Change the {key} value in {filename})".format(**locals())
                        ),
                    )
                if len(task["layers"]) == len(template_task["layers"]):
                    match_count = 0

                    for layer, template_layer in zip(
                        task["layers"], template_task["layers"]
                    ):
                        # lists of strings can be just compared with equal
                        if layer == template_layer:
                            match_count += 1

                    if match_count == len(task["layers"]):
                        self.fail(
                            f"Layers in {filename} are identical with"
                            f" the example file {example}."
                            " Layers should be different from the provided example."
                            f" Add, remove, or modify the list of layers in {filename}"
                            f" to match the output of analysis in {task['analyses']}"
                        )


if __name__ == "__main__":
    unittest.main()
