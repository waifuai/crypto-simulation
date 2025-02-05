import subprocess
import pytest

def test_cli_help():
    # Test that the CLI provides a help message.
    result = subprocess.run(['python', 'main.py', '--help'], capture_output=True, text=True)
    assert result.returncode == 0
    assert "usage: main.py" in result.stdout
