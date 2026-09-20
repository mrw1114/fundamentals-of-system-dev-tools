import subprocess
import sys
import pytest

def test_whitespace_name_exits_with_2():
    cmd = ["sdt-greet", "--name", "    "]
    result = subprocess.run(cmd, capture_output=True, text=True)
    # 预期退出码为 2
    assert result.returncode == 2