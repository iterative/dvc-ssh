from dvc_ssh import SSHFileSystem

from .cloud import TEST_SSH_KEY_PATH

# TODO: InteractiveSSHClient.public_key_auth_requested

# "ssh": {
#     "type": supported_cache_type,
#     "port": Coerce(int),
#     "user": str,
#     "password": str,
#     "ask_password": Bool,
#     "passphrase": str,
#     "ask_passphrase": Bool,
#     "keyfile": str,
#     "timeout": Coerce(int),
#     "gss_auth": Bool,
#     "allow_agent": Bool,
#     "max_sessions": Coerce(int),
#     Optional("verify", default=False): Bool,
#     **REMOTE_COMMON,
# },


def test_denied_user(ssh_server, mocker):
    f = SSHFileSystem(
        host=ssh_server["host"],
        port=ssh_server["port"],
        user="user",
        keyfile=TEST_SSH_KEY_PATH,
    )

    assert f.fs


def test_password_set(ssh_server, mocker):
    f = SSHFileSystem(
        host=ssh_server["host"],
        port=ssh_server["port"],
        user="user",
        password="password",
    )

    assert f.fs


def test_password_prompt(ssh_server, mocker):
    f = SSHFileSystem(
        host=ssh_server["host"],
        port=ssh_server["port"],
        user="user",
        ask_password=True,
    )

    mock_getpass = mocker.patch(
        "dvc_ssh.ask_password",
    )
    mock_getpass.return_value = "password"

    assert f.fs
