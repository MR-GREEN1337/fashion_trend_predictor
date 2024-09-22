from datetime import timedelta
import os
from loguru import logger

from src.app import get_app

TIME_WINDOW_SIZE = 30

def reduce_data(data, new_data):
    """
    Function to reduce data in a window
    """
    return data + new_data

def init_data():
    """
    Function to initialize data
    """
    return 0

def run():
    """
    Retrieve Data from an API and send it to a Kafka Topic
    """

    app = get_app()

    logger.info("Setting input topic for data_collection service")
    input_topic = app.topic(os.environ["KAFKA_INPUT_TOPIC"])

    logger.info("Setting output topic for data_collection service")
    output_topic = app.topic(os.environ["KAFKA_OUTPUT_TOPIC"])

    # Creating a streaming dataframe receiver
    sdf = app.dataframe(input_topic)

    sdf.tumbling_window(timedelta(seconds=TIME_WINDOW_SIZE)) \
    .reduce(reduce_data, init_data) \
    .final()

    # Play some magic on data before sending to output topic
    #...

    sdf = sdf.to_topic(output_topic)

    # Start the application
    app.run(sdf)

if __name__ == "__main__":
    run()