#!python

from setuptools import setup, find_packages

setup(
    name = 'ARMSCGen',
    version = '0.0.5',
    packages = find_packages(),
    py_modules = ['ARMSCGen'],
    author = 'alex.park',
    author_email = 'saintlinu07@gmail.com',
    url = 'https://github.com/alexpark07/ARMSCGen',
    description = 'ARM/Thumb Shellcode Generator',
    license = 'Mostly GPLv2, some licenses have different',
    classifiers          = [
        'Topic :: Security',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'License :: GPLv2 License',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers'
        ]
)
