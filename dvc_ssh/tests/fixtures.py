# pylint: disable=redefined-outer-name

import os

import pytest

from .cloud import SSH, TEST_SSH_KEY_PATH, TEST_SSH_USER


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):  # pylint: disable=unused-argument
    return os.path.join(os.path.dirname(__file__), "docker-compose.yml")


@pytest.fixture(scope="session")
def ssh_server(docker_services):
    import asyncssh
    from sshfs import SSHFileSystem

    conn_info = {
        "host": "127.0.0.1",
        "port": docker_services.port_for("openssh-server", 2222),
    }

    def get_fs():
        return SSHFileSystem(
            **conn_info,
            username=TEST_SSH_USER,
            client_keys=[TEST_SSH_KEY_PATH],
        )

    def _check():
        try:
            get_fs().exists("/")
        except asyncssh.Error:
            return False
        else:
            return True

    docker_services.wait_until_responsive(timeout=30.0, pause=1, check=_check)
    return conn_info


@pytest.fixture
def ssh_connection(ssh_server):
    from sshfs import SSHFileSystem

    yield SSHFileSystem(
        host=ssh_server["host"],
        port=ssh_server["port"],
        username=TEST_SSH_USER,
        client_files=[TEST_SSH_KEY_PATH],
    )


@pytest.fixture
def make_ssh(ssh_server, monkeypatch):
    def _make_ssh():
        from dvc_ssh import SSHFileSystem

        # NOTE: see http://github.com/iterative/dvc/pull/3501
        monkeypatch.setattr(SSHFileSystem, "CAN_TRAVERSE", False)

        url = SSH(SSH.get_url(**ssh_server))
        url.mkdir(exist_ok=True, parents=True)
        return url

    return _make_ssh


@pytest.fixture
def ssh(make_ssh):
    return make_ssh()
