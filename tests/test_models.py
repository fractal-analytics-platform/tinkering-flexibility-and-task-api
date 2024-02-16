from devtools import debug
from models import Task


def _dummy_function():
    pass


def test_model_task():
    NEW_FILTERS = dict(attribute=True)
    task = Task(function=_dummy_function, new_filters=NEW_FILTERS)
    debug(task.new_filters)
    debug(NEW_FILTERS)
    assert task.new_filters == NEW_FILTERS
