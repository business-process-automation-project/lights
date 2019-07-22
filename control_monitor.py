import os
import re
import paho.mqtt.client as mqtt # import the client1
import time
import requests
import configparser
import json
import fileinput


config = configparser.ConfigParser()
config.read('config.ini')
config.sections()
mqtt_broker = config['MONITOR']['mqtt_broker']
mqtt_topic1 = config['MONITOR']['mqtt_topic']
mqtt_topic2 = config['LIGHTS']['mqtt_topic']
monitor1_f = config['MONITOR']['monitor1']
monitor2_f = config['MONITOR']['monitor2']
monitor3_f = config['MONITOR']['monitor3']
default_f = config['MONITOR']['default']


def on_message(client, userdata, message):
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)

    if message.topic == mqtt_topic1:
        content = json.loads(str(message.payload.decode("utf-8")))

        qst = content["question"]
        ans1 = content["answer1"]
        ans2 = content["answer2"]
        ans3 = content["answer3"]

        monitor1_html = re.sub('<!--QUESTION-->', qst, default_html)
        monitor1_html = re.sub('<!--ID-->', '1', monitor1_html)
        monitor1_html = re.sub('<!--ANSWER-->', ans1, monitor1_html)

        monitor2_html = re.sub('<!--QUESTION-->', qst, default_html)
        monitor2_html = re.sub('<!--ID-->', '2', monitor2_html)
        monitor2_html = re.sub('<!--ANSWER-->', ans2, monitor2_html)

        monitor3_html = re.sub('<!--QUESTION-->', qst, default_html)
        monitor3_html = re.sub('<!--ID-->', '3', monitor3_html)
        monitor3_html = re.sub('<!--ANSWER-->', ans3, monitor3_html)

        with open(monitor1_f, 'w') as file:
            file.write(monitor1_html)
        with open(monitor2_f, 'w') as file:
            file.write(monitor2_html)
        with open(monitor3_f, 'w') as file:
            file.write(monitor3_html)

    if message.topic == mqtt_topic2:
        if str(message.payload.decode("utf-8")) == "Answer1":
            print("test")
            with open(monitor1_f, 'r') as file:
                monitor1_html = file.read().replace('\n', '')
                monitor1_html = re.sub('<!--COLOR-->', 'color:green !important;', monitor1_html)
                monitor1_html = re.sub('<!--BCOLOR-->', 'border-color:green !important;', monitor1_html)
            with open(monitor1_f, 'w') as file:
                file.write(monitor1_html)
        if str(message.payload.decode("utf-8")) == "Answer2":
            with open(monitor2_f, 'r') as file:
                monitor2_html = file.read().replace('\n', '')
                monitor2_html = re.sub('<!--COLOR-->', 'color:green !important;', monitor2_html)
                monitor2_html = re.sub('<!--BCOLOR-->', 'border-color:green !important;', monitor2_html)
            with open(monitor2_f, 'w') as file:
                file.write(monitor2_html)
        if str(message.payload.decode("utf-8")) == "Answer3":
            with open(monitor3_f, 'r') as file:
                monitor3_html = file.read().replace('\n', '')
                monitor3_html = re.sub('<!--COLOR-->', 'color:green !important;', monitor3_html)
                monitor3_html = re.sub('<!--BCOLOR-->', 'border-color:green !important;', monitor3_html)
            with open(monitor3_f, 'w') as file:
                file.write(monitor3_html)
        if str(message.payload.decode("utf-8")) == "DefaultLight":
            monitor1_html = default_html
            monitor2_html = default_html
            monitor3_html = default_html

            with open(monitor1_f, 'w') as file:
                file.write(monitor1_html)
            with open(monitor2_f, 'w') as file:
                file.write(monitor2_html)
            with open(monitor3_f, 'w') as file:
                file.write(monitor3_html)


with open(default_f, 'r') as file:
    default_html = file.read().replace('\n', '')

with open(monitor1_f, 'w') as file:
    file.write(default_html)
with open(monitor2_f, 'w') as file:
    file.write(default_html)
with open(monitor3_f, 'w') as file:
    file.write(default_html)

print("creating new instance")
client = mqtt.Client("monitor_control")       # create new instance
client.on_message = on_message              # attach function to callback
print("connecting to broker")
client.connect(mqtt_broker)                 # connect to broker
client.loop_start()                         # start the loop
print("Subscribing to topics", mqtt_topic1, mqtt_topic2)
client.subscribe(mqtt_topic1)
client.subscribe(mqtt_topic2)
# print("Publishing message to topic", "house/bulbs/bulb1")
# client.publish("house/bulbs/bulb1", "OFF")
while True:
    time.sleep(10)           # wait
    print("running...")
client.loop_stop()                          # stop the loop
client.disconnect()                         # disconnect
