ckan-streamcatalog
==================

Stream Catalog extends CKAN to support data stream publishing and subscription
Author: Juhani Jaakkola, juhani.jaakkola@hiq.fi
Initial Creation: 24.03.2014 

Description
-----------

## Extension information

Extension name:
ckannext-streamcatalog

Description:
Stream Catalog extends CKAN to support data stream publishing and subscription"

CKAN source folder
/usr/lib/ckan/default/src

Git URL.
git@github.com:nullbox/ckan-streamcatalog.git


## Installation

### Install Py4J
> wget http://sourceforge.net/projects/py4j/files/0.8.1/py4j-0.8.1.tar.gz/download -O py4j-0.8.1.tar.gz
> tar -zxvf py4j-0.8.1.tar.gz
> sudo mv py4j-0.8.1 /opt/.

Run Python install in the Py4j folder to install 
> sudo python setup.py install 

### Py4J BrokerClient wrapper

Java 7 installation - needed by BrokerClient
> sudo apt-get install openjdk-7-jdk
> sudo update-alternatives --config java

Configuring $JAVA_HOME by editing /etc/environment - needed by WSO2 ESB
> sudo nano /etc/environment -> Add $JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64
> source /etc/environment

### Configuring StreamCatalog plugin

Install Python paster script - To create extension template
> sudo apt-get install python-pastescript

Create new extension template
> sudo paster --plugin=ckan create -t ckanext ckanext-iauthfunctions

Activate CKAN virtual environment
> . /usr/lib/ckan/default/bin/activate

Create test data to CKAN database
> . /usr/lib/ckan/default/bin/activate
> sudo ckan create-test-data

Install streamcatalog plugin to Python environment
> cd ../[StreamCatalog home]/
> sudo python setup.py develop

Add plugin to CKAN by editing - find section "ckan.plugins = ..." and append " streamcatalog"
> sudo nano /etc/ckan/default/production.ini


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
- [ ] Make Ant build script to build the Jar file -> Example from CommonBase project..btw. 
		The jar file includes whole lot of unnecessary stuff, 51mb in total??!
- [X] Expose publish / subscriebe & CreateTopic functions to CKAN interface
- [X] Install Py4J to virtual environment
- [ ] Implement IResourcePreview plugin interface
- [ ] Implement same origin policy properly in Stream Preview

- [ ] Wrap StreamCatalog functions to ajax/rest interface, so they could be called from jQuery (if possible)


Other notes
-----------

### CKAN implementation - Finding a place for hook
class ckan.plugins.interfaces.ITemplateHelpers <- Add custom template helper functions
class ckan.plugins.interfaces.IMiddleware <- Hook into Pylons middleware stack
ckan.plugins.interfaces.IDatasetForm <- Customize CKAN’s dataset (package) schemas and forms.

"By implementing this interface plugins can customise CKAN’s dataset schema, for example to add new custom fields to datasets."
