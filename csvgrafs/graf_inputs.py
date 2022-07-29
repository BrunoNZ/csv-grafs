#!/usr/bin/python3
# -*- coding: utf-8 -*-

from os import listdir
from os.path import join
import csv
import json
import numpy as np


class GrafDefs:

    def __init__(self, graf):
        self.kinds = graf.get("kinds", ["original"])
        self.x_field = graf.get("xfield", False)
        self.title = graf.get("title", "")
        self.x_label = graf.get("xlabel", "")
        self.y_label = graf.get("ylabel", "")
        self.filename = graf.get("filename", None)
        self.entries = graf.get("entries", {})
        self.entries_names = list(map(lambda e: e.get("field"), self.entries))
        self.legend_options = graf.get("legend_options", {})

    def get_vx(self, ginput):
        if self.x_field:
            return list(ginput.get_field_values(self.x_field))[0]
        return range(0, ginput.d_x)

    def get_output_filename(self, kind):
        if self.filename:
            return self.filename
        return kind + "_" + "-".join(self.entries_names)


class GrafInputs:

    ARGS_DICT = {
        "--input_dir": "inputdir",
        "-i": "inputdir",
        "--output_dir": "outputdir",
        "-o": "outputdir"
    }

    def __init__(self, sys_args):
        self.__init_args(sys_args[0])
        self.__read_command_line_args(sys_args)
        self.__read_files()
        self.__organize_values()
        self.__process_data()

    def __init_args(self, jsonfile):
        args = {}
        with open(jsonfile, encoding="UTF-8") as json_content:
            args = json.load(json_content)

        self.values = {}
        self.fieldnames = args.get("header", [])
        self.delimiter = args.get("delimiter", ";")
        self.files = args.get("files", [])
        self.output_dir = args.get("output_dir", None)
        self.grafs = []
        for graf in args.get("grafs", []):
            self.grafs.append(GrafDefs(graf))

    def __read_command_line_args(self, sys_args):
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

    def __read_files(self):
        for index, fname in enumerate(self.files):
            self.values.update({index: self.__read_csv(fname)})

    def __read_csv(self, fname):
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

    def __organize_values(self):
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

    def __process_data(self):
        self.values_normalized = self.__calculate_norm()
        self.avg = self.__calculate_avg()

    def __calculate_norm(self):
        normalized = {}
        for name, matrix in self.values.items():
            normalized.update({name: {}})
            for index, vector in matrix.items():
                norm = vector / np.linalg.norm(vector)
                normalized[name].update({index: norm})
        return normalized

    def __calculate_avg(self):
        avg = {}
        for name, matrix in self.values.items():
            result = np.matrix(list(matrix.values())).mean(0).tolist()[0]
            avg.update({name: {0: result}})
        return avg

    def get_field_values(self, name, kind=None):
        try:
            return self.get_value_by_kind(kind)[name].values()
        except KeyError as err:
            print("get_field_values", name, kind, "=>", err)
            raise

    def get_field_items(self, name, kind=None):
        try:
            return self.get_value_by_kind(kind)[name].items()
        except KeyError as err:
            print("get_field_items", name, kind, "=>", err)
            raise

    def get_value_by_kind(self, kind=None):
        v_name = "values"
        if kind == "norm":
            v_name = "values_normalized"
        elif kind == "avg":
            v_name = "avg"
        return getattr(self, v_name)
