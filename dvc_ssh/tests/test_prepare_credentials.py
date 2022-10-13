import pytest

from dvc_ssh import SSHFileSystem


@pytest.mark.parametrize("password", [None, "foo"])
@pytest.mark.parametrize("passphrase", [None, "bar"])
def test_passphrase(mocker, password, passphrase):
    connect = mocker.patch("asyncssh.connect")

    kwargs = {"password": password, "passphrase": passphrase}
    _ = SSHFileSystem(host="foo", **kwargs).fs

    assert connect.call_args[1]["password"] == password
    assert connect.call_args[1]["passphrase"] == passphrase
