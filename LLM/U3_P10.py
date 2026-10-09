from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, StorageContext, load_index_from_storage
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from dotenv import load_dotenv
import os, logging

try: 
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
        handlers=[logging.FileHandler("U3_P10.log")],   
        force=True
    )

    load_dotenv()

    api_key=os.getenv("GEMINI_API_KEY")

    if api_key:
        Settings.llm=GoogleGenAI(model="gemini-3.5-flash-lite", api_key=api_key)
        Settings.embed_model=GoogleGenAIEmbedding(model_name="gemini-embedding-001", api_key=api_key)
        logging.log(level=20, msg="Embedding model and LLM model settings configured.")
    Settings.chunk_size=550
    Settings.chunk_overlap=50

    PERSIST_DIR = "./U3_P10_storage"

    if not os.path.exists(PERSIST_DIR):
        logging.log(level=20, msg="Creating the indexed storage.")
        documents = SimpleDirectoryReader("U3_P10_data").load_data()
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist(persist_dir=PERSIST_DIR)
    
    else:
        logging.log(level=20, msg="Loadding data from the indexed storage.")
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(storage_context)

    query_engine = index.as_query_engine()
    if query_engine:
        logging.log(level=20, msg="Query engine set.")

    while True:
        prompt = input("\nEnter query: ").strip()
        if prompt == "" or not prompt:
            print("ERROR: Invalid query! try again.")
        else:
            if prompt.lower() == "exit":
                break
            else:
                response = query_engine.query(prompt)
                print("AI:",response)

except Exception as e:
    print("\n\nERROR:",e)