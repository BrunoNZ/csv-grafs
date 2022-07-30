#!/usr/bin/python3

import sys
import subprocess
import multiprocessing
from multiprocessing.pool import ThreadPool
from os import listdir
from os.path import join, dirname

CSV_GRAFS = join(dirname(__file__), "main.py")
POPEN_OPTS = {"stdout": subprocess.PIPE, "stderr": subprocess.DEVNULL}


def call_proc(opts):
    with subprocess.Popen([CSV_GRAFS] + opts, **POPEN_OPTS) as cmd:
        out, err = cmd.communicate()
        print("OK: ", " ".join(opts))
        return (out, err)


def main():
    args = sys.argv[1:]
    defs_json = args[0]
    input_dir = args[1]
    inside_dir = args[2]
    output_dir = args[3]

    results = listdir(input_dir)
    results_dir = map(lambda f: [f, join(input_dir, f, inside_dir)], results)

    thread_pool = []
    with ThreadPool(multiprocessing.cpu_count()) as pool:
        for rname, dir_in in results_dir:
            dir_out = join(output_dir, rname)
            args = [defs_json, "-i", dir_in, "-o", dir_out]
            thread_pool.append(pool.apply_async(call_proc, (args,)))
        pool.close()
        pool.join()


if __name__ == '__main__':
    main()
