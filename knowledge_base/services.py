import os
import hashlib
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredExcelLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from django.conf import settings

class DocumentProcessor:
    def __init__(self):
        self.chunk_size = 1000
        self.chunk_overlap = 200

    def compute_hash(self, file_path):
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def load_document(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.pdf':
            loader = PyPDFLoader(file_path)
        elif ext in ['.docx', '.doc']:
            loader = Docx2txtLoader(file_path)
        elif ext in ['.xlsx', '.xls']:
            loader = UnstructuredExcelLoader(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
        return loader.load()

    def process(self, file_path, extra_metadata=None):
        docs = self.load_document(file_path)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, 
            chunk_overlap=self.chunk_overlap
        )
        splits = text_splitter.split_documents(docs)
        
        # Add metadata
        if extra_metadata:
            for split in splits:
                split.metadata.update(extra_metadata)
                
        return splits

class VectorStoreService:
    def __init__(self):
        self.persist_directory = os.path.join(settings.BASE_DIR, 'chroma_db')
        # Use Google API Key
        api_key = os.getenv("GOOGLE_API_KEY", "") 
        self.embedding_function = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=api_key) if api_key else None
        
    def get_vectorstore(self):
        if not self.embedding_function:
            raise ValueError("Google API Key not set")
            
        return Chroma(
            persist_directory=self.persist_directory, 
            embedding_function=self.embedding_function
        )

    def add_documents(self, splits):
        vectorstore = self.get_vectorstore()
        vectorstore.add_documents(documents=splits)

    def add_text(self, text, metadata=None):
        """Adds a raw text string directly to the vector store."""
        from langchain_core.documents import Document
        if metadata is None:
            metadata = {}
        
        doc = Document(page_content=text, metadata=metadata)
        self.add_documents([doc])

    def similarity_search(self, query, k=5, filter=None):
        vectorstore = self.get_vectorstore()
        # Chroma expects filter in the format: {'key': 'value'} or {'key': {'$in': ['a', 'b']}}
        # But for basic usage, just passing the dict works.
        return vectorstore.similarity_search(query, k=k, filter=filter)
