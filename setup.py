#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0', ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

DATA_FILES = [
    ('/usr/share/icons/graph_simulacra', ['icons/icons8-plus-48.png']),
    ('/usr/share/icons/graph_simulacra', ['icons/icons8-save-48.png']),
    ('/usr/share/icons/graph_simulacra', ['icons/icons8-quill-with-ink-48.png'])
]

setup(
    author="Janith Perera",
    author_email='janith@member.fsf.org',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
    ],
    description="A graphical presentation of graph matrices.",
    entry_points={
        'console_scripts': [
            'graph_simulacra=graph_simulacra.cli:main',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='graph_simulacra',
    name='graph_simulacra',
    packages=find_packages(include=['graph_simulacra']),
    data_files=DATA_FILES,
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/jantwisted/graph_simulacra',
    version='0.1.0',
    zip_safe=False,
)
