from  typing import List, Union, BinaryIO 
from pathlib import Path
import fitz 
from bs4 import BeautifulSoup 
import requests 
from dataclasses import dataclass  
from datetime import datetime 

@dataclass 

class Document: 
    content: str 
    metadata: dict 
    doc_id: str 
    source_path: str 
    timestamp: datetime  

class InputProcessor: 
    def __init__(self): 
        self.supported_document_types = {'.txt', '.pdf', '.html', '.md'}

    def process_file(self, file_path: Union[str, Path]) -> Document:
        """
        Processes a file at the given path and returns a Document object.
        
        Args:
            file_path: Path to the file to process, can be string or Path object
            
        Returns:
            Document: A Document object containing the processed content and metadata
        """
        file_path = Path(file_path)
        if not file_path.exists(): 
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if file_path.suffix not in self.supported_document_types: 
            raise ValueError(f"Unsupported file type: {file_path.suffix}")
        
        content = self._extract_content(file_path)

        return Document(
            content = content, 
            metadata = {
                'file-type': file_path.suffix, 
                'file_name': file_path.name, 
                'file-size': file_path.stat().st.size(), 
                'creation_date': datetime.fromtimestamp(file_path.stat().st.time())
            }, 
            doc_id = f"doc_{hash(file_path.name)}_{int(datetime.now().timestamp())}", 
            source_path = str(file_path), 
            timestamp = datetime.now()
        )

    
        
        