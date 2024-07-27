from os import mkdir, getcwd
from os.path import getctime, getmtime, exists
from pathlib import Path
from re import match
from shutil import copy
from time import localtime, strftime, time


def process_file(source: Path, target: str) -> None:
    filename = str(source).split("\\")[-1]
    created = getctime(source)
    modified = getmtime(source)
    earliest = min(created, modified)
    year = strftime("%Y", localtime(earliest))
    date = strftime("%d-%m", localtime(earliest))
    if date == target:
        if not exists(f"OnThisDayIn{year}"):
            mkdir(f"OnThisDayIn{year}")
        try:
            copy(source, rf"OnThisDayIn{year}\{filename}")
        except:
            pass

   
def process_files(source: Path, date: str) -> None:
    for file in source.rglob("*"):
        if file.is_file():
            process_file(file, date)


if __name__ == "__main__":
    today = strftime("%d-%m", localtime(time()))
    while True:
        date_mode = input(
            "1 - Output all files made on the current date\n2 - Set a specific date to look for\n"
        )
        if date_mode == "1":
            date = strftime("%d-%m", localtime(time()))
            break
        elif date_mode == "2":
            date = input(
                "Please enter your desired date in the following format: dd-mm\nExample: 14-06\n"
            )
            pattern = r"[0-9]{2}-[0-9]{2}"
            if match(pattern, date):
                break
        print("Invalid input\n")
    while True:
        source = input(
            "Provide an adress of a folder or press Enter to go through the current folder instead\n"
        )
        if not source:
            source = Path(getcwd())
            break
        else:
            source = source.strip()
            source = Path(source.replace('"', ""))
            if exists(source):
                break
        print("Invalid input\n")
    process_files(source, date)
