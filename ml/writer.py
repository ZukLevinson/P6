import os
import csv
import re
import io


class CSVWriter:
    def __init__(self):
        self.MAIN_FOLDER = "data"
        self.columns = ["sentence", "target"]

        self.folder_format = lambda folder_id: f"wiki_sentences_{str(folder_id).rjust(5, '0')}"
        self.csv_format = lambda csv_id: f"set_{str(csv_id).rjust(3, '0')}"

    def create_folder(self):
        new_id = "0".rjust(5, "0")

        if not os.path.isdir(self.MAIN_FOLDER):
            os.mkdir(self.MAIN_FOLDER)

        if os.listdir("data"):
            last_name = sorted(os.listdir(self.MAIN_FOLDER))[-1]
            new_id = int(last_name.split("_")[-1]) + 1

        new_dir_name = self.folder_format(new_id)
        os.mkdir(f"{self.MAIN_FOLDER}/{new_dir_name}")

        return new_dir_name

    def create_csv_file(self, folder_name, columns=None):
        if columns is None:
            columns = self.columns

        files = os.listdir(f"{self.MAIN_FOLDER}/{folder_name}")

        new_id = 0

        if files:
            last_name = sorted(files)[-1]

            new_id = int(re.split("[_.]", last_name)[1]) + 1

        new_csv_name = self.csv_format(new_id)

        with open(f"{self.MAIN_FOLDER}/{folder_name}/{new_csv_name}.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(columns)

        return new_csv_name

    def add_rows(self, path, rows):
        with io.open(f"{self.MAIN_FOLDER}/{path}", "w+", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(rows)

    def count_rows(self, path):
        with io.open(f"{self.MAIN_FOLDER}/{path}", "w+", encoding="utf-8") as file:
            writer = csv.reader(file)
            return len(list(writer))

    def count_csvs_in_folder(self, path):
        return len(os.listdir(f"{self.MAIN_FOLDER}/{path}"))
