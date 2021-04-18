import os
import csv
import random
import io


class FileReader:
    def __init__(self):
        self.ROOT_FOLDER = "data"
        self.columns = ["sentence", "target"]

        self.folder_format = lambda folder_id: f"wiki_sentences_{str(folder_id).rjust(5, '0')}"
        self.csv_format = lambda csv_id: f"set_{str(csv_id).rjust(3, '0')}"

        self.files = {}

        for (dir_path, dir_name, file_names) in os.walk(self.ROOT_FOLDER):
            if file_names:
                for file in file_names:
                    self.files[os.path.join(dir_path, file)] = []

    def read_random_lines(self, lines_count=2000):
        lines = []
        total_lines = 0

        for file_path in self.files:
            with io.open(file_path, newline='', encoding="utf-8") as file:
                csv_reader = csv.reader(file)
                total_lines += len(list(csv_reader))

        for file_path in self.files:
            with io.open(file_path, newline='', encoding="utf-8") as file:
                csv_reader = csv.reader(file)

                file_lines = list(csv_reader)

                lines_in_file = len(file_lines)
                lines_to_count = int((lines_in_file / total_lines) * lines_count)

                for i in range(lines_to_count):
                    while True:
                        index = random.randint(0, lines_in_file)

                        print(self.files.get(file_path))

                        if index in self.files.get(file_path):
                            index = random.randint(0, lines_in_file)
                        else:
                            break

                    self.files[file_path].append(index)
                    lines.append(file_lines[index])

        random.shuffle(lines)
        return lines


if __name__ == "__main__":
    reader = FileReader()
    list_1 = reader.read_random_lines()
