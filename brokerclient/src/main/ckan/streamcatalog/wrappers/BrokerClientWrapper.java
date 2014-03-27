package ckan.streamcatalog.wrappers;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.rmi.RemoteException;
import java.util.Properties;

import org.apache.log4j.Logger;
import org.wso2.carbon.event.client.broker.BrokerClient;
import org.wso2.carbon.event.client.broker.BrokerClientException;
import org.wso2.carbon.event.client.stub.generated.SubscriptionDetails;
import org.wso2.carbon.event.client.stub.generated.authentication.AuthenticationExceptionException;

import py4j.GatewayServer;

public class BrokerClientWrapper {
	static final Logger logger = Logger.getLogger(BrokerClientWrapper.class.getName());
	static final String PROPERTIES_FILE = "brokerclient.properties";
	private BrokerClient brokerClient;

	public BrokerClientWrapper() throws IOException, AuthenticationExceptionException {
		Properties properties = new Properties();

		try {
			InputStream in = new FileInputStream(PROPERTIES_FILE);
			properties.load(in);

			logger.info("Properties file succesfully loaded");

			// Enabling SSL connection to WSO2 ESB
			System.setProperty("javax.net.ssl.trustStore", properties.getProperty("ESB.TrustStore"));
			System.setProperty("javax.net.ssl.trustStorePassword", properties.getProperty("ESB.TrustStorePassword"));

			brokerClient = new BrokerClient(properties.getProperty("ESB.Url"), properties.getProperty("ESB.User.ID"),
			      properties.getProperty("ESB.Password"));

		} catch (IOException | AuthenticationExceptionException err) {
			logger.error(err);
			throw err;
		}
	}

	public String subscribe(String topicID, String eventSinkUrl) throws BrokerClientException {
		try {
			String suID = brokerClient.subscribe(topicID, eventSinkUrl);
			logger.info("Creating - Subscription: " + suID + " Topic: " + topicID + " URL: " + eventSinkUrl);
			return suID;

		} catch (BrokerClientException err) {
			logger.error(err);
			throw err;
		}
	}

	public boolean unsubscribe(String suID) {
		try {
			brokerClient.unsubscribe(suID);
			logger.info("Unsubscribing ID: " + suID);
			return true;
		} catch (RemoteException err) {
			logger.error(err);
			return false;
		}
	}

	// Note: there might be problems here with Py4j since we are returning java objects 
	public SubscriptionDetails[] getAllSubscriptions() throws RemoteException {
		try {
			SubscriptionDetails[] subsriptions = brokerClient.getAllSubscriptions();
			logger.info("Count all subscriptions: " + subsriptions != null ? subsriptions.length : "0");
			return subsriptions;

		} catch (RemoteException err) {
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
