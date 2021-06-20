"""
Module to create the post
"""
from pathlib import Path
from typing import Union

import fire
import pandas as pd
from mdutils.mdutils import MdUtils
from mdutils.tools import Html

from list_scikit import MY_LIST_DICT


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
            "create_post": create_post,
        }
    )
