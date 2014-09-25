package ckan.streamcatalog.wrappers;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.rmi.RemoteException;
import java.util.Properties;

import javax.xml.namespace.QName;

import org.apache.axis2.AxisFault;
import org.apache.log4j.Logger;
import org.apache.axiom.om.OMAbstractFactory;
import org.apache.axiom.om.OMElement;
import org.apache.axiom.om.OMFactory;
import org.wso2.carbon.event.client.broker.BrokerClient;
import org.wso2.carbon.event.client.broker.BrokerClientException;
import org.wso2.carbon.event.client.stub.generated.SubscriptionDetails;
import org.wso2.carbon.event.client.stub.generated.authentication.AuthenticationExceptionException;

import py4j.GatewayServer;

import java.lang.reflect.Field;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;


public class BrokerClientWrapper {
	static final Logger logger = Logger.getLogger(BrokerClientWrapper.class.getName());
	static final String PROPERTIES_FILE = "brokerclient.properties";
	private BrokerClient brokerClient;
	Properties properties;

	public BrokerClientWrapper() throws IOException, AuthenticationExceptionException {

		try {
			InputStream in = new FileInputStream(PROPERTIES_FILE);
			properties = new Properties();
			properties.load(in);

			logger.info("Properties file succesfully loaded");

			// Enabling SSL connection to WSO2 ESB
			System.setProperty("javax.net.ssl.trustStore", properties.getProperty("ESB.TrustStore"));
			System.setProperty("javax.net.ssl.trustStorePassword", properties.getProperty("ESB.TrustStorePassword"));

		} catch (IOException err) {
			logger.error(err);
			throw err;
		}
	}

	public Boolean createTopic(String topicID) throws RemoteException, BrokerClientException, AuthenticationExceptionException {
		try {
			String suID = subscribe(topicID, "/dev/null");
			return unsubscribe(suID);
		} catch (RemoteException | BrokerClientException | AuthenticationExceptionException err) {
			logger.error(err);
			throw err;
		}
	}

	public String subscribe(String topicID, String eventSinkUrl) throws BrokerClientException, AuthenticationExceptionException, AxisFault {
		try {
			brokerClient = new BrokerClient(properties.getProperty("ESB.Url"), properties.getProperty("ESB.User.ID"),
			      properties.getProperty("ESB.Password"));
			String suID = brokerClient.subscribe(topicID, eventSinkUrl);
			logger.info("Creating - Subscription: " + suID + " Topic: " + topicID + " URL: " + eventSinkUrl);
			return suID;

		} catch (BrokerClientException | AxisFault | AuthenticationExceptionException err) {
			logger.error(err);
			throw err;
		}
	}

	public boolean unsubscribe(String suID) throws RemoteException, AuthenticationExceptionException {
		try {
			brokerClient = new BrokerClient(properties.getProperty("ESB.Url"), properties.getProperty("ESB.User.ID"),
			      properties.getProperty("ESB.Password"));
			brokerClient.unsubscribe(suID);
			logger.info("Unsubscribing ID: " + suID);
			return true;
		} catch (RemoteException | AuthenticationExceptionException err) {
			logger.error(err);
			throw err;
		}
	}

	// Circumvented problems with returning Java objects using JSON.
	public String getAllSubscriptions() throws RemoteException, AuthenticationExceptionException {
		try {
			brokerClient = new BrokerClient(properties.getProperty("ESB.Url"), properties.getProperty("ESB.User.ID"),
			      properties.getProperty("ESB.Password"));
			SubscriptionDetails[] subsriptions = brokerClient.getAllSubscriptions();
			logger.info("Count all subscriptions: " + subsriptions != null ? subsriptions.length : "0");

			Gson gson = new GsonBuilder().setPrettyPrinting().create();
			return gson.toJson(subsriptions);

		} catch (RemoteException | AuthenticationExceptionException err) {
			logger.error(err);
			throw err;
		}
	}

	/**
	 * Publish (send) a message to given WSO2 ESB topic.
	 */
	public boolean publish(String topic, String message) throws RemoteException, AuthenticationExceptionException {
		try {
			brokerClient = new BrokerClient(properties.getProperty("ESB.Url"), properties.getProperty("ESB.User.ID"),
			      properties.getProperty("ESB.Password"));
			OMFactory fac = OMAbstractFactory.getOMFactory();
			OMElement ele = fac.createOMElement(new QName("http://wso2.org", topic));
			ele.setText(message);
			brokerClient.publish(topic, ele);
			return true;
		} catch (RemoteException | AuthenticationExceptionException err) {
			logger.error(err);
			throw err;
		}
	}

	public static void main(String[] args) {
		try {
			BrokerClientWrapper wrapper = new BrokerClientWrapper();
			logger.info("Py4j Gateway Server started");

			// Start Py4j Gateway
			GatewayServer gatewayServer = new GatewayServer(wrapper);
			gatewayServer.start();

		} catch (IOException | AuthenticationExceptionException error) {
			logger.error(error);
			System.exit(1);
		}
	}
}
