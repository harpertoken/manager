# SPDX-License-Identifier: MIT

from setuptools import setup, find_packages
from manager._version import __version__

setup(
    name="manager",
    version=__version__,
    packages=find_packages(),
    install_requires=["jinja2"],
    extras_require={
        "test": ["pytest"],
    },
    entry_points={
        "console_scripts": [
            "manager-cli=manager.cli:main",
        ],
    },
    author="opencode",
    description="A library for generating xAI API tool call templates using Jinja2",
    license="MIT",
)
