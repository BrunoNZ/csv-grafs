#!/usr/bin/python3
# -*- coding: utf-8 -*-

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
        # self.plt.xlim(1, 60)

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

    def set_title(self, title):
        self.a_x.set_title(title)

    def modify_height(self, perc):
        box = self.a_x.get_position()
        self.a_x.set_position([
            box.x0, box.y0 + box.height * (1.0-perc),
            box.width, box.height*perc
        ])

    def set_legend_options(self, options):
        self.legend_options = options

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

    def plot_all_grafs(self):
        for graf in self.inputs.grafs:
            self.plot_graf(graf)

    def plot_graf(self, graf):
        plot = MatPlot()
        plot.set_title(graf.get("title", ""))
        plot.set_labels(
            x_label=graf.get("xlabel", ""),
            y_label=graf.get("ylabel", "")
        )
        for entry in graf.get("entries", []):
            name = entry.get("field")
            for index, values in self.inputs.values.items():
                v_y = values[name]
                v_x = range(0, len(v_y))
                label = name + ":" + str(index)
                plot.add_simple_plot(v_x, v_y, label)
        plot.show()
        plot.close()
