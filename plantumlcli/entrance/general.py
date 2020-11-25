from enum import IntEnum
from typing import Optional, Tuple

import click

from .base import _click_exception_with_exit_code
from .local import _check_local_plantuml, print_local_check_info
from .remote import _check_remote_plantuml, print_remote_check_info
from ..models.base import PlantumlType, Plantuml
from ..models.local import LocalPlantuml
from ..models.remote import RemotePlantuml
from ..utils import load_text_file


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


def print_text_graph(plantuml: Plantuml, sources: Tuple[str]):
    """
    Print text graph of source codes
    :param plantuml: plantuml object
    :param sources: source code files
    """
    for source in sources:
        click.echo('{source}: '.format(source=source))
        click.echo(plantuml.dump_txt(load_text_file(source)))