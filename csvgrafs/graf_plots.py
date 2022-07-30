#!/usr/bin/python3
# -*- coding: utf-8 -*-

from os import makedirs
from os.path import join
from csvgrafs.matplot import MatPlot


class GrafPlots:

    def __init__(self, ginputs):
        self.inputs = ginputs
        self.outdir = self.inputs.output_dir
        if self.outdir != "" or self.outdir is not None:
            makedirs(self.outdir, exist_ok=True)
        else:
            self.outdir = None

    def plot_all_grafs(self):
        for graf in self.inputs.grafs:
            if graf.enabled:
                for kind in graf.kinds:
                    self.prepare_plot(graf, kind).display()

    def prepare_plot(self, graf, kind):
        plot = MatPlot(self.set_outfile(graf, kind))
        self.plot_basic_infos(plot, graf)
        self.plot_entries(plot, graf, kind)
        return plot

    def set_outfile(self, graf, kind):
        if self.outdir is None:
            return None
        return join(self.outdir, graf.get_output_filename(kind))

    def plot_basic_infos(self, plot, graf):
        plot.set_title(graf.title)
        plot.set_legend_options(graf.legend_options)
        plot.set_labels(x_label=graf.x_label, y_label=graf.y_label)
        if graf.x_field:
            plot.set_xticks(graf.get_xticks(self.inputs))

    def plot_entries(self, plot, graf, kind):
        v_x = graf.get_vx(self.inputs)
        for entry in graf.entries:
            name = entry.get("field")
            opts = entry.get("opts", {})
            matrix = self.inputs.get_field_items(name, kind)
            for index, values in matrix:
                label = name
                if len(matrix) > 1:
                    label += ":" + str(index)
                plot.add_simple_plot(v_x, values, label, **opts)
