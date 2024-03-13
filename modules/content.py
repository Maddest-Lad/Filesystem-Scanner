from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from modules.temporary_copy import with_temporary_copy



@dataclass
class Content(ABC):
    """Parent dataclass for all content types"""
    path: Path
    content: any

    # Metadata
    name: str
    type: str
    size: int
    date_created: str
    date_modified: str

    @abstractmethod
    @with_temporary_copy
    def process(self):
        pass    
    
    def __post_init__(self):
        """Extract metadata from the file"""
        self.name = self.path.name
        self.type = self.path.suffix
        self.size = self.path.stat().st_size
        self.date_created = self.path.stat().st_ctime
        self.date_modified = self.path.stat().st_mtime

    def __str__(self) -> str:
        return self.path.name
    
    def __repr__(self) -> str:
        return f"Content({self.name!r}, Path={self.path!r}, Type={self.type!r}, {self.size} bytes, Created={self.date_created}, Modified={self.date_modified}"


@dataclass
class RawText(Content):
    """Text content"""
    
    def process(self):
        with open(self.path, "r") as f:
            return f.read()

@dataclass   
class StructuredText(Content):
    """Structured text content (JSON, XML, CSV, TSV)"""
    
    def process(self):
        pass

@dataclass
class Document(Content):
    """Document content"""
    
    def process(self):
        pass

@dataclass
class Image(Content):
    """Image content"""
    
    def ocr(self):
        pass
    
    def process(self):
        pass

@dataclass
class Code(Content):
    """Code content"""
    
    def process(self):
        pass

@dataclass
class UnknownContent(Content):
    """Unknown content"""
    
    def process(self):
        pass


