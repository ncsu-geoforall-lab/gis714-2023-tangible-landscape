#!/usr/bin/env python3

"""Run predefined case for each analysis and render it with its result"""

import argparse
import base64
import fnmatch
import json
import os
import subprocess
import weakref
from pathlib import Path
from xml.dom.minidom import getDOMImplementation


def is_python_file(path):
    """Return True if path is a Python file"""
    path = Path(path)
    return path.is_file() and path.suffix == ".py"


def is_json_file(path):
    """Return True if path is a JSON file"""
    path = Path(path)
    return path.is_file() and path.suffix == ".json"


def resolve_path(path, root_file):
    """Creates an absolute path from a path relative to root_file.

    Returns path as is if the input path is absolute.
    """
    path = Path(path)
    if path.is_absolute():
        return path
    base = Path(root_file).parent
    path = base / path
    return path.resolve()


class GrassRenderer:
    """Interface for rendering into a file using GRASS GIS

    Assuming that the provided filename is unique to a given instance.
    """

    def __init__(self, runner, filename, width=250, height=250):
        self._runner = runner
        self._env = os.environ.copy()
        self._env["GRASS_RENDER_FILE"] = filename
        self._env["GRASS_RENDER_IMMEDIATE"] = "cairo"
        self._env["GRASS_RENDER_FILE_READ"] = "TRUE"
        self._legend_file = Path(filename).with_suffix(".grass_vector_legend")
        self._env["GRASS_LEGEND_FILE"] = str(self._legend_file)
        self._env["GRASS_RENDER_WIDTH"] = str(width)
        self._env["GRASS_RENDER_HEIGHT"] = str(height)
        self._runner.run_env(self._env, ["d.erase"])

        # Since we asked for a vector legend,
        # we need to delete the legend file when done.
        def remove_if_exists(path):
            path.unlink(missing_ok=True)

        self._finalizer = weakref.finalize(self, remove_if_exists, self._legend_file)

    def run(self, *args):
        """Run a rendering command"""
        self._runner.run_env(self._env, list(args))

    def clean(self):
        """Remove temporary files"""
        self._finalizer()


class GrassRunner:
    """Interface for running GRASS tools or anything else in GRASS GIS as commands"""

    def __init__(self, executable, mapset):
        self.executable = executable
        self.mapset = mapset

    def run_env(self, env, args):
        """Run a command with environmental variables provided in env"""
        subprocess.check_call([self.executable, self.mapset, "--exec"] + args, env=env)

    def run(self, *args):
        """Run a command"""
        self.run_env(args=list(args), env=None)

    def run_python(self, *args):
        """Run a Python script.

        Assuming the correct Python interpreter is 'python'."""
        self.run("python", *args)


def image_to_text(filename):
    """Return file contents as 'data:image/png' suitable for inclusion into HTML.

    The file needs to be a PNG.
    """
    data = base64.b64encode(open(filename, "rb").read()).decode("utf-8")
    return "data:image/png;base64,{0}".format(data)


def add_head(dom, parent, title):
    head_element = dom.createElement("head")
    title_element = dom.createElement("title")
    title_element.appendChild(dom.createTextNode(title))
    head_element.appendChild(title_element)
    parent.appendChild(head_element)


def add_activity(dom, parent, activity, image, heading_level, image_as_data):
    heading = dom.createElement(heading_level)
    heading.appendChild(dom.createTextNode(activity["title"]))
    parent.appendChild(heading)
    author = dom.createElement("p")
    emphasis = dom.createElement("em")
    emphasis.appendChild(dom.createTextNode(f"Created by {activity['author']}."))
    author.appendChild(emphasis)
    parent.appendChild(author)
    description = dom.createElement("p")
    description.appendChild(dom.createTextNode(activity["instructions"]))
    parent.appendChild(description)
    img_paragraph = dom.createElement("p")
    img = dom.createElement("img")
    if image_as_data:
        data = image_to_text(image)
        img.setAttribute("src", data)
    else:
        img.setAttribute("src", image)
    img.setAttribute("alt", "Image rendered by the activity")
    img_paragraph.appendChild(img)
    parent.appendChild(img_paragraph)


def create_activity_page(activity, image, filename):
    """Create HTML page for an activity given its definition and redered image"""
    impl = getDOMImplementation()
    doc_type = impl.createDocumentType(
        "html",
        "-//W3C//DTD XHTML 1.0 Strict//EN",
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd",
    )
    dom = impl.createDocument("http://www.w3.org/1999/xhtml", "html", doc_type)
    html = dom.documentElement
    add_head(dom=dom, parent=html, title=activity["title"])
    body = dom.createElement("body")
    add_activity(
        dom=dom,
        parent=body,
        activity=activity,
        image=image,
        heading_level="h1",
        image_as_data=True,
    )
    html.appendChild(body)
    with open(filename, mode="w") as out:
        out.write(dom.toxml())


class IndexPage:
    """Multi-stage writter for a main/index file with multiple activities"""

    def __init__(self, title, filename):
        self._filename = filename
        impl = getDOMImplementation()
        doc_type = impl.createDocumentType(
            "html",
            "-//W3C//DTD XHTML 1.0 Strict//EN",
            "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd",
        )
        self._dom = impl.createDocument(
            "http://www.w3.org/1999/xhtml", "html", doc_type
        )
        self._html = self._dom.documentElement
        add_head(dom=self._dom, parent=self._html, title=title)
        self._body = self._dom.createElement("body")
        heading = self._dom.createElement("h1")
        heading.appendChild(self._dom.createTextNode(title))
        self._body.appendChild(heading)

    def add_activity(self, activity, image):
        """Add one activity and its image"""
        add_activity(
            dom=self._dom,
            parent=self._body,
            activity=activity,
            image=image,
            heading_level="h2",
            image_as_data=False,
        )

    def finish(self):
        """Finish creating HTML and write it to file"""
        # This is not most reusable, but it is all we need now.
        self._html.appendChild(self._body)
        with open(self._filename, mode="w") as out:
            out.write(self._dom.toxml())


def filename_matches_pattern(filename, patterns):
    """Return True if filename matches a pattern from patterns"""
    for pattern in patterns:
        if fnmatch.fnmatch(filename, pattern):
            return True
    return False


def main():
    """Process command line, collect files, and process them"""
    # We allow the main function to have more variables for sake of flow clarity.
    # pylint: disable=too-many-locals
    parser = argparse.ArgumentParser(
        description="Run, render, and create HTML for activities"
    )
    parser.add_argument("config_file", help="an integer for the accumulator")
    parser.add_argument("mapset_path", help="an integer for the accumulator")
    parser.add_argument(
        "--grass", default="grass", help="GRASS GIS exectutable (path or name)"
    )
    parser.add_argument(
        "--exclude",
        action="append",
        help="Exclude files based on pattern (shell wildcards with Python fnmatch)",
    )
    parser.add_argument(
        "--no-individual-pages",
        action="store_true",
        help="Do not generate separate pages for individual activities",
    )
    args = parser.parse_args()

    with open(args.config_file) as main_config_file:
        main_config = json.load(main_config_file)
    path = resolve_path(main_config["includeTasks"], args.config_file)

    grass_runner = GrassRunner(executable=args.grass, mapset=args.mapset_path)

    index_page = IndexPage(
        title="Tangible Landscape Activities Overview", filename="index.html"
    )

    for json_file in path.iterdir():
        if not is_json_file(json_file):
            continue
        if json_file.samefile(args.config_file):
            continue
        if args.exclude and filename_matches_pattern(str(json_file), args.exclude):
            continue
        with open(json_file) as file_o:
            activity_config = json.load(file_o)

        activity = activity_config["tasks"][0]
        python_file = activity["analyses"]
        python_file = resolve_path(python_file, json_file)

        grass_runner.run_python(python_file)
        img_name = str(Path(json_file.stem).with_suffix(".png"))
        grass_renderer = GrassRenderer(
            runner=grass_runner, filename=img_name, width=500, height=500
        )
        for layer in activity["layers"]:
            grass_renderer.run(*layer)
        if not args.no_individual_pages:
            html_name = str(Path(json_file.stem).with_suffix(".html"))
            create_activity_page(activity, img_name, html_name)
        index_page.add_activity(activity, img_name)

    index_page.finish()


if __name__ == "__main__":
    main()
