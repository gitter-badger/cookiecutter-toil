"""{{cookiecutter.project_slug}} module."""

from os.path import join
from os.path import abspath
from os.path import dirname
import json

ROOT = abspath(dirname(__file__))

with open(join(ROOT, "data", "setup.json"), "r") as f:
    SETUP = json.load(f)

__version__ = SETUP.get("version")

__author__ = SETUP.get("author")
