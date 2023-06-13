import os
import shutil
import re

main_path = 'C:\\Users\PC\Desktop\Хлам'

extensions = {

    'video': ['mp4', 'mov', 'avi', 'mkv'],

    'audio': ['mp3', 'wav', 'ogg', 'amr'],

    'image': ['jpg', 'png', 'jpeg', 'svg'],

    'archive': ['zip', 'gz', 'tar'],

    'documents': ['pdf', 'txt', 'doc', 'docx', 'xlsx', 'pptx'],
}


# Перемістили усі файлі в main_path
def parse_folders(folder):
    dirpath_filenames = []
    for i in os.scandir(folder):
        if i.is_dir():
            for dirpath, dirnames, filenames in os.walk(i.path):
                for a in filenames:
                    dirpath_filenames.append(dirpath+'\\'+a)
    for ands in dirpath_filenames:
        s = ands.split('\\')[-1]
        os.rename(ands, f'{folder}\\{s}')


# Получили список папок
def get_folders_path(folder) -> list:
    dirpath_filenames = []
    for i in os.scandir(folder):
        if i.is_dir():
            for dirpath, dirnames, filenames in os.walk(i.path):
                dirpath_filenames.append(dirpath)
    return dirpath_filenames


# Видаляємо пусті папки
def remove_empty_folders(folder):
    folders_path = get_folders_path(folder)
    for char in folders_path:
        if not os.listdir(char):
            os.removedirs(char)


# Получили список путів файлів
def get_file_path(folder):
    spisok = []
    for i in os.listdir(folder):
        spisok.append(os.path.join(folder, i))
    return spisok


# Повернули список назв файлів
def replace_file(folder):
    get_file = get_file_path(folder)
    spisok = []
    for file in get_file:
        file_name = file.split('\\')[-1]
        file_name = file_name.replace(' ', '_', 1)
        rep = re.compile("[^a-zA-Zа-яА-я,.,_,\d]")
        text = rep.sub("", file_name)
        spisok.append(text)
    return spisok


# Получаємо список нормалізованих назв файлів
def normalise(folder):
    CYRILLIC = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    LATIN = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
             "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    TRANS = {}
    list_translate = []
    get_replace_file = replace_file(folder)

    for c, l in zip(CYRILLIC, LATIN):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
    for i in get_replace_file:
        list_translate.append(i.translate(TRANS))
    return list_translate


# Получили список шляхів нормалізованих путів файлів
def get_new_file_path(folder):
    normalise_file = normalise(folder)
    spisok = []
    for i in normalise_file:
        spisok.append(os.path.join(folder, i))
    return spisok


# Змінюємо назви файлів
def normalise_file_path(folder):
    old_file_path = get_file_path(folder)
    new_file_path = get_new_file_path(folder)
    spisok_old = []
    spisok_new = []
    for k, j in zip(old_file_path, new_file_path):
        if k not in j:
            spisok_old.append(k)
            spisok_new.append(j)
    for a, b in zip(spisok_old, spisok_new):
        os.rename(a, b)


# Создали папки під іменами із словника
def create_folders_from_list(folder_path, folder_names):
    for folder in folder_names:
        if not os.path.exists(f'{folder_path}\\{folder}'):
            os.mkdir(f'{folder_path}\\{folder}')


# Сортируємо файли по папкам
def sort_files(folder_path):
    file_paths = get_new_file_path(folder_path)
    ext_list = list(extensions.items())
    for file_path in file_paths:
        extension = file_path.split('.')[-1]
        file_name = file_path.split('\\')[-1]
        for dict_key_int in range(len(ext_list)):
            if extension in ext_list[dict_key_int][1]:
                os.rename(
                    file_path, f'{main_path}\\{ext_list[dict_key_int][0]}\\{file_name}')


# Создаємо папки в папці archive
def create_folder_from_archive(folder):
    archive_path = folder+'\\'+'archive'
    for i in os.listdir(archive_path):
        name = i.split('.')[0]
        os.mkdir(archive_path+'\\'+name)


# Розпакували архіви до папок під їх назвами
def unpuck_archives(folder):
    folders = folder+'\\'+'archive'
    file_name = []
    file_names_ext = []
    for dirpath, dirnames, filenames in os.walk(folders):
        for i in filenames:
            file_name.append(i.split('.')[0])
        for i in filenames:
            file_names_ext.append(i)
    for a, b in zip(file_name, file_names_ext):
        shutil.unpack_archive(folders+'\\'+b, folders+'\\'+a)


# Удалили архіви з папки
def delete_archives(folder):
    folders = folder+'\\'+'archive'
    for i in os.scandir(folders):
        if i.is_file():
            os.remove(i)


if __name__ == '__main__':
    parse_folders(main_path)
    remove_empty_folders(main_path)
    normalise_file_path(main_path)
    create_folders_from_list(main_path, extensions)
    sort_files(main_path)
    create_folder_from_archive(main_path)
    unpuck_archives(main_path)
    delete_archives(main_path)
