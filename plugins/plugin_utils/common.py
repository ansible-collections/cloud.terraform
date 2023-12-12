# -*- coding: utf-8 -*-

# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import subprocess
from typing import List, Tuple


# no module available here, mock functionality to be consistent throughout the rest of the codebase
def module_run_command(cmd: List[str], cwd: str, check_rc: bool) -> Tuple[int, str, str]:
    completed_process = subprocess.run(cmd, capture_output=True, check=check_rc, cwd=cwd)
    return (
        completed_process.returncode,
        completed_process.stdout.decode("utf-8"),
        completed_process.stderr.decode("utf-8"),
    )
