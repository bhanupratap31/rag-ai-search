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
                    if current_chunk: 
                        chunk_text = ' '.join(current_chunk)
                        chunks.append(Chunk(
                            text = chunk_text, 
                            metadata = metadata.copy(), 
                            chunk_id = f"chunk_{len(chunks)}_{hash(chunk_text)}"
                        ))

        