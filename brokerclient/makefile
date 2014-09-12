basedir = /var/www/ckan/pyenv/src/ckanext-streamcatalog/brokerclient
libdir = $(basedir)/lib
srcdir = $(basedir)/src/main

sourcefiles = $(srcdir)/ckan/streamcatalog/wrappers/BrokerClientWrapper.java

jarfiles = $(libdir)/axiom-1.2.11.wso2v4.jar:$(libdir)/axiom-api-1.2.11.wso2v4.jar:$(libdir)/axiom-impl-1.2.11.wso2v4.jar:$(libdir)/commons-logging-1.1.1.jar:$(libdir)/log4j-1.2.17.jar:$(libdir)/axis2-1.6.1.wso2v10.jar:$(libdir)/org.wso2.carbon.event.client-common-4.2.0.jar:$(libdir)/org.wso2.carbon.event.client-stub-4.2.0.jar:$(libdir)/org.wso2.carbon.event.client-4.2.0.jar:$(libdir)/org.wso2.carbon.core-4.2.0.jar:$(libdir)/py4j-0.8.1.jar

classfiles  = $(sourcefiles:.java=.class)

all: $(classfiles)
%.class: %.java
	javac -d . -classpath .:$(libdir)/* $<

clean:
	rm -f *.class