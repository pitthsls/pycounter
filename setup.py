from setuptools import setup, find_packages

__version__ = None  # will be set by exec below

exec(open('pycounter/_version.py', 'rb').read())

setup(
    name='pycounter',
    version=__version__,
    packages=find_packages(),
    author='Geoffrey Spear',
    author_email='geoffspear@gmail.com',
    description='Project COUNTER/NISO SUSHI statistics',
    keywords='library COUNTER journals usage_statistics SUSHI',
    test_suite='pycounter.test',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        ],
    install_requires=['pyisbn', 'openpyxl', 'lxml', 'requests',
                      'six', 'python-dateutil']
    )
