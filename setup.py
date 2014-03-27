from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(
    name='ckanext-streamcatalog',
    version=version,
    description="Stream Catalog extends CKAN to support data stream publishing and subscription",
    long_description='''
    ''',
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='MMEA',
    author_email='juhani.jaakkola@hiq.fi',
    url='www.hiq.fi',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.streamcatalog'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points='''
        [ckan.plugins]
        # Add plugins here, e.g.
        # myplugin=ckanext.streamcatalog.plugin:PluginClass
    ''',
)
