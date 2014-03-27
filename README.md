ckan-streamcatalog
==================

Stream Catalog extends CKAN to support data stream publishing and subscription

Project started 24.03.2014

Project notes
-------------

## Guides

Install Python paster script
sudo apt-get install python-pastescript

Activate CKAN virtual environment
. /usr/lib/ckan/default/bin/activate

Create new extension template
sudo paster --plugin=ckan create -t ckanext ckanext-iauthfunctions

## Extension information

CKAN source folder
cd /usr/lib/ckan/default/src

Extension name:
ckannext-streamcatalog

Description:
Stream Catalog extends CKAN to support data stream publishing and subscription"

Git URL.
git@github.com:nullbox/ckan-streamcatalog.git

## TODO:
- [X] Development environment -> Check. vagrant-ckan-bash repository
- [X] Create a Git ja Github repositories for the project
- [X] Create a base for the inplementation
- [X] Create a class for Java Wrapper - Broker Client
- [X] Add Log4j and properties file to the wrapper class
- [ ] Create init.d script for the wrapper
- [X] Init BrokerClient - Java - TrustStore, WSO ESB connection -> well that was easy
- [X] Expose BrokerClient / Create needed functions to Wrapper
- [X] Create functional tests for wrapper functions
- [ ] Sure, you have a test, but convert it now into a JUnit test
- [ ] Failing test cases, try to break that client!
- [ ] Write Pyhton tests for wrapper class
- [X] Pass wrapper exeptions to Python, but log them first
- [ ] BrokerClient connection should be preserved long as possible. How long it actually is connected? Timeout somewhere?
- [ ] You can not remove a topic with BrokerClient, damned, fix this somehow?