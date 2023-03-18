from evdev import InputDevice, categorize, ecodes, evtest
from gamepad_config import get_gamepad_config
from protocol.gamepad_node_messages import *
import paho.mqtt.client as mqtt
import json
import os
import time

evtest.list_devices()

mapper = get_gamepad_config("bitdo")
found = False
while not found:
    print("Waiting for gamepad...")
    for num in range(100):

        input_device_path = f'/dev/input/event{num}'
        try:
            gamepad = InputDevice(input_device_path)
            print(gamepad.name)
            if gamepad.name == "8BitDo Pro 2" or gamepad.name == "Microsoft X-Box 360 pad":
                found = True
                break
        except:
            pass

    time.sleep(1)

print("Found gamepad")
client = mqtt.Client()
client.connect("localhost", 1883, 60)
client.loop_start()

for event in gamepad.read_loop():
    print(event)
    if mapper.type_is_mapped(event.type):
        button_name = mapper.get_button_name(event.type, event.code)
        if button_name is None:
            continue
        status      = mapper.get_button_state(event.type, event.code, event.value)
        button_type = mapper.get_button_type(event.type, event.code)
        if button_type == "continuous":
            message = ContinuousGamepadButton(button_name, status)
        else:
            message = DiscreteGamepadButton(button_name, status)
        client.publish(message.get_topic(), json.dumps(message.to_dict()))
    else:
        print("WTF")