import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("CLIENT_ID")

mqtt_broker = os.getenv('MQTT_BROKER')
mqtt_port = int(os.getenv('MQTT_PORT'))
mqtt_topic = os.getenv("MQTT_TOPIC")


cloud_sync_period = int(os.getenv("Cloud_Sync_Period"))
cloud_mqtt_broker = os.getenv("CLOUD_MQTT_BROKER")
cloud_mqtt_port = int(os.getenv("CLOUD_MQTT_PORT"))
cloud_mqtt_topic = os.getenv("CLOUD_MQTT_TOPIC")

inference_enable = eval(os.getenv("INFERENCE_ENABLE"))
store_enable = eval(os.getenv("STORE_ENABLE"))

outlier_enable = eval(os.getenv("OUTLIER_ENABLE"))
outlier_model_name = os.getenv("OUTLIER_MODEL")
outlier_drop_rate = int(os.getenv("OUTLIER_DROP_RATE"))

reduction_enable = eval(os.getenv("REDUCTION_ENABLE"))
reduction_model = os.getenv('REDUCTION_MODEL')

sliding_window_size = int(os.getenv("SLIDING_WINDOW_SIZE"))

db_url = os.getenv("DB_URL")
collection_name = os.getenv("COLLECTION_NAME")
