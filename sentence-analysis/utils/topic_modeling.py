import pandas as pd


def analyze_csv(file_storage):

    df = pd.read_csv(file_storage.stream)
    
    return df.head()
