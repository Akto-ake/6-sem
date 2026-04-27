from pathlib import Path
from zipfile import ZipFile

DOIT_CONFIG = {"default_tasks": ['docs']}


def task_docs():
    """"Create  documentation"""
    rstpy = list(Path(".").glob("**/*.rst")) + list(Path(".").glob("**/*.py")) 
    # print(rstpy)
    ext = {"html": "html", "text": "text"}
    for typ in ("html", "text"):
        yield {
            "name": f"{typ} doc",
            "actions": [f"cd doc && sphinx-build -M {typ} source source/_build"],
            "targets": [f"doc/source/_build/html/index.{ext[typ]}"],
            "file_dep": rstpy,
        }
    
def task_erase():
    """Clean all junk"""
    
    return {
        "actions": ["rm -rf doc/source/_build *.zip"],
    }

def task_zip():
    """Create zip archive"""
    def create_zip(filename, files):
        with (ZipFile(filename, "w") as zf):
            for f in files:
                zf.write(f)
    
    
    files = list(Path("doc/source/_build/html").glob("**"))
    
    return {
        "actions": [(create_zip, ["docs.zip", files])],
        "task_dep": ["docs"],
    }