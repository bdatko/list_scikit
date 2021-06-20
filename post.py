"""
Module to create the post
"""
import re
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


def create_scikit_offical(source_data: Union[Path, str], output_file: Union[Path, str]):
    with open(source_data) as file:
        data = file.read()

    x = re.findall("(?<=- `)[\s\S]*?(?=<)", data)
    res = list(x)
    res = [i.replace("\n", "") if "\n" in i else i for i in res]
    res = [i.strip() for i in res]
    res.remove("Chinese translation")
    res.remove("Persian translation")

    libraries = pd.DataFrame(res, columns=["library"])
    libraries.to_csv(output_file, index=False)


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


def create_post(source_data: Union[Path, str], output_file: Union[Path, str]):
    pass


if __name__ == "__main__":
    fire.Fire(
        {
            "create_scikit_offical": create_scikit_offical,
            "create_venn_figure": create_venn_figure,
        }
    )
