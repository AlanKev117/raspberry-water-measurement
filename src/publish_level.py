import os
import json
import time

import requests

http_endpoint = os.getenv("HTTP_ENDPOINT", None)
iot_endpoint = os.getenv("IOT_ENDPOINT", None)
topic = os.getenv("TOPIC", None)
cert = os.getenv("CERT", None)
key = os.getenv("KEY", None)

vars = [http_endpoint, iot_endpoint, topic, cert, key]

assert None not in vars, "ERROR: There is at least one variable missing for the level publisher!"

# create and format values for HTTPS request
publish_url = 'https://' + iot_endpoint + ':8443/topics/' + topic + '?qos=1'

week_seconds = 60 * 60 * 24 * 7

while True:

  try:
    measure_response = requests.get(http_endpoint)
    assert measure_response.status_code == 200
    level = measure_response.json()["level"]
  except:
    print("Error reading from sensor microservice!")
    continue

  try:
    data = {
      "level": level,
      "expiration_time": int(time.time()) + week_seconds
    }
    publish_msg = json.dumps(data)

    # Publish measurement
    publish = requests.request('POST',
      publish_url,
      data=publish_msg,
      cert=[cert, key])

    print("Response status: ", str(publish.status_code))

  except:
    print("Error sending message to topic!")
    continue

  # Wait 10 seconds until next iteration.
  time.sleep(10)
