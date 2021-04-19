import os
import csv
import random
import io


class FileReader:
    def __init__(self, **kwargs):
        self.ROOT_FOLDER = "data" if kwargs.get("root") is None else kwargs.get("root")
        self.columns = ["sentence", "target"]

        self.folder_format = lambda folder_id: f"wiki_sentences_{str(folder_id).rjust(5, '0')}"
        self.csv_format = lambda csv_id: f"set_{str(csv_id).rjust(3, '0')}"

        self.files = {}

        for (dir_path, dir_name, file_names) in os.walk(self.ROOT_FOLDER):
            if file_names:
                for file in file_names:
                    self.files[os.path.join(dir_path, file)] = 2

    # def read_random_lines(self, lines_count=2000):
    #     lines = []
    #     total_lines = 0
    #
    #     for file_path in self.files:
    #         with io.open(file_path, newline='', encoding="utf-8") as file:
    #             csv_reader = csv.reader(file)
    #             total_lines += len(list(csv_reader))
    #
    #     for file_path in self.files:
    #         with io.open(file_path, newline='', encoding="utf-8") as file:
    #             csv_reader = csv.reader(file)
    #
    #             file_lines = list(csv_reader)
    #
    #             lines_in_file = len(file_lines)
    #             lines_to_count = int((lines_in_file / total_lines) * lines_count)
    #
    #             for i in range(lines_to_count):
    #                 while True:
    #                     index = random.randint(0, lines_in_file - 1)
    #
    #                     if index not in self.files.get(file_path):
    #                         break
    #
    #                 self.files[file_path].append(index)
    #                 lines.append(file_lines[index])
    #
    #     random.shuffle(lines)
    #     return lines

    def get_lines(self, lines_count=2000):
        lines = []
        line_total = 0

        for file_path in self.files:
            with io.open(file_path, newline='', encoding="utf-8") as file:
                if line_total == lines_count:
                    return lines

                file_lines = list(csv.reader(file))
                file_length = len(file_lines)

                min_index = self.files.get(file_path)

                if min_index > file_length:
                    continue

                max_index = min(file_length - 1, min_index + lines_count)

                lines += file_lines[min_index:max_index]
                line_total += max_index - min_index

                self.files[file_path] = max_index

                # print(f"MIN: {min_index}, MAX: {max_index}, FILE: {file_path}")

        return lines

    def vocabulary(self, tokenizer):
        for file_path in self.files:
            with io.open(file_path, newline='', encoding="utf-8") as file:
                csv_reader = csv.reader(file)
                file_lines = [" ".join(line) for line in list(csv_reader)]

                tokenizer.fit_on_texts([line.split() for line in file_lines])

        result = len(tokenizer.word_index) + 1

        print(f"Model vocabulary size is {result}")
        return result
