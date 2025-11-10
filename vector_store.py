from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader, TextLoader
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY not found in environment variables")

rag_initialized = False
vector_store = None
retriever = None

def load_documents():
    docs = []
    current_directory = os.path.dirname(__file__)
    data_dir = os.path.join(current_directory, "data")

    pdf_path = os.path.join(data_dir, "rules.pdf")
    if os.path.isfile(pdf_path):
        pdf_loader = PyPDFLoader(pdf_path)
        pdf_docs = pdf_loader.load()
        if pdf_docs:
            docs.extend(pdf_docs)
            print(f"✅ Loaded {len(pdf_docs)} pages from rules.pdf")
        else:
            print("⚠️ No content loaded from rules.pdf")

    md_loader = DirectoryLoader(data_dir, glob="**/*.md", loader_cls=TextLoader,loader_kwargs={"encoding": "utf-8"})
    md_docs = md_loader.load()
    if md_docs:
        docs.extend(md_docs)
        print(f"✅ Loaded {len(md_docs)} MD documents (OWASP, PEP8, Big-O guides)")
    else:
        print("⚠️ No MD files found in data/ – ensure owasp_security.md, pep8_syntax.md, bigo_performance.md exist")

    if not docs:
        raise ValueError("❌ No documents loaded from data/ folder (PDF or MD files)")

    return docs

def init_rag():
    global rag_initialized, vector_store, retriever
    if rag_initialized:
        print("ℹ️ RAG already initialized")
        return

    docs = load_documents()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = text_splitter.split_documents(docs)
    if not split_docs:
        raise ValueError("❌ Text splitter produced no chunks")

    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        google_api_key=GOOGLE_API_KEY,
    )

    vector_store = FAISS.from_documents(split_docs, embeddings)
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})

    print("✅ RAG index initialized with code best practices (rules.pdf + OWASP/PEP8/Big-O MDs)")
    rag_initialized = True