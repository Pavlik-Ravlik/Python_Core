from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    pass


class Record:
    def __init__(self, name: Name, phone: Phone):
        self.name = name
        self.phone = phone
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(phone)

    def edit_phone(self, phone):
        self.phones[phone] = phone

    def remove_phone(self, phone):
        del self.phones[phone]


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record


# Створення запису
name = Name('Pasha')
phone_1 = Phone('380933431170')
phone_2 = Phone('380989116179')
record_1 = Record(name, Phone)
record_1.add_phone(phone_1)
record_1.add_phone(phone_2)

# Створення адресної книги
address_book = AddressBook()

# Додавання запису в адресну книгу
address_book.add_record(record_1)

# Пошук записів в адресній книзі на ім'я
search_result = address_book.data.get("Pasha")
if search_result:
    for phone in search_result.phones:
        print(f'{search_result.name.value}:{phone.value}')
