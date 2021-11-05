import sys
import os
import types
import logging

_UNKNOWN_CLIENT_IP = "Unknown-X.X.X.X"
ENABLE_LOGGING_CALLCHAIN_SSHCLIENT = "ENABLE_LOGGING_CALLCHAIN_SSHCLIENT"


class Logger(logging.Logger):
    def print_callchain_sshclient(self, msg: str) -> str:
        """Support print call chain and ssh connection info."""
        # 0: _log; 1: info/debug/...; 2: see %(funcName)s; 3: caller
        # PY 3.8 add `stacklevel` parameter, see: https://github.com/python/cpython/pull/7424
        ssh_connection_client = os.getenv("SSH_CONNECTION", os.getenv("SSH_CLIENT", _UNKNOWN_CLIENT_IP))
        if ssh_connection_client != _UNKNOWN_CLIENT_IP:
            msg = "%s by client=%r " % (msg, ssh_connection_client.split(maxsplit=1)[0])
        caller_three, caller_four = range(3, 5)
        try:
            caller_frame = sys._getframe(caller_three)  # type: types.FrameType
            caller_frame_filename = os.path.basename(caller_frame.f_code.co_filename)
            msg = "%s -> by %s caller(%r:%s in %r) " % (
                msg,
                caller_three,
                caller_frame.f_code.co_name,
                caller_frame.f_lineno,
                caller_frame_filename,
            )
        except ValueError:
            msg = msg
        else:
            try:
                caller_frame = caller_frame.f_back
                caller_frame_filename = os.path.basename(caller_frame.f_code.co_filename)
                msg = "%s -> by %s caller(%r:%s in %r)" % (
                    msg,
                    caller_four,
                    caller_frame.f_code.co_name,
                    caller_frame.f_lineno,
                    caller_frame_filename,
                )
            except AttributeError:
                msg = msg
        return msg

    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False, **kwargs):
        if os.getenv(ENABLE_LOGGING_CALLCHAIN_SSHCLIENT):
            msg = self.print_callchain_sshclient(msg)
        super(__class__, self)._log(level, msg, args, exc_info=None, extra=None, stack_info=False, **kwargs)
