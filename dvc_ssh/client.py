import asyncio
import os
import sys
from collections.abc import Sequence
from getpass import getpass
from typing import TYPE_CHECKING, Optional, cast

from asyncssh import SSHClient
from asyncssh.public_key import (
    _DEFAULT_KEY_FILES,
    KeyEncryptionError,
    KeyImportError,
    SSHLocalKeyPair,
    read_private_key,
    read_public_key,
)

if TYPE_CHECKING:
    from asyncssh.auth import KbdIntPrompts, KbdIntResponse
    from asyncssh.config import FilePath
    from asyncssh.connection import SSHClientConnection
    from asyncssh.misc import MaybeAwait
    from asyncssh.public_key import KeyPairListArg, SSHKey


class InteractiveSSHClient(SSHClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._conn: Optional["SSHClientConnection"] = None
        self._keys_to_try: Optional[list["FilePath"]] = None
        self._passphrases: dict[str, str] = {}

    def connection_made(self, conn: "SSHClientConnection") -> None:
        self._conn = conn
        self._keys_to_try = None

    def connection_lost(self, _exc: Optional[Exception]) -> None:
        self._conn = None

    async def public_key_auth_requested(
        self,
    ) -> Optional["KeyPairListArg"]:
        assert self._conn is not None
        if self._keys_to_try is None:
            self._keys_to_try = []
            options = self._conn._options
            config = options.config
            client_keys = cast(Sequence["FilePath"], config.get("IdentityFile", ()))
            if not client_keys:
                client_keys = [
                    os.path.expanduser(os.path.join("~", ".ssh", path))
                    for path, cond in _DEFAULT_KEY_FILES
                    if cond
                ]
            for key_to_load in client_keys:
                try:
                    read_private_key(key_to_load, passphrase=options.passphrase)
                except KeyImportError as exc:
                    if str(exc).startswith("Passphrase"):
                        self._keys_to_try.append(key_to_load)
                except OSError:
                    pass

        while self._keys_to_try:
            key_to_load = self._keys_to_try.pop()
            pubkey_to_load = str(key_to_load) + ".pub"
            try:
                key = await self._read_private_key_interactive(key_to_load)
            except KeyImportError:
                continue
            try:
                pubkey: Optional["SSHKey"] = read_public_key(pubkey_to_load)
            except (OSError, KeyImportError):
                pubkey = None
            return SSHLocalKeyPair(key, pubkey)
        return None

    async def _read_private_key_interactive(self, path: "FilePath") -> "SSHKey":
        path = str(path)
        passphrase = self._passphrases.get(path)
        if passphrase:
            return read_private_key(path, passphrase=passphrase)

        loop = asyncio.get_running_loop()
        for _ in range(3):
            passphrase = await loop.run_in_executor(
                None, getpass, f"Enter passphrase for key '{path}': "
            )
            if passphrase:
                try:
                    key = read_private_key(path, passphrase=passphrase)
                    self._passphrases[path] = passphrase
                    return key
                except (KeyImportError, KeyEncryptionError):
                    pass
        raise KeyImportError("Incorrect passphrase")

    def kbdint_auth_requested(self) -> "MaybeAwait[Optional[str]]":
        return ""

    async def kbdint_challenge_received(
        self,
        name: str,
        instructions: str,
        _lang: str,
        prompts: "KbdIntPrompts",
    ) -> Optional["KbdIntResponse"]:
        assert self._conn is not None
        options = self._conn._options
        username = f"{options.username}" if options.username else ""
        if options.host:
            prompt_prefix = f"({username}@{options.host}) "
        elif username:
            prompt_prefix = f"({username}) "
        else:
            prompt_prefix = ""

        def _getpass(prompt: str) -> str:
            prompt = f"{prompt_prefix}{prompt}"
            return getpass(prompt=prompt).rstrip()

        # NOTE: we write an extra line otherwise the prompt will be written on
        # the same line as any active tqdm progress bars
        sys.stderr.write(os.linesep)
        if instructions:
            sys.stderr.write(f"{instructions}{os.linesep}")
        loop = asyncio.get_running_loop()
        return [
            await loop.run_in_executor(
                None, _getpass, f"({name}) {prompt}" if name else prompt
            )
            for prompt, _ in prompts
        ]
