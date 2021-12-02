import os

import pytest


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    return os.path.join(
        str(pytestconfig.rootdir), "dvc_ssh", "tests", "docker-compose.yml"
    )


@pytest.fixture
def make_ssh():
    def _make_ssh():
        raise NotImplementedError

    return _make_ssh


@pytest.fixture
def ssh(make_ssh):
    return make_ssh()

