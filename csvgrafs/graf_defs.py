#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np


class GrafDefs:
    """
Armazena os parâmetros de um gráfico/figura, lidos da seção "grafs" do
arquivo JSON

### Atributos:
- enabled (bool): Define se o gráfico deve ser plotado ou não.
- kinds ([string]): Lista dos tipos de gráficos que devem ser plotados
    para o atual conjunto de parâmetros.
    (Opções: "original", "avg", "norm", "norm01").
    Padrão: ["original"]
- entries ([dict]): Dicionário contendo as opções dos campos que devem ser
    plotados
- entries_names ([string]): Lista dos nomes dos campos, gerada a partir
    das chaves de "entries"
- opts (dict): Dicionário contendo todas as chaves de VALID_OPTS

### Opções válidas (VALID_OPTS):
- plot_title (bool): Indica se o título deve ser plotado ou não.
    Padrão: True
- plot_legend (bool): Indica se as legendas devem ser plotadas ou não.
    Padrão: True
- xfield (string): Nome do campo que deve ser usado para o eixo X.
    Caso o valor seja nulo será usado "range(1, len)", sendo "len"
    a quantidade de linhas dos arquivos CSVs.
    Padrão: None
- xfreq (int): Valor que define a frequência em que os ticks do eixo X
    serão plotados, entre o primeiro e último valor de "x_field".
    Caso o valor seja nulo será usado o valor de "x_field".
    Ex.: Para o valor 5, será plotado: [1,6,11,...].
    Padrão: 1
- title (string): Título do gráfico.
    Padrão: None
- xlabel (string): Label do eixo X
    Padrão: None
- ylabel (string): Label do eixo Y
    Padrão: None
- filename (string): Nome do arquivo de saída.
    Caso o valor seja nulo será usada uma combinação do tipo e dos campos.
    Padrão: None
- legend_options (dict): Opções de plotagem da legenda, que serão passados
    como parâmetros para a função "matplotlib.pyplot.legend"
    Padrão: {}
    """

    VALID_OPTS = [
        ["plot_title", True],
        ["plot_legend", True],
        ["xfield", None],
        ["xfreq", None],
        ["title", None],
        ["xlabel", None],
        ["ylabel", None],
        ["filename", None],
        ["legend_options", {}]
    ]

    def __init__(self, graf, legend_options=dict):
        self.enabled = graf.get("enabled", True)
        self.entries = graf.get("entries", [])
        self.kinds = graf.get("kinds", ["original"])
        self.opts = {}
        for opt_name, opt_default in self.VALID_OPTS:
            self.opts.update({opt_name: graf.get(opt_name, opt_default)})
        self.opts["legend_options"] = {
            **legend_options,
            **self.opts["legend_options"]
        }
        self.entries_names = list(map(lambda e: e.get("field"), self.entries))

    def plot_title(self):
        return self.opts["plot_title"]

    def plot_legend(self):
        return self.opts["plot_legend"]

    def legend_options(self):
        return self.opts["legend_options"]

    def xfield(self):
        return self.opts["xfield"]

    def xfreq(self):
        return self.opts["xfreq"]

    def title(self):
        return self.opts["title"]

    def xlabel(self):
        return self.opts["xlabel"]

    def ylabel(self):
        return self.opts["ylabel"]

    def filename(self):
        return self.opts["filename"]

    def get_vx(self, ginput):
        if self.xfield():
            return list(ginput.get_field_matrix(self.xfield()))[0]
        return range(0, ginput.d_x)

    def get_xticks(self, ginput):
        v_x = self.get_vx(ginput)
        if not self.xfreq():
            return v_x
        return np.arange(v_x[0], v_x[-1], self.xfreq())

    def get_output_filename(self, kind):
        if self.filename():
            return self.filename()
        return kind + "_" + "-".join(self.entries_names)
