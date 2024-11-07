from shared.utils import garbage_cleaner
from storage import contacts, exceptions
from models import Record, Phone

def phone_handler(func):
    def inner(*args, **kwargs):
        err_test_cases = [
            (lambda: not args, ('LACK_OF_ARGUMENTS', exceptions['LACK_OF_ARGUMENTS'])),
            (lambda: not args[0], ('LACK_OF_ARGUMENTS', exceptions['LACK_OF_ARGUMENTS'])),
            (lambda: not len(contacts.data), ('LACK_OF_RECORDS', exceptions['LACK_OF_RECORDS'])),
            (lambda: args[0] and args[0][0] not in contacts.data.keys(), ('LACK_OF_DATA', exceptions['LACK_OF_DATA'])),
        ]

        for condition, message in err_test_cases:
            if condition():
                print(message)
                return

        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(('Unexpected error', exceptions['Any other exception']))
            print(f"Error details: {str(e)}")

    return inner

def edit_handler(func):
    def inner(*args, **kwargs):
        err_test_cases = [
            (lambda: not args or not args[0], ('LACK_OF_ARGUMENTS', exceptions['LACK_OF_ARGUMENTS'])),
            (lambda: len(args[0]) != 2, ('LACK_OF_ARGUMENTS', exceptions['LACK_OF_ARGUMENTS'])),
        ]

        for condition, message in err_test_cases:
            if condition():
                print(message)
                return

        try:
            name, number = args[0]
            cleaned_number = garbage_cleaner(number)

            if name not in contacts.data:
                record = Record(name)
                record.add_phone(cleaned_number)
                contacts.add_record(record)
            else:
                record = contacts.find(name)
                if record.phones:
                    record.edit_phone(record.phones[0].value, cleaned_number)
                else:
                    record.add_phone(cleaned_number)

            return func(*args, **kwargs)
        except ValueError as e:
            print(('INVALID_NUMBER', exceptions['INVALID_NUMBER']))
        except Exception as e:
            print(('Unexpected error', exceptions['Any other exception']))
            print(f"Error details: {str(e)}")

    return inner