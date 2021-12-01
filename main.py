from objects.company import Company, viewPublicCompanies
from objects.user import User

data_provider = DataProviderJSON("users.json", "companies.json")
controller = Controller(data_provider)
view = ConsoleView(controller)
view.run()