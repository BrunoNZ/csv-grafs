#!/usr/bin/python3
# -*- coding: utf-8 -*-

from os import makedirs
from os.path import join
from csvgrafs.matplot import MatPlot


class GrafPlots:
    """
Plota todos os gráficos do GrafInputs dado como entrada.

### Atributos:
- inputs (GrafInputs): A instância de GrafInputs usada para inicializar a
    classe
    """

    def __init__(self, ginputs):
        self.inputs = ginputs
        self.__create_outdir()

    def plot_all_grafs(self):
        for graf in self.inputs.grafs:
            if graf.enabled:
                for kind in graf.kinds:
                    self.plot_graf(graf, kind)

    def plot_graf(self, graf, kind):
        plot = MatPlot(self.inputs.figsize, self.inputs.dpi)
        self.__plot_entries(plot, graf, kind)
        self.__plot_infos(plot, graf)
        plot.display(
            self.__get_outfile(graf, kind),
            self.inputs.mplbackend,
            self.inputs.fastmode
        )

    def __create_outdir(self):
        if self.__outdir() != "" or self.__outdir() is not None:
            makedirs(self.__outdir(), exist_ok=True)

    def __outdir(self):
        return self.inputs.output_dir

    def __get_outfile(self, graf, kind):
        return join(self.__outdir(), graf.get_output_filename(kind))

    def __plot_infos(self, plot, graf):
        plot.set_labels(x_label=graf.xlabel(), y_label=graf.ylabel())
        if graf.xfield():
            plot.set_xticks(graf.get_xticks(self.inputs))
        if graf.plot_title():
            plot.set_title(graf.title())
        if graf.plot_legend():
            plot.set_legend(graf.legend_options())

    def __plot_entries(self, plot, graf, kind):
        v_x = graf.get_vx(self.inputs)
        for entry in graf.entries:
            name = entry.get("field")
            opts = entry.get("opts", {})
            matrix = self.inputs.get_field_matrix(name, kind)
            for index, vector in enumerate(matrix):
                label = name
                if len(matrix) > 1:
                    label += ":" + str(index)
                plot.add_simple_plot(v_x, vector[:], label, **opts)
