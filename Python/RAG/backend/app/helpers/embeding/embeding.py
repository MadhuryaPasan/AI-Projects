#=======================================
import pymupdf.layout # always add this before PyMuPDF4LLMLoader
from langchain_pymupdf4llm import PyMuPDF4LLMLoader
#========================================
from langchain.agents.middleware import dynamic_prompt, ModelRequest
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import asyncio
from dotenv import load_dotenv
from langchain_ollama import OllamaEmbeddings
from pathlib import Path

load_dotenv()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

MODEL_NAME = os.getenv("MODEL_NAME") or ""
BASE_URL = os.getenv("BASE_URL") or ""
API_KEY = os.getenv("API_KEY") or "" 
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL") or ""

embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
vector_store = None

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=5000,  # chunk size (characters)
    chunk_overlap=500,  # chunk overlap (characters)
    add_start_index=True,  # track index in original document
)

async def load_all_pdfs(paths):
    all_docs = []
    for path in paths:
        loader = PyMuPDF4LLMLoader(file_path=path)
        # aload() returns a list of documents for one PDF
        pdf_docs = await loader.aload()
        all_docs.extend(pdf_docs)
    return all_docs

async def initialize_vector_store():
    global vector_store
    try:
        print("Initializing vector store...")
        # Determine embedding dimension dynamically
        # This requires the Ollama server to be up
        test_embed = embeddings.embed_query("hello world")
        embedding_dim = len(test_embed)
        
        index = faiss.IndexFlatL2(embedding_dim)
        
        vector_store = FAISS(
            embedding_function=embeddings,
            index=index,
            docstore=InMemoryDocstore(),
            index_to_docstore_id={},
        )
        
        pdf_paths = [str(UPLOAD_DIR / f.name) for f in UPLOAD_DIR.iterdir() if f.suffix == ".pdf"]
        print(f"Loading files: {pdf_paths}")

        if pdf_paths:
            docs = await load_all_pdfs(pdf_paths)
            print(f"Loaded {len(docs)} pages")

            all_splits = text_splitter.split_documents(docs)
            print(f"Created {len(all_splits)} chunks")

            if all_splits:
                document_ids = vector_store.add_documents(documents=all_splits)
                print(f"Added {len(document_ids)} documents to vector store")
        else:
             print("No PDF files found to ingest.")

    except Exception as e:
        print(f"Failed to initialize vector store: {e}")
        # vector_store remains None or partially init
        # Safe to leave it None so checks fail gracefully


@dynamic_prompt
def prompt_with_context(request: ModelRequest) -> str:
    """Inject context into state messages."""
    if vector_store is None:
        print("Warning: Vector store not initialized. Returning default prompt.")
        return "You are a helpful assistant."

    last_query = request.state["messages"][-1].text
    try:
        retrieved_docs = vector_store.similarity_search(last_query, k=15)
        docs_content = "\n\n".join(doc.page_content for doc in retrieved_docs)
        system_message = (
            "You are a helpful assistant."
            "Use the provided context to answer the user's question when relevant."
            "If the context does not contain the answer, respond honestly.\n\n"
            f"Context:\n{docs_content}"
        )
        # print(system_message)
        return system_message
    except Exception as e:
        print(f"Error during retrieval: {e}")
        return "You are a helpful assistant."


if __name__ == "__main__":
    asyncio.run(initialize_vector_store())
