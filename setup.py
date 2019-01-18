import sys

try:
    # noinspection PyUnresolvedReferences
    from setuptools import setup, find_packages
except ImportError:
    print("Test result reporter now needs setuptools in order to build. Install it using"
          " your package manager (usually python-setuptools) or via pip (pip"
          " install setuptools).")
    sys.exit(1)

__version__ = '0.0.1'

# noinspection PyBroadException
try:
    with open('requirements.txt') as f:
        requirements = f.read().splitlines()
except Exception:
    requirements = []
    print("Error while parsing requirements file")

setup(
    name='telegram-removed-messages-notifier',
    version=__version__,
    description='Notify about removed messages in telegram',
    install_requires=requirements,
    packages=find_packages(),
    include_package_data=True,
    scripts=[
        'bin/telegram_removed_messages_notifier',
    ],
)