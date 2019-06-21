import paho.mqtt.client as mqtt  # import the client1
import time
import requests
import configparser


config = configparser.ConfigParser()
config.read('config.ini')
config.sections()
mqtt_broker = config['LIGHTS']['mqtt_broker']
mqtt_topic = config['LIGHTS']['mqtt_topic']
lights_raspbee = config['LIGHTS']['lights_raspbee']
lights_apikey = config['LIGHTS']['lights_apikey']
lights_url = 'http://' + lights_raspbee + '/api/' + lights_apikey


def on_message(client, userdata, message):
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)

    if str(message.payload.decode("utf-8")) == "blink":
        requests.put(lights_url + '/groups/1/action', json={"alert": "lselect"})

    if str(message.payload.decode("utf-8")) == "answer1":
        requests.put(lights_url + '/groups/1/action', json={"alert": "none"})
        requests.put(lights_url + '/groups/1/scenes/2/recall', json={})

    if str(message.payload.decode("utf-8")) == "answer2":
        requests.put(lights_url + '/groups/1/action', json={"alert": "none"})
        requests.put(lights_url + '/groups/1/scenes/3/recall', json={})

    if str(message.payload.decode("utf-8")) == "answer3":
        requests.put(lights_url + '/groups/1/action', json={"alert": "none"})
        requests.put(lights_url + '/groups/1/scenes/4/recall', json={})

    if str(message.payload.decode("utf-8")) == "standard":
        requests.put(lights_url + '/groups/1/action', json={"alert": "none"})
        requests.put(lights_url + '/groups/1/scenes/1/recall', json={})


    # requests.put(lights_url + '/lights/1/state', json={'on': True, 'alert': 'none'})
    # #if resp.status_code != 200:
    #     # This means something went wrong.
    #     # raise ApiError('GET /tasks/ {}'.format(resp.status_code))
    # # for todo_item in resp.json():
    #    # print('{} {}'.format(todo_item['id'], todo_item['summary']))
    #
    # print(resp.json())
    # light = resp.json()
    #
    # print(light['1'])
    # print('ID der LED: ' + light['1']['name'])


requests.put(lights_url + '/groups/1/scenes/1/recall', json={})

print("creating new instance")
client = mqtt.Client("light_control")       # create new instance
client.on_message = on_message              # attach function to callback
print("connecting to broker")
client.connect(mqtt_broker)                 # connect to broker
client.loop_start()                         # start the loop
print("Subscribing to topic", mqtt_topic)
client.subscribe(mqtt_topic)
# print("Publishing message to topic", "house/bulbs/bulb1")
# client.publish("house/bulbs/bulb1", "OFF")
while True:
    time.sleep(10)           # wait
    print("running...")
client.loop_stop()                          # stop the loop
client.disconnect()                         # disconnect
