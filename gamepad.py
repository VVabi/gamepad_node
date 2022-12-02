from evdev import InputDevice, categorize, ecodes
from gamepad_config import get_gamepad_config
from protocol.gamepad_node_messages import *
import paho.mqtt.client as mqtt
import json

mapper = get_gamepad_config("bitdo")

gamepad = InputDevice('/dev/input/event17')

client = mqtt.Client()
client.connect("localhost", 1883, 60)
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