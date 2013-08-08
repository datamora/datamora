import os
from setuptools import setup

version = '0.1dev'
long_description = '\n\n'.join([
    open('README.md').read(),
    open('CHANGES.md').read(),
])

setup(
    name = "data-server",
    version = version,
    description = "Capture data that is relevant and timely.",
    long_description = long_description,
    author = "FLC Ltd.",
    author_email = "contact@flcltd.com",
    url = 'http://data.flcltd.com',
    license = "MIT",
    keywords = ['python', 'data', 'daeta', 'server', 'capture'],
    classifiers = [
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Bottle',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Database'
    ],
    py_modules = ['data_server'],
    zip_safe = False,
    install_requires = ['bottle'],
)