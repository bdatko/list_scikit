"""
Module to create the venn diagram
"""
from pathlib import Path
from typing import Union

import fire
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib_venn import venn2

from list_scikit import MY_LIST_DICT

FONT = {"family": "serif", "size": 22}

matplotlib.rc("font", **FONT)


def create_venn_figure(source_data: Union[Path, str], output_file: Union[Path, str]):
    libraries = pd.read_csv(source_data)
    fig, ax = plt.subplots(figsize=(12, 12))
    v = venn2(
        [set(libraries["library"].to_list()), set(MY_LIST_DICT.keys())],
        ("Scikit-learn Related Project Official", "My List"),
        ax=ax,
    )
    fig.savefig(
        output_file,
        bbox_inches="tight",
        facecolor=fig.get_facecolor(),
        dpi=600,
    )


if __name__ == "__main__":
    fire.Fire(
        {
            "create_venn_figure": create_venn_figure,
        }
    )
