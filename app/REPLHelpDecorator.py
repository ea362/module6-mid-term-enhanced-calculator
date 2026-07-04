from app.help_system import HelpProvider

class REPLHelpDecorator(HelpProvider):
    def __init__(self, provider):
        self.provider = provider

    def get_help(self):
        help_dict = self.provider.get_help()
        help_dict.update({
            "history": "Show calculation history",
            "undo": "Undo last calculation",
            "redo": "Redo last undone calculation",
            "filter": "Filter history",
            "export_csv": "Export filtered history to CSV",
            "export_excel": "Export filtered history to Excel",
            "analytics": "Show summary statistics",
            "save": "Save history",
            "load": "Load history",
            "exit": "Exit the calculator",
        })
        return help_dict
