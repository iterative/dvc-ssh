import pytest
from dvc.testing.api_tests import (  # noqa, pylint: disable=unused-import
    TestAPI,
)
from dvc.testing.remote_tests import (  # noqa, pylint: disable=unused-import
    TestRemote,
)
from dvc.testing.workspace_tests import TestAdd as _TestAdd
from dvc.testing.workspace_tests import (  # noqa, pylint: disable=unused-import
    TestGetUrl,
)
from dvc.testing.workspace_tests import TestImport as _TestImport
from dvc.testing.workspace_tests import (  # noqa, pylint: disable=unused-import
    TestLsUrl,
)


@pytest.fixture
def cloud(make_cloud):
    yield make_cloud(typ="ssh")


@pytest.fixture
def remote(make_remote):
    yield make_remote(name="upstream", typ="ssh")


@pytest.fixture
def workspace(make_workspace):
    yield make_workspace(name="workspace", typ="ssh")


class TestImport(_TestImport):
    @pytest.fixture
    def stage_md5(self):
        return "dc24e1271084ee317ac3c2656fb8812b"

    @pytest.fixture
    def is_object_storage(self):
        return False

    @pytest.fixture
    def dir_md5(self):
        return "b6dcab6ccd17ca0a8bf4a215a37d14cc.dir"


class TestAdd(_TestAdd):
    @pytest.fixture
    def hash_name(self):
        return "md5"

    @pytest.fixture
    def hash_value(self):
        return "8c7dd922ad47494fc02c388e12c00eac"

    @pytest.fixture
    def dir_hash_value(self):
        return "b6dcab6ccd17ca0a8bf4a215a37d14cc.dir"
