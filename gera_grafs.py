#!/usr/bin/python3

import sys
import csv


def read_args():
    sys_args = sys.argv[1:]
    args_dict = {
        "--header": "header",
        "-H": "header",
        "--filename": "filename",
        "-F": "filename",
        "--size": "size",
        "-S": "size"
    }
    args = {}
    for i, opt in enumerate(sys_args):
        opt_arg = args_dict.get(opt)
        if opt_arg:
            args[opt_arg] = sys_args[i+1]
    return args


def read_csv(args):
    fieldnames = args.get("header").split(";")
    values = {}
    for name in fieldnames:
        values.update({name: []})
    with open(args["filename"], newline='', encoding="utf-8") as csvfile:
        obj = csv.DictReader(csvfile,
                             fieldnames=fieldnames,
                             delimiter=';',
                             quoting=csv.QUOTE_NONNUMERIC)
        for row in obj:
            for name in obj.fieldnames:
                values[name].append(row[name])
    return values


def main():
    args = read_args()
    values = read_csv(args)
    print(values)


main()
