import os
import time
from pathlib import Path
from dotenv import load_dotenv
from tqdm.auto import tqdm
from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai._common import GoogleGenerativeAIError

# Load environment variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = "us-east-1"
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "medicalindex")

# Check if API key exists before setting it
if GOOGLE_API_KEY:
    os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
else:
    raise ValueError("GOOGLE_API_KEY environment variable is not set. Please set it before running the application.")

# Upload directory
UPLOAD_DIR = "./uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
spec = ServerlessSpec(cloud="aws", region=PINECONE_ENV)
existing_indexes = [i["name"] for i in pc.list_indexes()]

if PINECONE_INDEX_NAME not in existing_indexes:
    print(f"📦 Creating Pinecone index: {PINECONE_INDEX_NAME}")
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=768,
        metric="dotproduct",
        spec=spec
    )
    while not pc.describe_index(PINECONE_INDEX_NAME).status["ready"]:
        time.sleep(1)

index = pc.Index(PINECONE_INDEX_NAME)

# Initialize embedding model once (outside function)
embed_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")


def safe_embed(texts, retries=3, delay=3):
    """Embed documents with retry logic in case of API errors."""
    for attempt in range(1, retries + 1):
        try:
            return embed_model.embed_documents(texts)
        except GoogleGenerativeAIError as e:
            print(f"⚠️ Embedding failed (attempt {attempt}/{retries}): {e}")
            time.sleep(delay)
    raise RuntimeError("Embedding failed after multiple retries")


def batch_list(lst, batch_size=20):
    """Split a list into smaller batches"""
    for i in range(0, len(lst), batch_size):
        yield lst[i:i + batch_size]


def load_vectorstore(uploaded_files):
    """Load, split, embed, and upsert PDF content into Pinecone"""
    file_paths = []

    # Save uploaded files locally
    for file in uploaded_files:
        save_path = Path(UPLOAD_DIR) / file.filename
        with open(save_path, "wb") as f:
            f.write(file.file.read())
        file_paths.append(str(save_path))

    # Process each PDF
    for file_path in file_paths:
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=50)
        chunks = splitter.split_documents(documents)

        texts = [chunk.page_content for chunk in chunks]
        # metadatas = [{"text": chunk.page_content, "source": str(Path(file_path))} for chunk in chunks]
        metadatas = [{"text": chunk.page_content, "source": str(Path(file_path))} for chunk in chunks]

        ids = [f"{Path(file_path).stem}-{i}" for i in range(len(chunks))]

        print(f"🔍 Embedding {len(texts)} chunks...")

        # Embed in batches
        embeddings = []
        for text_batch in batch_list(texts, batch_size=20):
            embeddings.extend(safe_embed(text_batch))

        print("📤 Uploading to Pinecone...")
        with tqdm(total=len(embeddings), desc="Upserting to Pinecone") as progress:
            for i, (vec_id, emb, meta) in enumerate(zip(ids, embeddings, metadatas)):
                index.upsert(vectors=[(vec_id, emb, meta)])
                progress.update(1)

        print(f"✅ Upload complete for {file_path}")
