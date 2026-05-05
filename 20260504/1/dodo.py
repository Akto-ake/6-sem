from pathlib import Path
import shutil

from doit.task import clean_targets


DOIT_CONFIG = {"default_tasks": ["html"]}

def task_pot():
    """Build translation"""
    return {
        "file_dep": list(Path("mood").glob("**/*.py")),
        "actions": ["python3 -m babel.messages.frontend extract -o mud.pot mood"],
        "targets": ["mud.pot"],
        "clean": [clean_targets],
    }


def task_po():
    """Update translation"""
    return {
        "file_dep": ["mud.pot"],
        "actions": [
            "python3 -m babel.messages.frontend update "
            "-D mud -i mud.pot -d po -l ru_RU.UTF-8 --init-missing",
        ],
        "targets": ["po/ru_RU.UTF-8/LC_MESSAGES/mud.po"],
        "task_dep": ["pot"],
        "clean": [clean_targets],
    }


def task_mo():
    """Compile translation"""
    return {
        "file_dep": ["po/ru_RU.UTF-8/LC_MESSAGES/mud.po"],
        "actions": [
            "python3 -m babel.messages.frontend compile "
            "-D mud -d po -l ru_RU.UTF-8",
        ],
        "targets": ["po/ru_RU.UTF-8/LC_MESSAGES/mud.mo"],
        "task_dep": ["po"],
        "clean": [clean_targets],
    }


def task_i18n():
    """Build i18n"""
    return {
        "actions": ["touch .i18n"],
        "targets": [".i18n"],
        "task_dep": ["pot", "po", "mo"],
        "clean": [clean_targets],
    }


def task_html():
    """Build html"""
    rstpy = list(Path("doc").glob("**/*.rst")) + list(Path("mood").glob("**/*.py")) + [Path("doc/conf.py")]
    return {
        "actions": ["sphinx-build -M html doc doc/_build"],
        "targets": ["doc/_build/html/index.html"],
        "file_dep": rstpy,
        "clean": [(shutil.rmtree, ["doc/_build"], {"ignore_errors": True})],
    }


def task_test():
    """Run tests"""
    return {
        "file_dep": ["po/ru_RU.UTF-8/LC_MESSAGES/mud.mo", "test_server.py"],
        "actions": ["python3 -m unittest test_server.py", "touch .test"],
        "targets": [".test"],
        "task_dep": ["i18n"],
        "clean": [clean_targets],
    }
