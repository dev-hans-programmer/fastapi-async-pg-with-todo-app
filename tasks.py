import subprocess
import sys


def run(cmd: str):
    """Running a shell command"""
    print(f'\n - Running: {cmd}')
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        sys.exit(result.returncode)


def format_code():
    run('uv run ruff format .')


def lint_code():
    run('uv run ruff check .')


def fix_code():
    format_code()
    run('uv run ruff check . --fix')


def run_project():
    run('fastapi dev app/main.py')


if __name__ == '__main__':
    actions = {
        'format': format_code,
        'lint': lint_code,
        'fix': fix_code,
        'run': run_project,
    }

    if len(sys.argv) < 2:
        print(f'Usage: python {sys.argv[0]} [format|lint|fix]')
        sys.exit(1)

    action = sys.argv[1]
    if action in actions:
        actions[action]()
    else:
        print(f'Unknown action: {action}')
        sys.exit(1)
