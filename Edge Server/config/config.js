const path = require('path');
const dotenv = require('dotenv').config({ path: './config/.env' });
if (dotenv.error) {
    throw dotenv.error
  }


module.exports = {
  http: process.env.HTTP, 
  http_port: process.env.HTTP_PORT,
  https_port: process.env.HTTPS_PORT,
  mqtt_broker: process.env.MQTT_BROKER,
  mqtt_port: process.env.MQTT_PORT,
  mqtt_backend: process.env.MQTT_BACKEND,
  mqtt_backend_url: process.env.MQTT_BACKEND_URL,
  host_ip: process.env.HOST_IP,
  host_name: process.env.HOST_NAME,
  cloud_server: process.env.CLOUD_SERVER,
  edge_server: process.env.EDGE_SERVER,
  rp_id: process.env.RP_ID,
  pk_path: path.resolve(process.env.PK_PATH),
  cert_path: path.resolve(process.env.CERT_PATH),
  database: process.env.DATABASE,
  db_url: process.env.DB_URL,
  collection_name: process.env.COLLECTION_NAME,
  redis_url: process.env.REDIS_URL,
};
