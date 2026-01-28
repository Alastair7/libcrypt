import subprocess


def get_git_branch() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True
        ).strip()
    except Exception:
        return "You are not in a git directory"
