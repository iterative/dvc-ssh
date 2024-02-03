import pytest

from dvc.testing.api_tests import (  # noqa: F401
    TestAPI,
)
from dvc.testing.remote_tests import (  # noqa: F401
    TestRemote,
)
from dvc.testing.workspace_tests import (  # noqa: F401  # noqa: F401
    TestGetUrl,
    TestLsUrl,
)
from dvc.testing.workspace_tests import TestImport as _TestImport


@pytest.fixture
def cloud(make_cloud):
    return make_cloud(typ="ssh")


@pytest.fixture
def remote(make_remote):
    return make_remote(name="upstream", typ="ssh")


@pytest.fixture
def workspace(make_workspace):
    return make_workspace(name="workspace", typ="ssh")


class TestImport(_TestImport):
    @pytest.fixture
    def stage_md5(self):
        return "7033ee831f78a4dfec2fc71405516067"

    @pytest.fixture
    def is_object_storage(self):
        return False

    @pytest.fixture
    def dir_md5(self):
        return "b6dcab6ccd17ca0a8bf4a215a37d14cc.dir"
