from abc import ABC, abstractmethod
from AddressBook import *

class Command(ABC):
    @abstractmethod
    def execute(self, bot):
        pass

class AddCommand(Command):
    def execute(self, bot):
        name = Name(input("Name: ")).value.strip()
        phones = Phone().value
        birth = Birthday().value
        email = Email().value.strip()
        status = Status().value.strip()
        note = Note(input("Note: ")).value
        record = Record(name, phones, birth, email, status, note)
        return bot.book.add(record)

class SearchCommand(Command):
    def execute(self, bot):
        print("There are following categories: \nName \nPhones \nBirthday \nEmail \nStatus \nNote")
        category = input('Search category: ')
        pattern = input('Search pattern: ')
        result = bot.book.search(pattern, category)
        for account in result:
            if account['birthday']:
                birth = account['birthday'].strftime("%d/%m/%Y")
                result = "_" * 50 + "\n" + f"Name: {account['name']} \nPhones: {', '.join(account['phones'])} \nBirthday: {birth} \nEmail: {account['email']} \nStatus: {account['status']} \nNote: {account['note']}\n" + "_" * 50
                print(result)

class EditCommand(Command):
    def execute(self, bot):
        contact_name = input('Contact name: ')
        parameter = input('Which parameter to edit(name, phones, birthday, status, email, note): ').strip()
        new_value = input("New Value: ")
        return bot.book.edit(contact_name, parameter, new_value)

class RemoveCommand(Command):
    def execute(self, bot):
        pattern = input("Remove (contact name or phone): ")
        return bot.book.remove(pattern)

class SaveCommand(Command):
    def execute(self, bot):
        file_name = input("File name: ")
        return bot.book.save(file_name)

class LoadCommand(Command):
    def execute(self, bot):
        file_name = input("File name: ")
        return bot.book.load(file_name)

class CongratulateCommand(Command):
    def execute(self, bot):
        print(bot.book.congratulate())

class ViewCommand(Command):
    def execute(self, bot):
        print(bot.book)

class Bot:
    def __init__(self):
        self.book = AddressBook()
        self.commands = {
            'add': AddCommand(),
            'search': SearchCommand(),
            'edit': EditCommand(),
            'remove': RemoveCommand(),
            'save': SaveCommand(),
            'load': LoadCommand(),
            'congratulate': CongratulateCommand(),
            'view': ViewCommand(),
            'exit': None  # Placeholder for exit command
        }

    def handle(self, action):
        command = self.commands.get(action)
        if command:
            return command.execute(self)
        else:
            print("There is no such command!")