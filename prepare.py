"""
Module to prepare the data
"""
import re
from pathlib import Path
from typing import Union

import fire
import pandas as pd


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


if __name__ == "__main__":
    fire.Fire({"create_scikit_offical": create_scikit_offical})
