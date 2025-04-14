from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings
import os
from langchain_core.vectorstores import InMemoryVectorStore

load_dotenv()


if __name__ == "__main__":
    api_key = os.getenv("OPEN_AI_API_KEY")
    if api_key is None:
        print("Please set environment variable OPEN_AI_API_KEY")
        exit(1)

    file_path = "C:/Users/umaru/Downloads/Nike10k2021.pdf"  # ✅ Valid local file path
    loader = PyPDFLoader(file_path)


    docs = loader.load()



    # Split documents into small pieces called chunks that are co-related to each other
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )
    all_splits = text_splitter.split_documents(docs)
    print(f"Total splits created: {len(all_splits)}")

    #  creating embeddings
    ms_token = os.getenv("MISTRAL_API_KEY")
    # embeddings = MistralAIEmbeddings(model="mistral-embed")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    # vector_1 = embeddings.embed_query(all_splits[0].page_content)
    # vector_2 = embeddings.embed_query(all_splits[1].page_content)

    # Store all the embeddings in memory
    vector_store = InMemoryVectorStore(embeddings)
    ids = vector_store.add_documents(documents=all_splits)

    # searching via similarity search
    results = vector_store.similarity_search(
        "How many distribution centers does Nike have in the UK?"
    )

    print(results[0].page_content)

    # searching via similarity search
    results = vector_store.similarity_search(
        "what are the total sales in UK?"
    )

    print(results[0].page_content)