"""Registry of algorithm names for `rllib train --run=<alg_name>`"""


def _import_naf():
    from raylab.algorithms.naf.naf import NAFTrainer

    return NAFTrainer


def _import_svg_inf():
    from raylab.algorithms.svg.svg_inf import SVGInfTrainer

    return SVGInfTrainer


ALGORITHMS = {"NAF": _import_naf, "SVG(inf)": _import_svg_inf}
