import pickle
from pathlib import Path
import pandas as pd
import streamlit as st
from datetime import datetime


def load_file(path: str) -> pd.DataFrame:
    try:
        with open(path, "rb") as f:
            dataset = pickle.load(f)
        return dataset
    except Exception as e:
        st.error(f"Error loading {path}: {e}")
        return None


@st.cache_data
def load_data(folder: str) -> pd.DataFrame:
    files = [file for file in Path(folder).iterdir() if file.suffix == '.pkl']
    if not files:
        st.warning(f"No .pkl files found in folder: {folder}")
        return pd.DataFrame() 
    
    all_datasets = [load_file(file) for file in files]
    
    all_datasets = [dataset for dataset in all_datasets if dataset is not None]

    if not all_datasets:
        st.warning(f"All .pkl files failed to load in folder: {folder}")
        return pd.DataFrame()
    for i in all_datasets :
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_csv = f"dataset/merged_data_{timestamp}.csv"
        i.to_csv(output_csv, index=False)
    
    st.write(f"Data from {folder} saved as {output_csv}")
    
    return all_datasets


dataset_folder = "dataset"
df = load_data(f"./data")

st.dataframe(df)
