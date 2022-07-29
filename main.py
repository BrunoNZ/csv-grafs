#!/usr/bin/python3

import sys
from csvgrafs.graf_inputs import GrafInputs
from csvgrafs.graf_plots import GrafPlots


def main():
    ginputs = GrafInputs(sys.argv[1:])
    gplots = GrafPlots(ginputs)
    gplots.plot_all_grafs()


main()
