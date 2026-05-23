import csv


class CSVReader:
    @staticmethod
    def read_data(file_path):
        data_list = []
        with open(file_path, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data_list.append(row)
        return data_list

    @staticmethod
    def first_row(file_path):
        data = CSVReader.read_data(file_path)
        if not data:
            raise ValueError(f"No test data found in {file_path}")
        return data[0]
