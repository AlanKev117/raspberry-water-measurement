import os
import json
import time
import logging

import requests

logging.basicConfig(level=logging.INFO)

# Read variables from service environment.
local_sensor_endpoint = os.getenv("LOCAL_SENSOR_ENDPOINT")
aws_iot_host = os.getenv("AWS_IOT_HOST")
aws_iot_topic = os.getenv("AWS_IOT_TOPIC")
aws_iot_cert = os.getenv("AWS_IOT_CERT")
aws_iot_key = os.getenv("AWS_IOT_KEY")

# Assert there are no missing variables.
assert local_sensor_endpoint is not None, "Missing sensor endpoint"
assert aws_iot_host is not None, "Missing AWS IoT host"
assert aws_iot_topic is not None, "Missing AWS IoT topic"
assert aws_iot_cert is not None, "Missing AWS IoT cert"
assert aws_iot_key is not None, "Missing AWS IoT key"

# Runtime variables.
aws_iot_endpoint = f'https://{aws_iot_host}:8443/topics/{aws_iot_topic}?qos=1'
week_seconds = 60 * 60 * 24 * 7
credentials = [aws_iot_cert, aws_iot_key]

def read_sensor():
  # Read data from sensor
  sensor_response = requests.get(local_sensor_endpoint)
  status_code = sensor_response.status_code
  
  # Assert response was successful
  if status_code != 200:
    raise Exception(f"Sensor response was unsuccessful: {status_code}")
  
  # Parse json response
  payload = sensor_response.json()
  level = payload["level"]

  # Assert body has a valid value
  if level in (None, "null"):
    raise Exception(f"Sensor measurement invalid: {level}")
  
  return level

def create_message(level):
  # Create message for IoT topic
  data = {
    "level": level,
    "expiration_time": int(time.time()) + week_seconds
  }
  message = json.dumps(data)
  return message

def publish_message(message):
  # Try to publish message
  response = requests.post(aws_iot_endpoint, data=message, cert=credentials)
  status_code = response.status_code
  
  # Raise error if response was unsuccessful
  if status_code != 200:
    raise Exception(f"Error publishing message. Status code: {status_code}, response: {response.text}")
  
while True:
  
  try:
    level = read_sensor()
    message = create_message(level)
    publish_message(message)
    print(f"Water level published to IoT: {level}")
    logging.info(f"Water level published to IoT: {level}")
  except Exception as e:
    print(f"An error ocurred: {e}")
    logging.error(f"An error ocurred: {e}")
  
  time.sleep(10)
