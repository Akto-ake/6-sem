def task_docs():
    """"Create  documentation"""

    return {
        "actions": ["cd doc && sphinx-build -M html . _build"],
    }