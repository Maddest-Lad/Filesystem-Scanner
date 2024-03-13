from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from modules.temporary_copy import with_temporary_copy

@dataclass
class Content(ABC):
    """Parent dataclass for all content types"""
    path: Path

    # Metadata
    name: Optional[str] = field(default=None, init=False)
    type: Optional[str] = field(default=None, init=False)
    size: Optional[int] = field(default=None, init=False)
    date_created: Optional[datetime] = field(default=None, init=False)
    date_modified: Optional[datetime] = field(default=None, init=False)

    @abstractmethod
    def process(self):
        pass
        
    def __post_init__(self):
        """Extract metadata from the file"""
        self.name = self.path.name
        self.type = self.path.suffix
        self.size = self.path.stat().st_size
        self.date_created =  datetime.fromtimestamp(self.path.stat().st_ctime)
        self.date_modified = datetime.fromtimestamp(self.path.stat().st_mtime)

    def __str__(self) -> str:
        return self.path.name
    
    def __repr__(self) -> str:
        return f"Content({self.name}, Path={self.path}, Type={self.type}, {self.size} bytes, Created={self.date_created}, Modified={self.date_modified}"


@dataclass
class RawText(Content):
    """Text content"""
    
    @with_temporary_copy
    def process(self):
        with open(self.path, "r") as f:
            return f.read()

@dataclass   
class StructuredText(Content):
    """Structured text content (JSON, XML, CSV, TSV)"""
    
    @with_temporary_copy
    def process(self):
        pass

@dataclass
class Document(Content):
    """Document content"""
    
    @with_temporary_copy
    def process(self):
        pass

@dataclass
class Image(Content):
    """Image content"""
    
    def ocr(self):
        pass
    
    @with_temporary_copy
    def process(self):
        pass

@dataclass
class Code(Content):
    """Code content"""
    
    @with_temporary_copy
    def process(self):
        pass

@dataclass
class UnknownContent(Content):
    """Unknown content"""
    
    @with_temporary_copy
    def process(self):
        pass
