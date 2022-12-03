from evdev import InputDevice, categorize, ecodes
from gamepad_config import get_gamepad_config
from protocol.gamepad_node_messages import *
import paho.mqtt.client as mqtt
import json
import os
import time

mapper = get_gamepad_config("bitdo")

input_device_path = '/dev/input/event1'
while not os.path.exists(input_device_path):
    time.sleep(1)

gamepad = InputDevice(input_device_path)

client = mqtt.Client()
client.connect("10.0.0.36", 1883, 60)
client.loop_start()

for event in gamepad.read_loop():
    if mapper.type_is_mapped(event.type):
        button_name = mapper.get_button_name(event.type, event.code)
        status      = mapper.get_button_state(event.type, event.code, event.value)
        button_type = mapper.get_button_type(event.type, event.code)
        if button_type == "continuous":
            message = ContinuousGamepadButton(button_name, status)
        else:
            message = DiscreteGamepadButton(button_name, status)
        client.publish(message.get_topic(), json.dumps(message.to_dict()))
