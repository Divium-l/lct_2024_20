from celery import Celery
from backend.hackaton.dbconnect.views import saved_data
app = Celery('ml_learn', broker='redis://localhost')

import pandas as pd
import numpy as np
import torch
import plot_helper
from catboost import CatBoostClassifier, Pool
from transformers import AutoModel
from tqdm.notebook import tqdm

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn import metrics
from sklearn.utils.class_weight import compute_class_weight

import warnings

warnings.filterwarnings('ignore')


@app.task
def learn_model(saved_data):
    df = pd.read_csv("data/train.csv")
    print(df.columns.tolist())
    name_columns = pd.read_csv("data/train_labels.csv")
    train_dataset = pd.DataFrame(
        zip(df.columns.tolist(), name_columns.label.values.tolist()),
        columns=["name_column", "type_column"]
    )
    train_dataset["label"] = (train_dataset.type_column != "Other_data").astype(int)

