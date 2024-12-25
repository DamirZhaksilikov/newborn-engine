from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name='newborn-engine',
    version='0.1dev0',
    author='Damir Zhaksilikov', 
    author_email='damir.zhaksilikov@gmail.com',
    packages=find_packages(),
    long_description=open('README.md').read()
)