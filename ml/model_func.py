from catboost import CatBoostClassifier, Pool
import numpy as np
import pandas as pd
from transformers import AutoModel
from sqlalchemy import create_engine

class Dataset:
    def __init__(self, user, password, db, server, port, table):
        self.engine = (f"postgresql:///?User={user}&;Password={password}&Database={db}&Server={server}&Port={port}")
        self.table = table
    def get_df(self):
        df = pd.read_sql(f"SELECT * FROM {self.table}", self.engine)
        return df

class Model:
    def __init__(self, model_name, dataset):
        new_m = CatBoostClassifier()
        self.new_w = new_m.load_model(model_name)
        self.dataset = dataset

    def get_predictions(columns):
        model = AutoModel.from_pretrained('jinaai/jina-embeddings-v2-base-code', max_length=256, trust_remote_code=True)
        df = self.dataset.get_df()
        train_dataset = pd.DataFrame(
            df.columns.tolist(),
            columns=["name_column"]
        )
        features = []
        for name_col in train_dataset.name_column:
            if name_col in columns:
                features.append(",".join(df[name_col].astype(str).values) )
        list_embeddings = []
        for s in features[:100]:
            emb = model.encode([s])
            list_embeddings.append(emb)
        arr_embeddings = np.concatenate(list_embeddings)
        res = self.new_w.predict(arr_embeddings)
        res_dict = {}
        for i in range(len(columns)):
            res_dict[columns[i]] = bool(res[i])
    return res_dict


