#!/usr/bin/python3

import sys
from csvgrafs import graf_inputs as inputs
from csvgrafs import graf_plots as plots


def main():
    ginputs = inputs.GrafInputs(sys.argv[1:])
    gplots = plots.GrafPlots(ginputs)
    gplots.plot_all_grafs()


main()
