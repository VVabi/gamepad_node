import toml

class GamepadMapper():
    def __init__(self, config_dict):
        self.config = config_dict

        self.string_mappings = {}
        self.string_mappings["buttons"] = {}
        for key in self.config["buttons"]:
            self.string_mappings["buttons"][key] = {v:k for k,v in self.config["buttons"][key].items()}

        self.string_mappings["values"] = {}
        for key in self.config["values"]:
            self.string_mappings["values"][key] = {}
            if "mapping" in self.config["values"][key]:
                self.string_mappings["values"][key]["mapping"] = {v:k for k,v in self.config["values"][key]["mapping"] .items()}

    def get_button_name(self, type, code):
        return self.string_mappings["buttons"][str(type)][code]

    def get_button_state(self, type, code, value):
        button_name = self.get_button_name(type, code)
        mapping = self.string_mappings["values"]["default"]
        if button_name in self.config["values"]:
            mapping = self.string_mappings["values"][button_name]
        if "mapping" in mapping:
            return mapping["mapping"][value]
        return value

    def type_is_mapped(self, type):
        return str(type) in  self.string_mappings["buttons"]

    def get_button_type(self, type, code):
        button_name = self.get_button_name(type, code)
        if button_name in self.config["values"]:
            return self.config["values"][button_name]["button_type"]
        return self.config["values"]["default"]["button_type"]

def get_gamepad_config(gamepad_name):
    config_file = gamepad_name+"_gamepad.toml"

    with open(config_file) as fh:
        config_dict = toml.load(fh)

    mapper = GamepadMapper(config_dict)
    return mapper