from enum import IntEnum
from typing import Optional, Tuple, Union

import click

from .base import _click_exception_with_exit_code
from .local import _check_local_plantuml, print_local_check_info
from .remote import _check_remote_plantuml, print_remote_check_info
from ..models.base import PlantumlType, Plantuml
from ..models.local import LocalPlantuml, LocalPlantumlExecuteError
from ..models.remote import RemotePlantuml
from ..utils import load_text_file, linear_process


def print_double_check_info(local_ok: bool, local: LocalPlantuml,
                            remote_ok: bool, remote: RemotePlantuml) -> None:
    """
    Check if remote and local plantuml is found and okay
    :param local_ok: local plantuml object initialize success or not
    :param local: local plantuml object or raised exception when initialize
    :param remote_ok: remote plantuml object initialize success or not
    :param remote: remote plantuml object or raised exception when initialize
    """
    _local_ok = _check_local_plantuml(local_ok, local)
    _remote_ok = _check_remote_plantuml(remote_ok, remote)
    if not _local_ok and not _remote_ok:
        raise _click_exception_with_exit_code('PlantumlNotFound', 'Neither local nor remote plantuml is found.', -1)


class PlantumlCheckType(IntEnum):
    LOCAL = PlantumlType.LOCAL.value
    REMOTE = PlantumlType.REMOTE.value
    BOTH = 3


def _get_check_type(check: bool, check_local: bool, check_remote: bool) -> Optional[PlantumlCheckType]:
    if check:
        return PlantumlCheckType.BOTH
    elif check_local:
        return PlantumlCheckType.LOCAL
    elif check_remote:
        return PlantumlCheckType.REMOTE
    else:
        return None


def print_check_info(check_type: PlantumlCheckType,
                     local_ok: bool, local: LocalPlantuml,
                     remote_ok: bool, remote: RemotePlantuml) -> None:
    """
    Check for all the situations of plantuml
    :param check_type: type of checking process (BOTH, LOCAL and REMOTE)
    :param local_ok: local plantuml object initialize success or not
    :param local: local plantuml object or raised exception when initialize
    :param remote_ok: remote plantuml object initialize success or not
    :param remote: remote plantuml object or raised exception when initialize
    """
    if check_type == PlantumlCheckType.BOTH:
        print_double_check_info(local_ok, local, remote_ok, remote)
    elif check_type == PlantumlCheckType.LOCAL:
        print_local_check_info(local_ok, local)
    elif check_type == PlantumlCheckType.REMOTE:
        print_remote_check_info(remote_ok, remote)
    else:
        # nothing to check, maybe warnings can be placed here.
        pass


def print_text_graph(plantuml: Plantuml, sources: Tuple[str], concurrency: int):
    """
    Print text graph of source codes
    :param plantuml: plantuml object
    :param sources: source code files
    :param concurrency: concurrency when running this
    """
    _error_count = 0

    def _process_text(src: str):
        try:
            return True, plantuml.dump_txt(load_text_file(src))
        except LocalPlantumlExecuteError as e:
            return False, e

    def _print_text(src: str, ret: Tuple[bool, Union[str, LocalPlantumlExecuteError]]):
        _success, _data = ret

        if _success:
            click.secho('{source}: '.format(source=src), fg='green')
            click.echo(_data)
        else:
            nonlocal _error_count
            click.secho('{source}: [error with exitcode {code}]'.format(source=src, code=_data.exitcode), fg='red')
            click.secho(_data.stderr, fg='red')
            _error_count += 1

    linear_process(
        items=sources,
        process=lambda i, src: _process_text(src),
        post_process=lambda i, src, ret: _print_text(src, ret),
        concurrency=concurrency
    )

    if _error_count > 0:
        raise _click_exception_with_exit_code(
            name='TextGraphError',
            message='{count} error(s) found when generating text graph.'.format(count=_error_count),
            exitcode=-2,
        )
