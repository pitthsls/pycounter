import os
import platform

from setuptools import find_packages, setup

version = {}  # will be set by exec below

with open(os.path.join(os.path.dirname(__file__), "pycounter/version.py"), "r") as fp:
    exec(fp.read(), version)

with open("README.rst") as readmefile:
    readme = readmefile.read()

requirements = ["openpyxl", "requests", "pendulum==2.0.3", "click", "lxml"]

if platform.python_implementation() == "PyPy":
    requirements = ["cython"] + requirements

setup(
    name="pycounter",
    python_requires=">=3.6",
    version=version["__version__"],
    packages=find_packages(),
    author="Health Sciences Library System, University of Pittsburgh",
    author_email="speargh@pitt.edu",
    maintainer="Geoffrey Spear",
    maintainer_email="speargh@pitt.edu",
    url="https://www.github.com/pitthsls/pycounter",
    project_urls={"Documentation": "https://pycounter.readthedocs.io"},
    description="Project COUNTER/NISO SUSHI statistics",
    long_description=readme,
    keywords="library COUNTER journals usage_statistics SUSHI",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: PyPy3",
    ],
    extras_require={
        "docs": ["sphinx", "sphinx_rtd_theme"],
        "tests": ["httmock", "mock", "pytest", "coverage"],
    },
    install_requires=requirements,
    entry_points={"console_scripts": ["sushiclient = pycounter.sushiclient:main"]},
)
