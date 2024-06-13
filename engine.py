import os
import pickle
import faiss
from tqdm import tqdm
from datasets import load_dataset
# from huggingface_hub import login
from sentence_transformers import SentenceTransformer
import numpy as np

from dotenv import load_dotenv
load_dotenv()
BATCH_SIZE = 2
CHUNK_SIZE = 1024
model = SentenceTransformer("BAAI/bge-m3")

repo = "allmalab/eqanun"
dataset = load_dataset(repo)
labor_code = dataset["train"].filter(lambda x: x["id"] == "46943")["text"][0]
labor_code = [labor_code[i:i+CHUNK_SIZE] for i in range(0, len(labor_code), CHUNK_SIZE)]

if not os.path.exists("embeddings.pickle"):
    embeddings_list = []
    for i in tqdm(range(0, len(labor_code), CHUNK_SIZE)):
        text = labor_code[i:i+CHUNK_SIZE]
        embeddings = model.encode(text)
        embeddings_list.append(embeddings.reshape(1,-1))
    final_embeddings = np.concatenate(embeddings_list, axis=0)

    with open('embeddings.pickle', 'wb') as handle:
        pickle.dump(final_embeddings, handle, protocol=pickle.HIGHEST_PROTOCOL)

else:
    with open('embeddings.pickle', 'rb') as handle:
        final_embeddings = pickle.load(handle)

dim = final_embeddings.shape[-1]
index = faiss.IndexFlatL2(dim)
index.add(final_embeddings)

def faiss_search(query, index=index, n_neighbors=5):
    query_embedding = model.encode(query).reshape(1,-1)
    distances, indices = index.search(query_embedding, n_neighbors)

    return [labor_code[i] for i in indices[0]]

