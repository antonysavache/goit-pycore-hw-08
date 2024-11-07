from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not self.validate_phone(value):
            raise ValueError("Phone number must be 10 digits")
        super().__init__(value)

    @staticmethod
    def validate_phone(phone):
        return len(str(phone)) == 10 and phone.isdigit()

class Birthday(Field):
    def __init__(self, value):
        try:
            # Convert string to datetime object
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        if not isinstance(phone, Phone):
            phone = Phone(phone)
        self.phones.append(phone)

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if str(p) != str(phone)]

    def edit_phone(self, old_phone, new_phone):
        if not Phone.validate_phone(new_phone):
            raise ValueError("New phone number is not valid")

        for i, phone in enumerate(self.phones):
            if str(phone) == str(old_phone):
                self.phones[i] = Phone(new_phone)
                return
        raise ValueError("Phone number not found")

    def find_phone(self, phone):
        for p in self.phones:
            if str(p) == str(phone):
                return p
        return None

    def add_birthday(self, birthday):
        if not isinstance(birthday, Birthday):
            birthday = Birthday(birthday)
        self.birthday = birthday

    def __str__(self):
        birthday_str = f", birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}{birthday_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        if not isinstance(record, Record):
            raise ValueError("Can only add Record instances")
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.now().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                birthday_this_year = datetime(
                    today.year,
                    record.birthday.value.month,
                    record.birthday.value.day
                ).date()

                if birthday_this_year < today:
                    birthday_this_year = datetime(
                        today.year + 1,
                        record.birthday.value.month,
                        record.birthday.value.day
                    ).date()

                days_until_birthday = (birthday_this_year - today).days

                if days_until_birthday <= 7:
                    # If birthday falls on a weekend, congratulate on Monday
                    congratulation_date = birthday_this_year
                    if congratulation_date.weekday() >= 5:  # Saturday or Sunday
                        days_to_add = (7 - congratulation_date.weekday() + 1) % 7
                        congratulation_date += timedelta(days=days_to_add)

                    upcoming_birthdays.append({
                        "name": record.name.value,
                        "birthday": record.birthday.value.strftime("%d.%m.%Y"),
                        "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
                    })

        return upcoming_birthdays