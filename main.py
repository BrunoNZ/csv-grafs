#!/usr/bin/python3

import sys
from csvgrafs import graf_inputs as inputs
from csvgrafs import graf_plots as plots


def main():
    input_json = sys.argv[1:][0]
    ginputs = inputs.GrafInputs(input_json)
    gplots = plots.GrafPlots(ginputs)
    gplots.plot_all_grafs()


main()
