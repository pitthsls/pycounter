from setuptools import setup, find_packages

setup(
    name = 'pycounter',
    version = '0.3',
    packages = find_packages(),
    author = 'Geoffrey Spear',
    author_email = 'geoffspear@gmail.com',
    keywords = 'library COUNTER journals usage_statistics',
    test_suite = 'pycounter.test',
    install_requires = ['pyisbn', 'openpyxl', 'suds-jurko', 'six']
    )
