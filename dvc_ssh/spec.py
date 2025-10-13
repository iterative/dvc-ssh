import posixpath
from secrets import token_urlsafe

from sshfs import SSHFileSystem as _SSHFileSystem


def tmp_fname(prefix: str = "") -> str:
    """Temporary name for a partial download"""
    return f"{prefix}.{token_urlsafe(16)}.tmp"


class SSHFileSystem(_SSHFileSystem):
    async def _put_file(self, lpath, rpath, *args, **kwargs):
        parent = posixpath.dirname(rpath)
        tmp_info = posixpath.join(parent, tmp_fname())
        try:
            await super()._put_file(lpath, tmp_info, *args, **kwargs)
        except BaseException:
            # Handle stuff like KeyboardInterrupt
            # as well as other errors that might
            # arise during file transfer.
            try:
                await self._rm_file(tmp_info)
            except FileNotFoundError:
                pass
            raise
        else:
            await self._mv(tmp_info, rpath)
