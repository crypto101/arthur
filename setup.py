import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

import re
versionLine = open("cryptoctf/_version.py", "rt").read()
match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", versionLine, re.M)
versionString = match.group(1)

class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        sys.exit(tox.cmdline([]))

setup(name='cryptoctf',
      version=versionString,
      description='Software for the exercises in Crypto 101, the introductory '
                  'book on cryptography.',
      long_description='The game client for an online, hacker-themed text '
                       'adventure revolving around breaking cryptosystems. '
                       'Built using Twisted and Urwid.',
      url='https://github.com/lvh/cryptoctf',

      author='Laurens Van Houtven',
      author_email='_@lvh.io',

      packages=["cryptoctf", "cryptoctf.test"],
      test_suite="cryptoctf.test",
      #setup_requires=['tox'],
      cmdclass={'test': Tox},
      zip_safe=True,

      license='ISC',
      keywords="crypto urwid twisted",
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Framework :: Twisted",
        "Intended Audience :: Education",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Programming Language :: Python :: 2 :: Only",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Education",
        "Topic :: Games/Entertainment",
        "Topic :: Security :: Cryptography",
        ]
)
