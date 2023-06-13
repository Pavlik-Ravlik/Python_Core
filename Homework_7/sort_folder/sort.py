import os
import shutil
import re

main_path = 'C:\\Users\PC\Downloads'

extensions = {

    'video': ['mp4', 'mov', 'avi', 'mkv'],

    'audio': ['mp3', 'wav', 'ogg', 'amr'],

    'image': ['jpg', 'png', 'jpeg', 'svg'],

    'archive': ['zip', 'gz', 'tar'],

    'documents': ['pdf', 'txt', 'doc', 'docx', 'xlsx', 'pptx'],
}


# Перемістили усі файлі в main_path
def parse_folders(folder_path: str) -> None:
    dirpath_filenames = []
    for parse_folder in os.scandir(folder_path):
        if parse_folder.is_dir():
            for dirpath, dirnames, filenames in os.walk(parse_folder.path):
                for a in filenames:
                    dirpath_filenames.append(dirpath+'\\'+a)
    for names_dir in dirpath_filenames:
        name = names_dir.split('\\')[-1]
        os.rename(names_dir, f'{folder_path}\\{name}')


# Получили список папок
def get_folders_path(folder_path: str) -> list:
    dirpath_filenames = []
    for i in os.scandir(folder_path):
        if i.is_dir():
            for dirpath, dirnames, filenames in os.walk(i.path):
                dirpath_filenames.append(dirpath)
    return dirpath_filenames


# Видаляємо пусті папки
def remove_empty_folders(folder_path_list: list) -> None:
    folders_path = get_folders_path(folder_path_list)
    for char in folders_path:
        if not os.listdir(char):
            os.removedirs(char)


# Получили список путів файлів
def get_file_path(folder_path: str) -> list:
    spisok = []
    for i in os.listdir(folder_path):
        spisok.append(os.path.join(folder_path, i))
    return spisok


# Повернули список назв файлів
def replace_file(folder_path: str) -> list:
    get_file = get_file_path(folder_path)
    spisok = []
    for file in get_file:
        file_name = file.split('\\')[-1]
        file_name = file_name.replace(' ', '_', 1)
        rep = re.compile("[^a-zA-Zа-яА-я,.,_,\d]")
        text = rep.sub("", file_name)
        spisok.append(text)
    return spisok


# Получаємо список нормалізованих назв файлів
def normalise(folder_path: str) -> list:
    CYRILLIC = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    LATIN = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
             "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    TRANS = {}
    list_translate = []
    get_replace_file = replace_file(folder_path)

    for c, l in zip(CYRILLIC, LATIN):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
    for i in get_replace_file:
        list_translate.append(i.translate(TRANS))
    return list_translate


# Получили список шляхів нормалізованих путів файлів
def get_new_file_path(folder_path: str) -> list:
    normalise_file = normalise(folder_path)
    spisok = []
    for i in normalise_file:
        spisok.append(os.path.join(folder_path, i))
    return spisok


# Змінюємо назви файлів
def normalise_file_path(folder_path: str) -> None:
    old_file_path = get_file_path(folder_path)
    new_file_path = get_new_file_path(folder_path)
    spisok_old = []
    spisok_new = []
    for old, new in zip(old_file_path, new_file_path):
        if old not in new:
            spisok_old.append(old)
            spisok_new.append(new)
    for s_old, s_new in zip(spisok_old, spisok_new):
        os.rename(s_old, s_new)


# Создали папки під іменами із словника
def create_folders_from_list(folder_path: str, folder_names: dict) -> None:
    for names in folder_names:
        if not os.path.exists(f'{folder_path}\\{names}'):
            os.mkdir(f'{folder_path}\\{names}')


# Сортируємо файли по папкам
def sort_files(folder_path: str) -> None:
    file_paths = get_new_file_path(folder_path)
    ext_list = list(extensions.items())
    for path in file_paths:
        extension = path.split('.')[-1]
        file_name = path.split('\\')[-1]
        for dict_key_int in range(len(ext_list)):
            if extension in ext_list[dict_key_int][1]:
                os.rename(
                    path, f'{main_path}\\{ext_list[dict_key_int][0]}\\{file_name}')


# Создаємо папки в папці archive
def create_folder_from_archive(folder_path: str) -> None:
    archive_path = folder_path+'\\'+'archive'
    for archive in os.listdir(archive_path):
        name = archive.split('.')[0]
        os.mkdir(archive_path+'\\'+name)


# Розпакували архіви до папок під їх назвами та удалили архіви з папки
def unpuck_archives(folder_path: str) -> None:
    path_to_folders = folder_path+'\\'+'archive'
    file_name = []
    file_names_ext = []
    for dirpath, dirnames, filenames in os.walk(path_to_folders):
        for i in filenames:
            file_name.append(i.split('.')[0])
        for i in filenames:
            file_names_ext.append(i)
    for a, b in zip(file_name, file_names_ext):
        shutil.unpack_archive(path_to_folders+'\\'+b, path_to_folders+'\\'+a)
    for i in os.scandir(path_to_folders):
        if i.is_file():
            os.remove(i)


def start() -> None:
    parse_folders(main_path)
    remove_empty_folders(main_path)
    normalise_file_path(main_path)
    create_folders_from_list(main_path, extensions)
    sort_files(main_path)
    create_folder_from_archive(main_path)
    unpuck_archives(main_path)


if __name__ == '__main__':
    start()
