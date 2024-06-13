import os
import pickle
import faiss
from tqdm import tqdm
from datasets import load_dataset
from sentence_transformers import SentenceTransformer
import numpy as np

from dotenv import load_dotenv
load_dotenv()
BATCH_SIZE = 2
CHUNK_SIZE = 1024
model = SentenceTransformer("BAAI/bge-m3")

repo = "allmalab/eqanun"
doc_id = os.environ["DOCUMENT_ID"]
dataset = load_dataset(repo)
doc_text = dataset["train"].filter(lambda x: x["id"] == doc_id)["text"][0]
chunks = [doc_text[i:i+CHUNK_SIZE] for i in range(0, len(doc_text), CHUNK_SIZE)]

embedding_file = os.path.join("embeddings", f"{doc_id}.pickle")
if os.path.exists(embedding_file):
    with open(embedding_file, 'rb') as handle:
        final_embeddings = pickle.load(handle)
else:
    embeddings_list = []
    for chunk in tqdm(chunks):
        embeddings = model.encode(chunk)
        embeddings_list.append(embeddings.reshape(1,-1))
    final_embeddings = np.concatenate(embeddings_list, axis=0)

    with open(embedding_file, 'wb') as handle:
        pickle.dump(final_embeddings, handle, protocol=pickle.HIGHEST_PROTOCOL)

dim = final_embeddings.shape[-1]
index = faiss.IndexFlatL2(dim)
index.add(final_embeddings)

print(f"Index is ready. Number of entries: {index.ntotal}")

def faiss_search(query, index=index, n_neighbors=5):
    query_embedding = model.encode(query).reshape(1,-1)
    distances, indices = index.search(query_embedding, n_neighbors)

    return [chunks[i] for i in indices[0]]
