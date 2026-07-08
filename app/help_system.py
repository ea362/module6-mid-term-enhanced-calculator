class HelpProvider:
    def get_help(self):
        raise NotImplementedError # pragma: no cover


class BaseHelpProvider(HelpProvider):
    def get_help(self):
        return {
            "add": "Add two numbers",
            "subtract": "Subtract two numbers",
            "multiply": "Multiply two numbers",
            "divide": "Divide two numbers",
        }


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


class REPLHelpDecorator(HelpProvider):
    def __init__(self, provider):
        self.provider = provider

    def get_help(self):
        help_dict = self.provider.get_help()
        help_dict.update({
            "history": "Show calculation history",
            "clear": "Clear calculation history",
            "undo": "Undo last calculation",
            "redo": "Redo last undone calculation",
            "save": "Save history to file",
            "load": "Load history from file",
            "filter": "Filter history by operation",
            "export_csv": "Export filtered history to CSV",
            "export_excel": "Export filtered history to Excel",
            "analytics": "Show analytics summary of history",
            "exit": "Exit the calculator",
        })
        return help_dict
