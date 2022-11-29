from evdev import InputDevice, categorize, ecodes
from gamepad_config import get_gamepad_config

mapper = get_gamepad_config("bitdo")

gamepad = InputDevice('/dev/input/event13')

print(gamepad)

for event in gamepad.read_loop():
    if event.type != 4 and event.type != 0:
        button_name = mapper.get_button_name(event.type, event.code)
        status      = mapper.get_button_state(event.type, event.code, event.value)

        print(f"{button_name}: {status}")