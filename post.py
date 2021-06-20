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
from mdutils.mdutils import MdUtils
from mdutils.tools import Html

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


def create_post(source_data: Union[Path, str], output_file: str):
    libraries = pd.read_csv(source_data)
    libraries = libraries["library"].to_list()
    mdFile = MdUtils(
        file_name=output_file,
        title="",
    )
    mdFile.new_header(
        level=2,
        title="Zoo of scikit-learn related projects",
        style="setext",
        add_table_of_contents="n",
    )
    mdFile.new_paragraph(
        "With the popularity of `scikit-learn` many projects follow a similar API to ensure compatibility. The developers of `scikit-learn` recognize this trend and list various related projects: [Related projects](https://scikit-learn.org/stable/related_projects.html), [scikit-learn-contrib](https://github.com/scikit-learn-contrib), [scikit-learn-contrib repo](https://github.com/scikit-learn-contrib/scikit-learn-contrib)."
    )
    mdFile.new_paragraph(
        "I have found a few projects both on and off the list from SciKit's official aggregation."
    )
    mdFile.new_paragraph(
        Html.image(path="data/venn.png", size="600x400", align="center")
    )
    mdFile.new_paragraph(
        "Below is my list of just the differences from the above venn diagram:"
    )
    mdFile.new_paragraph(
        "\n".join(
            [
                "* " + MY_LIST_DICT[key]
                for key in list(set(MY_LIST_DICT.keys()) - set(libraries))
            ]
        )
    )
    mdFile.new_paragraph("Finally the full list of projects:")
    mdFile.new_paragraph("\n".join(["* " + value for _, value in MY_LIST_DICT.items()]))
    mdFile.create_md_file()


if __name__ == "__main__":
    fire.Fire(
        {
            "create_scikit_offical": create_scikit_offical,
            "create_venn_figure": create_venn_figure,
            "create_post": create_post,
        }
    )
