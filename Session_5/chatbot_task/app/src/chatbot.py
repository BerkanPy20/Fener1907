

import chromadb
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
from langchain_core.documents.base import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, Runnable
from langchain_chroma import Chroma
from chromadb.api import ClientAPI
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import requests
import re
from uuid import uuid4
from typing import List
import logging
import os
from langchain_core.runnables import RunnableLambda

# Hint: Use these variables in your tasks
OLLAMA_HOST_NAME = os.environ.get("OLLAMA_HOST_NAME", "localhost")
CHROMA_HOST_NAME = os.environ.get("CHROMA_HOST_NAME", "localhost")
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "bge-m3")
MODEL_NAME = os.environ.get("MODEL_NAME", "llama3.2:1B")
PDF_DOC_PATH = os.environ.get("PDF_DOC_PATH", "src/AI_Book.pdf")
COLLECTION_NAME = os.environ.get("COLLECTION_NAME", "ai_model_book")

logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more details
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Console logs
    ],
)

logger = logging.getLogger(__name__)

class CustomChatBot:
    """
    A class representing a chatbot that uses a ChromaDB client for document retrieval
    and the ChatOllama model for generating answers.

    This chatbot uses a retrieval-augmented generation (RAG) pipeline where it retrieves
    relevant information from a custom document database (ChromaDB) and then generates
    concise answers using a language model (ChatOllama).
    """

    def __init__(self, index_data: bool, pull_embedding_model: bool) -> None:
        """
        Initialize the CustomChatBot class by setting up the ChromaDB client for document retrieval
        and the ChatOllama language model for answer generation.
        """

        # Initialize the embedding function for document retrieval
        if pull_embedding_model:
            logger.info(f"Pulling embedding model{EMBEDDING_MODEL} now.")
            self._pull_embedding_model()

        # Task: initialize the embedding model
        self.embedding_function = OllamaEmbeddings(
    model=EMBEDDING_MODEL,
    base_url=f"http://{OLLAMA_HOST_NAME}:11434",
)

        # Initialize the ChromaDB client
        self.client = self._initialize_chroma_client()
        
        # Get or create the document collection in ChromaDB
        self.vector_db = self._initialize_vector_db()

        # Process pdf, embedd data and index to ChromaDB
        if index_data:
            logger.info(f"Index data to chroma db now.")
            self._index_data_to_vector_db()

        # Task: Initialize the document retriever
        self.retriever = (
            self.vector_db.as_retriever(
                search_kwargs={"k": 12}
            )
                        | RunnableLambda(self._unique_docs).with_config(
                run_name="unique_docs"
            )
        )


        # Task: Initialize the large language model (LLM) from Ollama
        self.llm = ChatOllama(
    model=MODEL_NAME,
    base_url=f"http://{OLLAMA_HOST_NAME}:11434",
    temperature=0,
)

        # Set up the retrieval-augmented generation (RAG) pipeline
        self.qa_rag_chain = self._initialize_qa_rag_chain()

    def _pull_embedding_model(self):
        logger.info(f"Pull embedding model {EMBEDDING_MODEL}")
        try:

            response = requests.post(f"http://{OLLAMA_HOST_NAME}:11434/api/pull", json = {"name": EMBEDDING_MODEL,  "stream": False})
            response.raise_for_status()
            logger.info(response.json())
        except:
            raise

    def _initialize_chroma_client(self) -> ClientAPI:
        """
        Initialize and return a ChromaDB HTTP client for document retrieval.

        Returns:
            chromadb.HttpClient: A client used to communicate with ChromaDB.
        """ 
        logger.info("Initialize chroma db client.")
        return chromadb.HttpClient(
            host=CHROMA_HOST_NAME,
            port=8000,
            settings=Settings(
                allow_reset=True,
                anonymized_telemetry=False,
            ),
            tenant=DEFAULT_TENANT,
            database=DEFAULT_DATABASE,
        )
    def _initialize_vector_db(self) -> Chroma:
        logger.info("Initialize chroma vector db.")

        return Chroma(
            client=self.client,
            collection_name=COLLECTION_NAME,
            embedding_function=self.embedding_function,
        )

    def _index_data_to_vector_db(self):

        pdf_doc = PDF_DOC_PATH
        logger.info(f"Building vector data base from {pdf_doc}")

        # Create pdf data loaders
        loader = PyPDFLoader(pdf_doc)

        # Load and split documents in chunks
        splitter = RecursiveCharacterTextSplitter()
        pages_chunked = splitter.split_documents(loader.load())

        # Function to clean text by removing invalid unicode characters, including surrogate pairs
        def clean_text(text):
            # Remove surrogate pairs
            text = re.sub(r'[\ud800-\udfff]', '', text)
            # Optionally remove non-ASCII characters (depends on your use case)
            text = re.sub(r'[^\x00-\x7F]+', '', text)
            return text

        pages_chunked_cleaned = [
            Document(page_content=clean_text(doc.page_content), metadata=doc.metadata)
            for doc in pages_chunked
        ]

        uuids = [str(uuid4()) for _ in range(len(pages_chunked_cleaned[0:100]))]

        self.vector_db.add_documents(documents=pages_chunked_cleaned[0:100], ids=uuids)

        logger.info(f"Finished building vector database with {self.client.get_collection(COLLECTION_NAME).count()}")

    def _initialize_qa_rag_chain(self) -> Runnable:
        """
        Set up the retrieval-augmented generation (RAG) pipeline for answering questions.
        
        The pipeline consists of:
        - Retrieving relevant documents from ChromaDB.
        - Formatting the retrieved documents for input into the language model (LLM).
        - Using the LLM to generate concise answers.
        
        Returns:
            dict: The RAG pipeline configuration.
        """
        logger.info("Initialize rag chain.")

        # Task: Define prompt
        prompt_template = """Use the retrieved excerpts to answer the question.
Read all excerpts carefully. A definition in an excerpt is sufficient to answer.
Answer directly in at most three sentences.
Only say "I don't know" if the excerpts contain no relevant information.

<retrieved_context>
{context}
</retrieved_context>

Question: {question}

Answer based on the excerpts:"""

        # Task: Initialize prompt langchain prompt template
        rag_prompt = ChatPromptTemplate.from_template(prompt_template)

        # Task: Build the RAG pipeline using the retriever and LLM
        return (
            {
                "context": self.retriever | self._format_docs,
                "question": RunnablePassthrough(),
            }
            | rag_prompt
            | self.llm
            | StrOutputParser()
        )
    def _unique_docs(self, docs):
        unique_docs = []
        seen = set()

        for doc in docs:
            text = doc.page_content.strip()
            if text and text not in seen:
                seen.add(text)
                unique_docs.append(doc)

            if len(unique_docs) == 3:
                break

        return unique_docs

    def _format_docs(self, docs: List[Document]) -> str:
        """
        Helper function to format the retrieved documents into a single string.
        
        Args:
            docs (List[Document]): A list of documents retrieved by ChromaDB.

        Returns:
            str: A string containing the concatenated content of all retrieved documents.
        """
        return "\n\n".join(doc.page_content for doc in docs)
    async def astream(self, question: str):
        self.last_sources = []

        try:
            async for event in self.qa_rag_chain.astream_events(
                question, version="v2"
            ):
                if (
                    event["event"] == "on_chain_end"
                    and event["name"] == "unique_docs"
                ):
                    self.last_sources = event["data"]["output"]

                if event["event"] == "on_chat_model_stream":
                    chunk = event["data"]["chunk"].content
                    if chunk:
                        yield chunk

        except Exception as e:
            logger.error(
                f"Error in stream_answer: {e}",
                exc_info=True,
            )
            raise