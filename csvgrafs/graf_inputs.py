#!/usr/bin/python3
# -*- coding: utf-8 -*-

from os import listdir
from os.path import join
import csv
import json
import numpy as np


class GrafInputs:

    ARGS_DICT = {
        "--input_dir": "inputdir",
        "-I": "inputdir",
        "--output_dir": "outputdir",
        "-O": "outputdir"
    }

    def __init__(self, sys_args):
        self.init_args(sys_args[0])
        self.read_command_line_args(sys_args)
        self.read_files()
        self.organize_values()
        self.process_data()

    def init_args(self, jsonfile):
        args = {}
        with open(jsonfile, encoding="UTF-8") as json_content:
            args = json.load(json_content)

        self.values = {}
        self.fieldnames = args.get("header", [])
        self.delimiter = args.get("delimiter", ";")
        self.files = args.get("files", [])
        self.output_dir = args.get("output_dir", None)
        self.grafs = args.get("grafs", [])

    def read_command_line_args(self, sys_args):
        args = {}
        for i, opt in enumerate(sys_args):
            opt_arg = self.ARGS_DICT.get(opt, False)
            if opt_arg:
                args[opt_arg] = sys_args[i+1]

        inputdir = args.get("inputdir", False)
        if inputdir:
            dirfiles = sorted(listdir(inputdir))
            self.files = map(lambda f: join(inputdir, f), dirfiles)

        if args.get("outputdir", False):
            self.output_dir = args.get("outputdir")

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
            result = np.matrix(list(matrix.values())).mean(0).tolist()[0]
            avg.update({name: {0: result}})
        return avg

    def get_field_values(self, name, kind=None):
        return self.get_value_by_kind(kind)[name].values()

    def get_field_items(self, name, kind=None):
        return self.get_value_by_kind(kind)[name].items()

    def get_value_by_kind(self, kind=None):
        v_name = "values"
        if kind == "norm":
            v_name = "values_normalized"
        elif kind == "avg":
            v_name = "avg"
        return getattr(self, v_name)
