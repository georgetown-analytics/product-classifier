#!/usr/bin/env python

try:
    from setuptools import setup
    from setuptools import find_packages
except ImportError:
    raise ImportError("Could not import \"setuptools\". Please install the setuptools package.")


packages = find_packages(where=".",
    exclude=('tests', 'bin', 'docs', 'fixtures', 'conf'))

requires = []

with open('requirements.txt', 'r') as reqfile:
    for line in reqfile:
        requires.append(line.strip())

classifiers = (
    'Intended Audience :: Developers',
    'License :: Other/Proprietary License',
    'Natural Language :: English',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 2.7',
)

config = {
    "name": "Product Classifier",
    "version": "1.0",
    "description": "Classify products into categories by their name with NLTK",
    "author": "Benjamin Bengfort",
    "author_email": "benjamin.bengfort@georgetown.edu",
    "url": "https://github.com/georgetown-analytics/product-classifier",
    "packages": packages,
    "install_requires": requires,
    "classifiers": classifiers,
    "zip_safe": False,
    "scripts": ['bin/apparel-classify.py',],
}

setup(**config)
