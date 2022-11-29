import enum
class ContinuousGamepadButton:
    def __init__(self, button_name, value):
        self.button_name = button_name #string
        self.value = value #int32

    def to_dict(self):
        ret = dict()
        ret['button_name'] = self.button_name
        ret['value'] = self.value
        return ret

    def get_topic(self):
        return 'gamepad/continuous'

class DiscreteGamepadButton:
    def __init__(self, button_name, value):
        self.button_name = button_name #string
        self.value = value #string

    def to_dict(self):
        ret = dict()
        ret['button_name'] = self.button_name
        ret['value'] = self.value
        return ret

    def get_topic(self):
        return 'gamepad/discrete'

