#!/usr/bin/python3

import sys
import multiprocessing
from multiprocessing.pool import ThreadPool
from os import listdir
from os.path import join
import subprocess

POPEN_OPTS = {"stdout": subprocess.PIPE, "stderr": subprocess.DEVNULL}


def call_proc(cmd):
    with subprocess.Popen(cmd, **POPEN_OPTS) as cmd_sp:
        out, err = cmd_sp.communicate()
        print("OK: ", " ".join(cmd))
        return (out, err)


def main():
    args = sys.argv[1:]
    csvgraf = args[0]
    defs_json = args[1]
    input_dir = args[2]
    inside_dir = args[3]
    output_dir = args[4]

    results = listdir(input_dir)
    results_dir = map(lambda f: [f, join(input_dir, f, inside_dir)], results)

    thread_pool = []
    with ThreadPool(multiprocessing.cpu_count()) as pool:
        for rname, dir_in in results_dir:
            dir_out = join(output_dir, rname)
            args = [csvgraf, defs_json, "-i", dir_in, "-o", dir_out]
            thread_pool.append(pool.apply_async(call_proc, (args,)))
        pool.close()
        pool.join()


if __name__ == '__main__':
    main()
