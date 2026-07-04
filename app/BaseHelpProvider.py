from app.help_system import HelpProvider

class ExtendedHelpDecorator(HelpProvider):
    def __init__(self, provider):
        self.provider = provider

    def get_help(self):
        help_dict = self.provider.get_help()
        help_dict.update({
            "power": "Raise a number to a power",
            "root": "Compute a square root",
            "modulus": "Compute a modulus",
            "int_divide": "Integer division",
            "percent": "Percentage calculation",
            "abs_diff": "Absolute difference",
        })
        return help_dict
