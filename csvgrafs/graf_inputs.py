#!/usr/bin/python3
# -*- coding: utf-8 -*-

import csv
import json
import numpy as np


class GrafInputs:
    def __init__(self, jsonfile):
        self.init_args(jsonfile)
        self.read_files()
        self.organize_values()
        self.process_data()

    def init_args(self, jsonfile):
        args = {}
        with open(jsonfile, encoding="UTF-8") as json_content:
            args = json.load(json_content)

        self.values = {}
        self.delimiter = args.get("delimiter", ";")
        self.fieldnames = args.get("header", [])
        self.files = args.get("files", [])
        self.grafs = args.get("grafs", [])

    def read_files(self):
        for index, fname in enumerate(self.files):
            self.values.update({index: self.read_csv(fname)})

    def read_csv(self, fname):
        values = {}
        for name in self.fieldnames:
            values.update({name: []})

        dict_reader_opts = {
            "fieldnames": self.fieldnames,
            "delimiter": self.delimiter,
            "quoting": csv.QUOTE_NONNUMERIC
        }
        with open(fname, newline='', encoding="utf-8") as csvfile:
            obj = csv.DictReader(csvfile, **dict_reader_opts)
            for row in obj:
                for name in obj.fieldnames:
                    values[name].append(row[name])
        return values

    def organize_values(self):
        nvalues = {}
        dx_vector = []
        for name in self.fieldnames:
            nvalues.update({name: {}})

        for index, matrix in self.values.items():
            for name, vector in matrix.items():
                nvalues[name].update({index: vector})
                dx_vector.append(len(vector))
        self.values.clear()
        self.values = nvalues

        s_dx_vector = np.unique(dx_vector)
        if len(s_dx_vector) != 1:
            raise AssertionError("not unique DX")
        self.d_x = s_dx_vector[0]

    def process_data(self):
        self.values_normalized = self.calculate_norm()
        self.avg = self.calculate_avg()

    def calculate_norm(self):
        normalized = {}
        for name, matrix in self.values.items():
            normalized.update({name: {}})
            for index, vector in matrix.items():
                norm = vector / np.linalg.norm(vector)
                normalized[name].update({index: norm})
        return normalized

    def calculate_avg(self):
        avg = {}
        for name, matrix in self.values.items():
            result = np.matrix(list(matrix.values())).mean(0).tolist()
            avg.update({name: result})
        return avg

    def get_field_values(self, name):
        return self.values[name].values()

    def get_field_items(self, name):
        return self.values[name].items()
