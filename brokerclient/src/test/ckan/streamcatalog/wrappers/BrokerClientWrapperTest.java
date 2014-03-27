package ckan.streamcatalog.wrappers;

import java.io.IOException;
import java.util.TreeMap;

import org.apache.commons.lang.RandomStringUtils;
import org.apache.log4j.Logger;
import org.wso2.carbon.event.client.broker.BrokerClientException;
import org.wso2.carbon.event.client.stub.generated.SubscriptionDetails;
import org.wso2.carbon.event.client.stub.generated.authentication.AuthenticationExceptionException;

public class BrokerClientWrapperTest {
	static private int NUMBER_TOPICS = 5;
	static private int NUMBER_SUBS = 10;
	static private int ID_LENGTH = 30;

	static private BrokerClientWrapper wrapper;
	static final Logger logger = Logger.getLogger(BrokerClientWrapperTest.class.getName());

	public static void main(String[] args) {
		String topicID;
		String suID;

		try {
			wrapper = new BrokerClientWrapper();

			// Storing each topic as a tree map key and a list for subscription IDs
			TreeMap<String, String> topicSubs = new TreeMap<>();

			for (int i = 0; i < NUMBER_TOPICS; i++) {

				// First subscription creates the topic
				topicID = RandomStringUtils.randomAlphanumeric(ID_LENGTH);
				suID = wrapper.subscribe(topicID, "http://www.url" + i + "plus" + 0 + ".com/test/");
				topicSubs.put(topicID, suID);

				for (int j = 1; j < NUMBER_SUBS; j++) {
					suID = wrapper.subscribe(topicID, "http://www.url" + i + "plus" + j + ".com/test/");
					topicSubs.put(topicID, suID);
				}
			}

			// Create new connection and unsubscribe everything
			wrapper = new BrokerClientWrapper();

			for (SubscriptionDetails entry : wrapper.getAllSubscriptions()) {
				wrapper.unsubscribe(entry.getSubscriptionId());
			}

		} catch (IOException | AuthenticationExceptionException | BrokerClientException err) {
			logger.error(err);
			System.exit(1);
		}
	}
}