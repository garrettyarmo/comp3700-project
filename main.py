from objects.controller import Controller
from objects.console_view import ConsoleView
from objects.data_provider_JSON import DataProviderJSON

data_provider = DataProviderJSON("users.json", "companies.json")
controller = Controller(data_provider)
view = ConsoleView(controller)
view.run()