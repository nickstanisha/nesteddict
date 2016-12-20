from __future__ import with_statement
from setuptools import setup
import nesteddict

nesteddict_classifiers = [
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Intended Audience :: Developers",
    "Topic :: Utilities"
]

with open("README.md", "r") as infile:
    long_description = infile.read()

setup(name="nesteddict",
      version=nesteddict.__version__,
      author="Nick Stanisha <github.com/nickstanisha>",
      url="http://github.com/nickstanisha/nesteddict",
      description="A nested dictionary data structure",
      long_description=long_description,
      license="MIT",
      classifiers=nesteddict_classifiers
      )