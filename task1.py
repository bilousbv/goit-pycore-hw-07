import re
from collections import UserDict
from datetime import datetime, timedelta

WEEKDAYS_LENGTH = 5
WEEK_LENGTH = 7
DATE_FORMAT = '%d.%m.%Y'


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            birthday = datetime.strptime(value, DATE_FORMAT).date()
            self.birthday = birthday
            super().__init__(birthday)
        except ValueError:
            raise Exception("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.birthday.strftime(DATE_FORMAT)


class Phone(Field):
    def __init__(self, value):
        if not re.match(r"^\d{10}$", value):
            raise Exception("Phone number must be exactly 10 digits.")
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.__phones = []
        self.__birthday = None

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number):
        phone_to_remove = None
        for phone in self.phones:
            if phone.value == phone_number:
                phone_to_remove = phone
                break
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            print("Phone number not found.")

    def edit_phone(self, old_phone_number, new_phone_number):
        self.remove_phone(old_phone_number)
        self.add_phone(new_phone_number)

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone.value
        return "Phone number not found."

    @property
    def birthday(self):
        return self.__birthday

    @property
    def phones(self):
        return self.__phones

    def add_birthday(self, birthday):
        self.__birthday = Birthday(birthday)

    def __str__(self):
        return (f"Contact name: {self.name.value},"
                f" Phones: {'; '.join(phone.value for phone in self.phones)},"
                f" Birthday: {self.birthday}")


class AddressBook(UserDict):
    def add_record(self, new_record):
        self.data[new_record.name.value] = new_record

    def find(self, record_name):
        return self.data.get(record_name)

    def delete(self, record_name):
        if record_name in self.data:
            del self.data[record_name]
        else:
            print("Contact not found.")

    def get_upcoming_birthdays(self):
        current_date = datetime.today().date()
        current_year = current_date.year
        users_for_congratulation = list()

        try:
            for user_name in self.data:
                user = self.data.get(user_name)
                if user.birthday is None:
                    continue

                user_birthday_date = datetime.strptime(str(user.birthday), DATE_FORMAT).date()
                user_birthday_date_this_year = user_birthday_date.replace(year=current_year)
                delta = user_birthday_date_this_year - current_date

                if delta.days not in range(0, 7):
                    continue

                weekday = user_birthday_date_this_year.weekday()

                if weekday < WEEKDAYS_LENGTH:
                    congratulation_date = user_birthday_date_this_year.strftime(DATE_FORMAT)
                else:
                    congratulation_date = user_birthday_date_this_year + timedelta(days=WEEK_LENGTH - weekday)

                users_for_congratulation.append(f"{user}, Congratulation date: {congratulation_date}")

            return users_for_congratulation
        except Exception as e:
            print(e)


# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
jane_record.add_birthday('13.08.1996')
book.add_record(jane_record)
# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

upcoming_birthdays = book.get_upcoming_birthdays()

print(upcoming_birthdays)
print('Upcoming Birthdays:')
for record in upcoming_birthdays:
    print(record)

# Видалення запису Jane
book.delete("Jane")
