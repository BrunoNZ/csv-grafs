#!/usr/bin/python3

import sys
import subprocess
import multiprocessing
from multiprocessing.pool import ThreadPool
from os import listdir
from os.path import join, dirname

CSV_GRAFS = join(dirname(__file__), "main.py")
POPEN_OPTS = {"stdout": subprocess.PIPE, "stderr": subprocess.DEVNULL}

PARAM_ERROR_MSG = """
Erro! Parâmetros inválidos. Utilize:
./execute_all.py [DEFS_JSON] [INPUT_DIR] [INSIDE_DIR] [OUTPUT_DIR]

 - DEFS_JSON: Arquivo JSON contendo as definições da plotagem
 - INPUT_DIR: Diretório contendo os diretórios dos resultados
 - INSIDE_DIR: Nome do diretório interno ao INPUT_DIR/<res> contendo os CSVs
   - Ex.: Para [INPUT_DIR]/<nome_resultado>/log, o valor seria "log"
   - Usar "" caso os CSVs estejam imediatamente em [INPUT_DIR]/<nome_resultado>
 - OUTPUT_DIR: Diretório onde as figuras serão criadas
"""


def __call_csvgraf(opts):
    with subprocess.Popen([CSV_GRAFS] + opts, **POPEN_OPTS) as cmd:
        out, err = cmd.communicate()
        print("OK: ", " ".join(opts))
        return (out, err)


def __verify_args(args):
    if len(args) == 4:
        return True

    print(PARAM_ERROR_MSG)
    return False


def main():
    args = sys.argv[1:]
    if not __verify_args(args):
        return
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
            thread_pool.append(pool.apply_async(__call_csvgraf, (args,)))
        pool.close()
        pool.join()


if __name__ == '__main__':
    main()
