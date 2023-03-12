from datetime import date
from os import makedirs, startfile
from os.path import exists, getsize

from timed_reference import main as start_timed_reference

DATE = date.today().strftime("%Y_%m_%d")
PATH = "C:\\Users\\Damien\\Desktop\\DRAWING_\\Quick_study"


def main():

    folder_ = f"{PATH}\\{DATE}"
    if not exists(folder_):
        makedirs(folder_)

    file_ = f"{PATH}\\{DATE}\\{DATE}.kra"
    if not exists(file_) or getsize(file_) == 0:
        with open(file_, 'w') as _:   # create a place holder file
            pass
        startfile(folder_)
        startfile("C:\\Program Files\\Krita (x64)\\bin\\krita.exe")
        start_timed_reference()


if __name__ == "__main__":
    main()
