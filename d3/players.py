import numpy as np
import pandas as pd
import uuid


def makeDF(filepath):
    with open(filepath) as f:
        lines = f.readlines()
    for index, item in enumerate(lines):
        lines[index] = item.split('\t')
    columns = lines[0]
    df = pd.DataFrame(lines[1:], columns=columns)
    df.to_csv('~/d3out/players.csv')
    return df

