from datetime import datetime

users = [
    {'name': 'Pavlo', 'birthday': datetime(year=1945, month=1, day=25)},
    {'name': 'Sasha', 'birthday': datetime(year=2000, month=2, day=25)},
    {'name': 'Kostya', 'birthday': datetime(year=2002, month=3, day=25)},
    {'name': 'Oleg', 'birthday': datetime(year=2015, month=4, day=25)},
    {'name': 'Jenya', 'birthday': datetime(year=2010, month=5, day=25)},
    {'name': 'Alex', 'birthday': datetime(year=1975, month=6, day=25)},
    {'name': 'Vanya', 'birthday': datetime(year=1978, month=7, day=25)},
    {'name': 'Andrey', 'birthday': datetime(year=1965, month=8, day=25)},
    {'name': 'Masha', 'birthday': datetime(year=1995, month=4, day=1)},
    {'name': 'Vika', 'birthday': datetime(year=1987, month=12, day=24)}, ]


def get_birthdays_per_week(birthday: list):
    current_time = datetime.now()
    birthday_list = []
    birthday_dict = {}

    # Through the loop we get the number, name and day of Sunday
    for dict_items in birthday:
        days = dict_items['birthday']  # 2000-04-25 00:00:00
        name = dict_items['name']  # Olexsandr, Pavlo
        str_days = days.strftime('%A')  # Tuesday, Friday

        # We are checking whether the birthday is exactly on Sunday, if yes, then we add the Sunday and name to the list
        if days.day - current_time.day == 7:
            birthday_list.append({str_days: name})

    # We cycle through the list and check whether the birthday falls on a weekend
    for char in birthday_list:
        key, value = list(char.items())[0]

        # If yes, then we replace this day with Monday
        if key == 'Saturday':
            char['Monday'] = char.pop('Saturday')

        elif key == 'Sunday':
            char['Monday'] = char.pop('Sunday')

    # We go through the cycle and check for duplicate Sundays
    for item in birthday_list:
        key, value = list(item.items())[0]

        # If there are duplicates, then we add all the values one key at a time separated by a comma
        if key in birthday_dict:
            birthday_dict[key] += f', {value}'

        # If there are no duplicates, then we add the value to the dictionary by key
        else:
            birthday_dict[key] = value

    # We display the value on the screen
    for key, val in birthday_dict.items():
        print(f'{key}: {val}')


get_birthdays_per_week(users)
