from models import AddressBook, Record


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Please provide all required arguments"
        except KeyError:
            return "Contact not found"
        except Exception as e:
            return f"An error occurred: {e}"
    return wrapper

@input_error
def add_contact(args, book: AddressBook):
    print(f"Received args: {args}")

    if len(args) != 2:
        raise ValueError("Give me name and phone please")

    name, phone = args[0], args[1]
    record = book.find(name)

    if record is None:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return "Contact added."
    else:
        record.add_phone(phone)
        return "Contact updated."

@input_error
def add_birthday(args, book: AddressBook):
    if len(args) != 2:
        raise ValueError("Give me name and birthday (DD.MM.YYYY) please")

    name, birthday = args
    record = book.find(name)

    if record is None:
        raise KeyError(f"Contact {name} not found")

    record.add_birthday(birthday)
    return f"Birthday added for {name}"

@input_error
def show_birthday(args, book: AddressBook):
    if len(args) != 1:
        raise ValueError("Give me name please")

    name = args[0]
    record = book.find(name)

    if record is None:
        raise KeyError(f"Contact {name} not found")

    if record.birthday is None:
        return f"No birthday set for {name}"

    return f"{name}'s birthday: {record.birthday}"

@input_error
def birthdays(args, book: AddressBook):
    upcoming = book.get_upcoming_birthdays()

    if not upcoming:
        return "No upcoming birthdays in the next week"

    result = "Upcoming birthdays:\n"
    for item in upcoming:
        result += f"{item['name']}: Birthday on {item['birthday']}, celebrate on {item['congratulation_date']}\n"
    return result.strip()

@input_error
def change_contact(args, book: AddressBook):
    if len(args) != 3:
        raise ValueError("Give me name, old phone and new phone please")

    name, old_phone, new_phone = args
    record = book.find(name)

    if record is None:
        raise KeyError(f"Contact {name} not found")

    record.edit_phone(old_phone, new_phone)
    return f"Phone number updated for {name}"

@input_error
def show_phone(args, book: AddressBook):
    if len(args) != 1:
        raise ValueError("Give me name please")

    name = args[0]
    record = book.find(name)

    if record is None:
        raise KeyError(f"Contact {name} not found")

    phones_info = f"Phones: {'; '.join(str(phone) for phone in record.phones)}" if record.phones else "No phones"
    birthday_info = f", Birthday: {record.birthday}" if record.birthday else ""

    return f"{name}: {phones_info}{birthday_info}"

@input_error
def show_all(book: AddressBook):
    if not book.data:
        return "No contacts saved"

    return '\n'.join(str(record) for record in book.data.values())

def show_help():
    commands = {
        "hello": "Show welcome message",
        "add [name] [phone]": "Add new contact or phone to existing contact",
        "change [name] [old_phone] [new_phone]": "Change existing contact's phone",
        "phone [name]": "Show contact's phones",
        "all": "Show all contacts",
        "add-birthday [name] [dd.mm.yyyy]": "Add birthday to contact",
        "show-birthday [name]": "Show contact's birthday",
        "birthdays": "Show upcoming birthdays",
        "close or exit": "Close the program"
    }

    result = "Available commands:\n"
    for command, description in commands.items():
        result += f"{command:40} - {description}\n"
    return result

def parse_input(user_input):
    try:
        cmd, *args = user_input.strip().split()
        print(f"Command: {cmd}, Args: {args}")
        return cmd.lower(), args
    except ValueError:
        return "help", []


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    print("Type 'help' to see available commands")

    commands = {
        "hello": lambda args: "How can I help you?",
        "add": lambda args: add_contact(args, book),
        "change": lambda args: change_contact(args, book),
        "phone": lambda args: show_phone(args, book),
        "all": lambda args: show_all(book),
        "add-birthday": lambda args: add_birthday(args, book),
        "show-birthday": lambda args: show_birthday(args, book),
        "birthdays": lambda args: birthdays(args, book),
        "help": lambda args: show_help(),
    }

    while True:
        try:
            user_input = input("\nEnter a command: ")
            command, args = parse_input(user_input)

            if command in ["close", "exit"]:
                print("Good bye!")
                break

            if command in commands:
                result = commands[command](args)
                print(result)
            else:
                print("Invalid command. Type 'help' to see available commands.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()