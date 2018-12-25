import os
from setuptools import setup, find_packages


def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()

setup(
    name='Multithread Scraper',
    version='0.1',
    url='https://github.com/trevorxander/2048',
    license='',
    author='Trevor Xander',
    author_email='trevorcolexander@gmail.com',
    long_description=read('README'),
    install_requires=['selenium'],
    packages=find_packages()

)
