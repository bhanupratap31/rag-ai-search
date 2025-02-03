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
                
        