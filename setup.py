from setuptools import setup, find_packages
import sys, os

version = '0.0.1'

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
    message_extractors = {
        'ckanext/streamcatalog': [
            ('**.py', 'python', None),
            ('templates/**.html', 'ckan', None),
            ('public/**', 'ignore', None)
            ],
        # Include CKAN core translations to ease translation combination process.
        '../ckan/ckan': [
            ('**.py', 'python', None),
            ('**.js', 'javascript', None),
            ('templates/importer/**', 'ignore', None),
            ('templates/**.html', 'ckan', None),
            ('templates_legacy/**.html', 'ckan', None),
            ('ckan/templates/home/language.js', 'genshi', {
                'template_class': 'genshi.template:TextTemplate'
            }),
            ('templates/**.txt', 'genshi', {
                'template_class': 'genshi.template:TextTemplate'
            }),
            ('templates_legacy/**.txt', 'genshi', {
                'template_class': 'genshi.template:TextTemplate'
            }),
            ('public/**', 'ignore', None),
        ],
        '../ckan/ckanext': [
            ('**.py', 'python', None),
            ('**.html', 'ckan', None),
            ('multilingual/solr/*.txt', 'ignore', None),
            ('**.txt', 'genshi', {
                'template_class': 'genshi.template:TextTemplate'
            }),
        ]
    },
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points='''
        [ckan.plugins]
        streamcatalog=ckanext.streamcatalog.plugin:StreamCatalogPlugin
        ''',
)
