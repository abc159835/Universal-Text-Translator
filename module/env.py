from pathlib import Path

# checkout the environment
def env():
    return True if Path(__file__).exists() else False


if env():
    PATH = Path(__file__).parent.parent.joinpath('dist')
else:
    PATH = Path(__file__).parent.parent.parent

WEB_PATH = PATH.joinpath('Application/static')