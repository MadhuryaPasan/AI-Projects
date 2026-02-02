from langchain.agents.middleware import dynamic_prompt, ModelRequest
from langchain_pymupdf4llm import PyMuPDF4LLMLoader
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import asyncio
from dotenv import load_dotenv
from langchain_ollama import OllamaEmbeddings
load_dotenv()

from pathlib import Path
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)



MODEL_NAME = os.getenv("MODEL_NAME") or ""
BASE_URL = os.getenv("BASE_URL") or ""
API_KEY = os.getenv("API_KEY") or "" 
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL") or ""


embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)


async def load_all_pdfs(paths):
    all_docs = []
    for path in paths:
        loader = PyMuPDF4LLMLoader(file_path=path)
        # aload() returns a list of documents for one PDF
        pdf_docs = await loader.aload()
        all_docs.extend(pdf_docs)
    return all_docs


embedding_dim = len(embeddings.embed_query("hello world"))
index = faiss.IndexFlatL2(embedding_dim)

vector_store = FAISS(
    embedding_function=embeddings,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={},
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # chunk size (characters)
    chunk_overlap=200,  # chunk overlap (characters)
    add_start_index=True,  # track index in original document
)

async def main():
    pdf_paths = [str(UPLOAD_DIR / f.name) for f in UPLOAD_DIR.iterdir() if f.suffix == ".pdf"]
    print(f"Loading files: {pdf_paths}")

    docs = await load_all_pdfs(pdf_paths)
    print(f"Loaded {len(docs)} pages")

    all_splits = text_splitter.split_documents(docs)
    print(f"Created {len(all_splits)} chunks")

    document_ids = vector_store.add_documents(documents=all_splits)
    print(f"Added {len(document_ids)} documents to vector store")


if __name__ == "__main__":
    asyncio.run(main())


@dynamic_prompt
def prompt_with_context(request: ModelRequest) -> str:
    """Inject context into state messages."""
    last_query = request.state["messages"][-1].text
    retrieved_docs = vector_store.similarity_search(last_query)

    docs_content = "\n\n".join(doc.page_content for doc in retrieved_docs)
    system_message = (
        "You are a helpful assistant. Use the following context in your response:"
        f"\n\n{docs_content}"
    )

    return system_message