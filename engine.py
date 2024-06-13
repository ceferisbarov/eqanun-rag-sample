import os
import pickle
import faiss
from tqdm import tqdm
from datasets import load_dataset
from sentence_transformers import SentenceTransformer
import numpy as np
from copy import deepcopy

from dotenv import load_dotenv
load_dotenv()
os.makedirs("embeddings", exist_ok=True)
BATCH_SIZE = 2
CHUNK_SIZE = 1024
DOCUMENTS = {"Əmək Məcəlləsi": ["46943", None], 
             "Vergi Məcəlləsi": ["46948", None],
             "Cinayət Məcəlləsi": ["46947", None]}
indices = []
model = SentenceTransformer("BAAI/bge-m3")
print("Loaded the embedding model...")

repo = "allmalab/eqanun"
# doc_id = os.environ["DOCUMENT_ID"]
dataset = load_dataset(repo, cache_dir="hf_cache")
for doc_name, doc_id in tqdm(DOCUMENTS.items()):
    doc_text = dataset["train"].filter(lambda x: x["id"] == doc_id[0])["text"][0]
    print(len(doc_text))
    print("*********************")
    chunks = [doc_text[i:i+CHUNK_SIZE] for i in range(0, len(doc_text), CHUNK_SIZE)]
    print(len(doc_text))
    print("*********************")
    print("Loaded the text corpus...")

    embedding_file = os.path.join("embeddings", f"{doc_id[0]}.pickle")
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
    print("Loaded or created embeddings...")

    dim = final_embeddings.shape[-1]
    DOCUMENTS[doc_name][1] = faiss.IndexFlatL2(dim)
    DOCUMENTS[doc_name][1].add(final_embeddings)
    print(f"Index is ready. Number of entries: {DOCUMENTS[doc_name][1].ntotal}")

def faiss_search(query, index, n_neighbors=5):
    query_embedding = model.encode(query).reshape(1,-1)
    distances, indices = index.search(query_embedding, n_neighbors)

    return [chunks[i] for i in indices[0]]
