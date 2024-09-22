import os
from loguru import logger
from quixstreams import Application

def get_app() -> Application:

    logger.info("Creating application...")
    app = Application(
        broker_address=os.environ["KAFKA_BROKER_ADDRESS"],
        consumer_group="json_data_to_features_consumer_group",
        auto_offset_reset="earliest",
        consumer_extra_config={"allow.auto.create.topics": "true"},
        producer_extra_config={"allow.auto.create.topics": "true"},
    )

    return app