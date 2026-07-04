from app.help_system import BaseHelpProvider, ExtendedHelpDecorator, REPLHelpDecorator

def test_dynamic_help_menu():
    provider = REPLHelpDecorator(ExtendedHelpDecorator(BaseHelpProvider()))
    help_dict = provider.get_help()

    assert "add" in help_dict
    assert "power" in help_dict
    assert "analytics" in help_dict
