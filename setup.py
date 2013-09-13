from setuptools import setup

version = '0.1dev'
long_description = '\n\n'.join([
    open('README.md').read(),
    open('CHANGES.md').read(),
])

setup(
    name="datamora",
    version=version,
    description="Capture time in bits.",
    long_description=long_description,
    author="FLC Ltd.",
    author_email="contact@flcltd.com",
    url='http://datamora.com',
    license="MIT",
    keywords=['python', 'datamora', 'data', 'mora', 'server', 'capture', 'time', 'bits'],
    classifiers=[
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
    py_modules=['datamora'],
    packages=['apps', 'apps.fois', 'bottling'],
    package_data={'apps.fois': ['views/*']},
    zip_safe=False,
    install_requires=['bottle>=0.11', 'SQLAlchemy==0.8.2', 'pyyaml'],
    dependency_links=[
        'https://github.com/defnull/bottle/tarball/master#egg=bottle-0.12-dev'
    ]
)
