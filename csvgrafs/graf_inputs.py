#!/usr/bin/python3
# -*- coding: utf-8 -*-

import csv
import json


class GrafInputs:
    def __init__(self, jsonfile):
        self.init_args(jsonfile)
        self.read_files()

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
