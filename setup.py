from __future__ import with_statement

import os
import platform

from setuptools import find_packages, setup

version = {}  # will be set by exec below

with open(os.path.join(os.path.dirname(__file__), "pycounter/version.py"), "r") as fp:
    exec(fp.read(), version)

with open("README.rst") as readmefile:
    readme = readmefile.read()

requirements = ["openpyxl", "requests", "six", "pendulum", "click", "lxml"]

if platform.python_implementation() == "PyPy":
    requirements = ["cython"] + requirements

setup(
    name="pycounter",
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    version=version["__version__"],
    packages=find_packages(),
    author="Health Sciences Library System, University of Pittsburgh",
    author_email="speargh@pitt.edu",
    maintainer="Geoffrey Spear",
    maintainer_email="speargh@pitt.edu",
    url="http://www.github.com/pitthsls/pycounter",
    project_urls={"Documentation": "https://pycounter.readthedocs.io"},
    description="Project COUNTER/NISO SUSHI statistics",
    long_description=readme,
    keywords="library COUNTER journals usage_statistics SUSHI",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    extras_require={
        "docs": ["sphinx", "sphinx_rtd_theme"],
        "tests": ["httmock", "mock", "pytest", "coverage"],
    },
    install_requires=requirements,
    entry_points={"console_scripts": ["sushiclient = pycounter.sushiclient:main"]},
)
