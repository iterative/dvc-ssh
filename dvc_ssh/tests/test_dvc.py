import pytest
from dvc.testing.test_api import TestAPI  # noqa, pylint: disable=unused-import
from dvc.testing.test_remote import (  # noqa, pylint: disable=unused-import
    TestRemote,
)
from dvc.testing.test_workspace import (  # noqa, pylint: disable=unused-import
    TestAdd,
    TestImport,
)


@pytest.fixture
def cloud_name():
    return "ssh"


@pytest.fixture
def remote(make_remote, cloud_name):
    yield make_remote(name="upstream", typ=cloud_name)


@pytest.fixture
def workspace(make_workspace, cloud_name):
    yield make_workspace(name="workspace", typ=cloud_name)


@pytest.fixture
def stage_md5():
    return "dc24e1271084ee317ac3c2656fb8812b"


@pytest.fixture
def is_object_storage():
    return False


@pytest.fixture
def dir_md5():
    return "b6dcab6ccd17ca0a8bf4a215a37d14cc.dir"


@pytest.fixture
def hash_name():
    return "md5"


@pytest.fixture
def hash_value():
    return "8c7dd922ad47494fc02c388e12c00eac"


@pytest.fixture
def dir_hash_value(dir_md5):
    return "b6dcab6ccd17ca0a8bf4a215a37d14cc.dir"
