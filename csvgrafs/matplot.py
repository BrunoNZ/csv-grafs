import matplotlib
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle


class MatPlot:
    """
Wrapper do Matplotlib para facilitar a plotagem de alguns
tipos especificos de gráficos.

### Atributos:
- plt (pyplot): Instancia de matplotlib.pyplot
- fig (Figure): Retorno de subplots
- a_x (axes.Axes): Retorno de subplots
    """

    DEFAULT_LEGEND_OPTIONS = {
        "loc": 'upper center',
        "bbox_to_anchor": (0.5, -0.125),
        "fancybox": False,
        "shadow": False,
        "ncol": 3
    }

    def __init__(self, figsize=None, dpi=None):
        self.plt = plt
        self.fig, self.a_x = self.plt.subplots(figsize=figsize, dpi=dpi)

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
        self.add_simple_plot(v_y_1, label + " (Inicial)", **options, **cont)
        self.add_simple_plot(v_y_2, label + " (Final)", **options, **dash)

    def set_labels(self, x_label=None, y_label=None):
        if x_label is not None:
            self.a_x.set_xlabel(x_label)
        if y_label is not None:
            self.a_x.set_ylabel(y_label)

    def set_xticks(self, ticks):
        self.a_x.set_xticks(ticks)

    def set_yticks(self, ticks):
        self.a_x.set_yticks(ticks)

    def set_title(self, title):
        self.a_x.set_title(title)

    def set_legend(self, options):
        self.a_x.legend(**{**self.DEFAULT_LEGEND_OPTIONS, **options})

    def modify_height(self, perc):
        box = self.a_x.get_position()
        self.a_x.set_position([
            box.x0, box.y0 + box.height * (1.0 - perc),
            box.width, box.height * perc
        ])

    def display(self, outfile=None, mplbackend="svg", fastmode=False):
        matplotlib.use(mplbackend)
        if fastmode:
            mplstyle.use('fast')
        else:
            self.fig.tight_layout()

        if outfile:
            self.fig.savefig(outfile)
        else:
            self.plt.show()
        self.plt.close()
