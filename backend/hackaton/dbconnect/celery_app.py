import json
import os
import time

import redis

import pandas as pd
import numpy as np
import torch
from catboost import CatBoostClassifier, Pool
from transformers import AutoModel
from tqdm.notebook import tqdm

from sklearn.utils.class_weight import compute_class_weight
from sklearn.model_selection import train_test_split

from .models import DatabaseConnection


def learn_model():
    print("start learning")
    r = redis.Redis(host=os.environ.get("REDIS_HOST"), port=os.environ.get("REDIS_PORT"))
    model_name = r.get('current_model')
    new_model_name = "model"+str(int(model_name[-1])+1%10)
    df = pd.read_csv(os.environ.get("DATA_DIR")+"train.csv")
    print(df.columns.tolist())
    name_columns = pd.read_csv(os.environ.get("DATA_DIR")+"train_labels.csv")

    train_dataset = pd.DataFrame(
        zip(df.columns.tolist(), name_columns.label.values.tolist()),
        columns=["name_column", "type_column"]
    )
    train_dataset["label"] = (train_dataset.type_column != "Other_data").astype(int)

    last_connections = DatabaseConnection.objects.all()
    for last_connection in last_connections:
        url = last_connection.url
        port = last_connection.port
        user = last_connection.user
        password = last_connection.password
        engine = (f"postgresql://{user}:{password}@{url}:{port}/hackathon")
        features = [",".join(df[name_col].astype(str).values) for name_col in train_dataset.name_column]
        saved_data = last_connection.saved_data
        if "tables" in  saved_data:
            for table in saved_data["tables"]:
                for column in saved_data["tables"]["columns"]:
                    df1 = pd.read_sql(f"SELECT {column["name"]} FROM {table["tableName"]}", engine)
                    df1["label"] = column["mask"].astype(int)
                    features.append(",".join(df1[column["name"]].astype(str).values))
        model = AutoModel.from_pretrained('jinaai/jina-embeddings-v2-base-code', max_length=256, trust_remote_code=True)
        list_embeddings = []
        for s in tqdm(features):
            emb = model.encode([s])
            list_embeddings.append(emb)
        arr_embeddings = np.concatenate(list_embeddings)
        X_train, X_test, y_train, y_test = train_test_split(arr_embeddings, train_dataset.label, test_size=0.1)
        weights = compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)
        model = CatBoostClassifier(
            iterations=1000,
            depth=2,
            learning_rate=0.01,
            loss_function='Logloss',
            eval_metric='AUC',
            class_weights=weights,
            od_type="Iter",
            od_wait=300
        )
        model.fit(
            X_train,
            y_train,
            eval_set=(X_test, y_test),
            use_best_model=True,
            # cat_features=f_cat, f_cat - индексы колонок с категорилаьными фичи
            plot=True,
            metric_period=100,
            verbose=True
        )
        model.save_model(new_model_name)
        r.set('current_model', 'new_model_name')
    else:
        return



