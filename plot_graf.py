#!/usr/bin/python3

import sys
from csvgrafs.graf_inputs import GrafInputs
from csvgrafs.graf_plots import GrafPlots

PARAM_ERROR_MSG = """
Erro! Parâmetros inválidos. Utilize:
./plot_graf.py <DEFS_JSON> [opts]

 * DEFS_JSON: Arquivo JSON contendo as definições da plotagem
 * opts:
   -i | --input_dir <INPUT_DIR>:
      INPUT_DIR: Diretório contendo os arquivos CSVs
   -o | --output_dir <OUTPUT_DIR>:
      OUTPUT_DIR: Diretório onde as figuras serão criadas
"""


def __verify_args(args):
    if len(args) in [1, 3, 5]:
        return True

    print(PARAM_ERROR_MSG)
    return False


def main():
    args = sys.argv[1:]
    if not __verify_args(args):
        return
    ginputs = GrafInputs(args)
    gplots = GrafPlots(ginputs)
    gplots.plot_all_grafs()


if __name__ == '__main__':
    main()
