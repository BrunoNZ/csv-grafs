#!/usr/bin/python3
# -*- coding: utf-8 -*-

from os import makedirs
from os.path import join
import matplotlib.pyplot as plt


class MatPlot:

    DEFAULT_LEGEND_OPTIONS = {
        "loc": 'upper center',
        "bbox_to_anchor": (0.5, -0.125),
        "fancybox": False,
        "shadow": False,
        "ncol": 3
    }

    def __init__(self):
        self.plt = plt
        self.filetype = ".png"
        self.legend_options = self.DEFAULT_LEGEND_OPTIONS
        self.fig, self.a_x = self.plt.subplots(figsize=[10, 6])

    def add_simple_plot(self, v_x, v_y, label, **options):
        self.a_x.plot(v_x, v_y, label=label, **options)

    def add_diff_plot(self, v_y_1, v_y_2, label, **options):
        diff = []
        for y1i, y2i in zip(v_y_1, v_y_2):
            diff.append(y1i - y2i)

        self.add_simple_plot(diff, label, **options)

    def add_firstlast_plot(self, v_y_1, v_y_2, label, **options):
        cont = {"ls": "-"}
        dash = {"ls": "--"}
        self.add_simple_plot(v_y_1, label+" (Inicial)", **options, **cont)
        self.add_simple_plot(v_y_2, label+" (Final)", **options, **dash)

    def set_labels(self, x_label=None, y_label=None):
        if x_label is not None:
            self.a_x.set_xlabel(x_label)
        if y_label is not None:
            self.a_x.set_ylabel(y_label)

    def set_xticks(self, x_ticks):
        self.a_x.set_xticks(x_ticks)

    def set_title(self, title):
        self.a_x.set_title(title)

    def modify_height(self, perc):
        box = self.a_x.get_position()
        self.a_x.set_position([
            box.x0, box.y0 + box.height * (1.0-perc),
            box.width, box.height*perc
        ])

    def set_legend_options(self, options):
        self.legend_options.update(options)

    def plot_legend(self):
        self.a_x.legend(**self.legend_options)

    def save(self, filename):
        self.plot_legend()
        self.fig.tight_layout()
        self.fig.savefig(filename + self.filetype)

    def show(self):
        self.plot_legend()
        self.fig.tight_layout()
        self.plt.show()

    def close(self):
        self.plt.close()


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
            self.plot_graf(graf)

    def plot_graf(self, graf):
        plot = MatPlot()
        defs = self.get_graf_defs(graf)
        outfile = self.set_outfile(defs)
        self.plot_basic_infos(plot, defs)
        self.plot_entries(plot, defs)
        self.display_plot(plot, outfile)

    def get_graf_defs(self, graf):
        defs = {}
        defs.update({"kind": graf.get("kind", None)})
        defs.update({"x_field": graf.get("xfield", False)})
        defs.update({"v_x": self.get_vx(defs["x_field"])})
        defs.update({"title": graf.get("title", "")})
        defs.update({"x_label": graf.get("xlabel", "")})
        defs.update({"y_label": graf.get("ylabel", "")})
        defs.update({"filename": graf.get("filename", None)})
        defs.update({"entries": graf.get("entries", {})})
        defs.update({"entries_names": list(map(
            lambda e: e.get("field", ""), defs["entries"]
        ))})
        defs.update({"legend_options": graf.get("legend_options", {})})
        return defs

    def set_outfile(self, defs):
        if self.outdir is None:
            return None

        filename = defs["filename"]
        if filename == "" or filename is None:
            filename = defs.get("kind", "") + "_"
            filename += "-".join(defs["entries_names"])

        return join(self.outdir, filename)

    def plot_basic_infos(self, plot, defs):
        plot.set_title(defs["title"])
        plot.set_legend_options(defs["legend_options"])
        plot.set_labels(x_label=defs["x_label"], y_label=defs["y_label"])
        if defs["x_field"]:
            plot.set_xticks(defs["v_x"])

    def get_vx(self, x_field):
        if x_field:
            return list(self.inputs.get_field_values(x_field))[0]
        return range(0, self.inputs.d_x)

    def plot_entries(self, plot, defs):
        for entry in defs["entries"]:
            name = entry.get("field")
            opts = entry.get("opts", {})
            matrix = self.inputs.get_field_items(name, defs["kind"])
            for index, values in matrix:
                label = name
                if len(matrix) > 1:
                    label += ":" + str(index)
                plot.add_simple_plot(defs["v_x"], values, label, **opts)

    def display_plot(self, plot, outfile=None):
        if outfile:
            plot.save(outfile)
        else:
            plot.show()
        plot.close()
