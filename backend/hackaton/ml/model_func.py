from catboost import CatBoostClassifier, Pool
import numpy as np
import pandas as pd
from transformers import AutoModel
from sqlalchemy import create_engine

class Dataset:
    def __init__(self, user, password, db, server, port, table):
        self.engine = (f"postgresql://{user}:{password}@{server}:{port}/{db}")
        self.table = table
    def get_df(self, columns):
        df = pd.read_sql(f"SELECT {','.join(columns)} FROM {self.table} LIMIT 100", self.engine)
        return df

class Model:
    def __init__(self, model_name, dataset):
        new_m = CatBoostClassifier()
        self.new_w = new_m.load_model(model_name)
        self.dataset = dataset
        self.model = AutoModel.from_pretrained('jinaai/jina-embeddings-v2-base-code', max_length=256, trust_remote_code=True)

    def get_predictions(self, columns):
        df = self.dataset.get_df(columns)
        train_dataset = pd.DataFrame(
            df.columns.tolist(),
            columns=["name_column"]
        )
        features = []
        for name_col in train_dataset.name_column:
            features.append(",".join(df[name_col].astype(str).values))
        list_embeddings = []
        for s in features:
            emb = self.model.encode([s])
            list_embeddings.append(emb)
        arr_embeddings = np.concatenate(list_embeddings)
        res = self.new_w.predict(arr_embeddings)
        res_dict = {}
        for i in range(len(columns)):
            res_dict[columns[i]] = bool(res[i])
        return res_dict


# d = Dataset("postgres", "R5O{vtoovFV8(2K£", "hackathon", "147.45.226.188", "5432", "addresses")
# m = Model("model", d)
# a = ["street", "house"]
# m.get_predictions(a)

