import subprocess


def test_whitespace_name_exits_with_2():
    cmd = ["sdt-greet", "--name", "    "]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    # 预期退出码为 2
    assert result.returncode == 2


def test_normal_name():
    cmd = ["sdt-greet", "--name", "王俊杰"]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    assert result.returncode == 0
    assert "Hello, 王俊杰" in result.stdout
