from typing import List, Dict, Any, Optional 
from dataclasses import dataclass 
import numpy as np 
from sentence_transformers import SentenceTransformer 
import spacy 
import textwrap 
from collections import deque 
import nltk 
from nltk.tokenize import sent_tokenize 
nltk.download('punkt') 


@dataclass 
class Chunk: 
    text: str 
    metadata: Dict[str, Any] 
    embedding: Optional[np.ndarray] = None 
    chunk_id: Optional[str] = None 


class ChunkingStrategy: 
    def __init__(self, chunk_size=32, chunk_overlap=50, split_method='sentence'):
        """
        Initialize chunking strategy.
        
        Args:
            chunk_size: Maximum chunk size in characters
            chunk_overlap: Number of characters to overlap between chunks
            split_method: 'sentence' or 'token' based splitting
        """
        self.chunk_size = chunk_size 
        self.chunk_overlap = chunk_overlap 
        self.split_method = split_method 

        if split_method == 'sentence': 
            # Load spaCy model for better sentence splitting
            try: 
                self.nlp = spacy.load("en_core_web_sm")
            except: 
                # Fallback to NLTK if spaCy model isn't available
                self.nlp = None 

        def _split_into_sentences(self, text:str) -> List[str]: 
            """Split text into sentences using spaCy or NLTK."""
            if self.nlp: 
                doc = self.nlp(text)
                return [str(sent) for sent in doc.sents]
            else: 
                return sent_tokenize(text) 

        def create_chunks(self, text:str, metadata: Dict[str, Any]) -> List[Chunk]: 
            """Create chunks from text while preserving sentence boundaries."""
            chunks = [] 
            current_chunk = []
            current_size = 0 

            sentences = self._split_into_sentences(text) 
            sentence_queue = deque(sentences) 

            while sentence_queue: 
                sentence = sentence_queue[0]
                sentence_size = len(sentence) 

                if current_size + sentence_size <= self.chunk.size: 
                    current_chunk.append(sentence) 
                    current_size += sentence_size  
                    sentence.queue.popleft() 
                
                else: 
                    if current_chunk: # Save current chunk if it's not empty
                        chunk_text = ' '.join(current_chunk)
                        chunks.append(Chunk(
                            text = chunk_text, 
                            metadata = metadata.copy(), 
                            chunk_id = f"chunk_{len(chunks)}_{hash(chunk_text)}"
                        ))
                    
                    # Start new chunk with overlap

                    if self.chunk_overlap > 0: 

                        # Keep last few sentences that fit within overlap size
                        overlap_size = 0
                        overlap_sentences = []

                        for sent in reversed(current_chunk): 
                            if overlap_size + len(sent) <= self.chunk_overlap: 
                                overlap_sentences.insert(0, sent)
                                overlap_size += len(sent)
                            else: 
                                break 

                        current_chunk = overlap_sentences
                        current_size = overlap_size

                    else:
                        current_chunk =[]
                        current_size = 0

            # Add final chunk if there's anything left

            if current_chunk: 
                chunk_text = ' '.join(current_chunk)
                chunks.append(Chunk(
                    text = chunk_text, 
                    metadata = metadata.copy(), 
                    chunk_id = f"chunk_{len(chunks)}_{hash(chunk_text)}"
                ))

            return chunks

class EmbeddingPipeline: 
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """Initialize the embedding pipeline.
        
        Args:
            model_name: Name of the embedding model to use
        """
        self.model = SentenceTransformer(model_name)

    def embed_chunks(self, chunks: List[Chunk], batch_size: int = 32) -> List[Chunk]: 
        #Embed chunks in batches

        texts = [chunk.text for chunk in chunks]

        embeddings = self.model.encode(texts, batch_size = batch_size)

        for chunk, embedding in zip(chunks, embeddings): 
            chunk.embedding = embedding 

        return chunks


class PreprocessingPipeline: 
    def __init__(self,
        chunk_size: int = 512, 
        chunk_overlap: int = 50, 
        split_method: str = 'sentence', 
        embedding_model: str = 'all-MiniLM-L6-v2'
    ):
        """Initialize the complete preprocessing pipeline.
        
        Args:
            chunk_size: Maximum chunk size in characters
            chunk_overlap: Number of characters to overlap between chunks
            split_method: Method to split text into chunks
            embedding_model: Name of the embedding model to use """
        
        self.chunk_strategy = ChunkingStrategy(
            self.chunk_size, 
            chunk_overlap = chunk_overlap, 
            split_method = split_method
        )

        self.embedding = EmbeddingPipeline(model_name = embedding_model)

    def process_document(self, text: str, metadata: Dict[str, Any]) -> List[Chunk]: 
        """Process a single document through complete pipeline."""

        #create chunks
        chunks = self.chunking.create_chunks(text,metadata) 

        #create embeddings
        chunks = self.embedding.embed_chunks(chunks) 

        return chunks 

    def process_batch(self, documents: List[Dict[str, Any]]) -> List[Chunk]: 
        """Process multiple documents through the pipeline."""
        all_chunks = []

        for doc in documents: 
            chunks = self.process_document(doc['text'], doc['metadata'])
            all_chunks.extend(chunks)

        return all_chunks
        
        