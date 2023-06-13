from collections import UserDict
from datetime import date, datetime


class Field:
    def __init__(self, value) -> None:
        self.__value = value

    def __str__(self) -> str:
        return f"{self.__value}"

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Name(Field):
    def __init__(self, name) -> None:
        self.value = name

    def __repr__(self) -> str:
        return f"Name(value={self.value})"

    @property
    def value(self):
        return super().value

    @value.setter
    def value(self, name: str):
        if not name.isalpha():
            raise ValueError
        super(Name, Name).value.fset(self, name)


class Phone(Field):
    def __init__(self, value) -> None:
        super().__init__(value)

    def __repr__(self) -> str:
        return f"Phone(value={self.value})"


class Birthday:
    def __init__(self, day=None, month=None):
        self.day = day
        self.month = month

    def set_value(self, value):
        try:
            datetime.strptime(value, '%y-%m-%d')
        except ValueError:
            raise ValueError('Should be YYYY-MM-DD')
        self.value = value

    def next_birthday(self):
        today = date.today()
        next_birthday = date(today.year, self.month, self.day)
        if next_birthday < today:
            next_birthday = date(today.year+1, self.month, self.day)
        return next_birthday

    def days_to_birthday(self):
        next_birthday = self.next_birthday()
        days_to_birthday = (next_birthday - date.today()).days
        return days_to_birthday


class Record:
    def __init__(
        self,
        name: Name,
        phone: Phone | str | None = None,
    ):
        self.name = name
        self.phones = []
        if phone is not None:
            self.add_phone(phone)

    def days_to_birthday(self):
        return self.days_to_birthday()

    def add_phone(self, phone: Phone | str):
        if isinstance(phone, str):
            phone = self.create_phone(phone)
        self.phones.append(phone)

    def create_phone(self, phone: str):
        return Phone(phone)

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                return p.value

    def remove_phone(self, phone):
        for p in self.phones:
            if p == phone:
                self.phones.remove(p)
                return True
        return False


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name] = record

    def search(self, search_str):
        results = []
        for record in self.data.values():
            if search_str.lower() in record.name.value.lower():
                results.append(record)
            else:
                for phone in record.phones:
                    if search_str in phone.value:
                        results.append(record)
                        break
        return results

    def __iter__(self):
        self.iter_index = 0
        self.n = 5
        self.iter_keys = list(self.data.keys())
        return self

    def __next__(self):
        if self.iter_index < len(self.iter_keys):
            records = []
            for key in self.iter_keys[self.iter_index:min(self.iter_index+self.n, len(self.iter_keys))]:
                records.append(
                    f"{self.data[key].name}: {', '.join([phone.value for phone in self.data[key].phones])}")
            self.iter_index += self.n
            return "\n".join(records)
        raise StopIteration


def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except (KeyError, ValueError, IndexError) as f:
            return str(f)
    return inner


@input_error
def normalise(number):
    new_phone = (
        number.strip()
        .removeprefix("+")
        .replace("(", "")
        .replace(")", "")
        .replace("-", "")
        .replace(" ", "")
    )
    return new_phone


@input_error
def handle_hello():
    return 'How can I help you?\n add - the bot saves in memory a new contact\n change - the bot saves a new phone number for an existing contact in memory\n phone - the bot outputs the phone number for the specified contact to the console.\n show all - By this command, the bot displays all saved contacts with phone numbers to the console.\n good bye, close, exit - on any of these commands, the bot completes its robot after'


@input_error
def handler_add(name, phone, address_book):
    phone = normalise(phone)
    if len(name) == 0 or name.isdigit() or len(phone) < 12 or phone.isalpha():
        raise ValueError(
            'Please enter the correct name and phone number, the name must be a period and the number must be numbers, preferably without symbols')
    record = address_book.get(name.lower())
    if not record:
        record = Record(name)
        address_book.add_record(record)
    record.add_phone(phone)
    return f"Added phone {phone} for contact {name}"


@input_error
def handler_change(name, old_phone, new_phone, address_book):
    old_phone = normalise(old_phone)
    new_phone = normalise(new_phone)
    record = address_book.get(name.lower())
    if not record:
        raise KeyError(f"{name} is not in contacts")
    if not record.edit_phone(old_phone, new_phone):
        raise ValueError(f"{old_phone} is not in {name}'s phones")
    return f"Changed phone {old_phone} to {new_phone} for contact {name}"


@input_error
def handler_phone(name, address_book):
    record = address_book.get(name.lower())
    if not record:
        raise KeyError(f"{name} is not in contacts")
    return "\n".join([phone.value for phone in record.phones])


@input_error
def handle_show_all(address_book):
    return "\n".join([f"{name}: {', '.join([phone.value for phone in record.phones])}" for name, record in address_book.items()])


@input_error
def show_day_to_birthday(day, month):
    return Birthday(day, month).days_to_birthday()


def main():
    address_book = AddressBook()

    while True:
        comands = input('Type hello to see a list of commands: ').lower()

        if comands == 'hello':
            print(handle_hello())

        elif comands == 'add':
            name_and_phone = input(
                'Please enter your name and phone number separated by a comma: ')
            try:
                name, phone = name_and_phone.rsplit(',', 1)
                message = handler_add(name, phone, address_book)
                print(message)
            except ValueError as e:
                print(str(e))

        elif comands == 'days birthday':
            dates = input(
                'Please enter a day and month separated by a comma: ')
            day, month = dates.split(',')
            dates = Birthday(int(day), int(month))
            print(dates.days_to_birthday())

        elif comands == 'next birthday':
            dates = input(
                'Please enter a day and month separated by a comma: ')
            day, month = dates.split(',')
            dates = Birthday(int(day), int(month))
            print(dates.next_birthday())

        elif comands == 'change':
            name_and_phone = input(
                'Please enter your name and phone number separated by a comma: ')
            try:
                name, old_phone, new_phone = name_and_phone.split(',', 2)
                message = handler_change(
                    name, old_phone, new_phone, address_book)
                print(message)
            except (KeyError, ValueError) as e:
                print(str(e))

        elif comands == 'phone':
            name = input('Please enter the name: ')
            try:
                message = handler_phone(name, address_book)
                print(message)
            except KeyError as e:
                print(str(e))

        elif comands == "show all":
            if len(address_book) >= 1:
                message = '\n'.join(list(address_book))
                print(message)
            elif len(address_book) == 0:
                message = 'Empty list'
                print(message)

        elif comands == 'good bye' or 'close' or 'exit':
            print('Good bye =)')
            break
        else:
            message = "Unknown command. Please try again."
            print(message)


if __name__ == '__main__':
    main()
