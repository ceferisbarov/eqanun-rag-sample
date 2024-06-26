import os
import pickle
import faiss
from tqdm import tqdm
from datasets import load_dataset
from sentence_transformers import SentenceTransformer
import numpy as np

from sentence_tokenizer_aze.tokenizer import sent_tokenize_aze

from dotenv import load_dotenv
load_dotenv()

os.makedirs("embeddings", exist_ok=True)

BATCH_SIZE = 2
CHUNK_SIZE = 4096
model = SentenceTransformer("BAAI/bge-m3")
print("Loaded the embedding model...")

def split_text(text):
    # TODO: Replace this with a more advanced algorithm
    sentences = sent_tokenize_aze(text.strip())
    combined_sentences = []
    current_sentence = ""
    for sentence in sentences:
        # Check if adding the next sentence would exceed the max length
        if len(current_sentence) + len(sentence) + 1 <= CHUNK_SIZE:  # +1 for the space
            if current_sentence:  # if current_sentence is not empty
                current_sentence += " " + sentence
            else:
                current_sentence = sentence
        else:
            # Append the current combined sentence to the list
            combined_sentences.append(current_sentence)
            # Start a new combined sentence with the current sentence
            current_sentence = sentence
    
    # Don't forget to add the last combined sentence to the list
    if current_sentence:
        combined_sentences.append(current_sentence)
    
    return combined_sentences

repo = "allmalab/eqanun"
doc_id = os.environ["DOCUMENT_ID"]
dataset = load_dataset(repo, cache_dir="hf_cache")
doc_text = dataset["train"].filter(lambda x: x["id"] == doc_id)["text"][0]
chunks = split_text(doc_text)
print("Loaded the text corpus...")

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
print("Loaded or created embeddings...")

dim = final_embeddings.shape[-1]
index = faiss.IndexFlatL2(dim)
index.add(final_embeddings)
print(f"Index is ready. Number of entries: {index.ntotal}")

def faiss_search(query, index=index, n_neighbors=5):
    query_embedding = model.encode(query).reshape(1,-1)
    distances, indices = index.search(query_embedding, n_neighbors)

    return [chunks[i] for i in indices[0]]
