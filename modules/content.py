from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import csv
import json
import xmltodict
from docx import Document as Docx
from PIL import Image
import pytesseract

from modules.temporary_copy import with_temporary_copy


@dataclass
class FileRecord(ABC):
    """Parent dataclass for all content types"""

    path: Path
    content: Optional[any] = field(default=None, init=False)

    # Metadata
    name: Optional[str] = field(default=None, init=False)
    type: Optional[str] = field(default=None, init=False)
    size: Optional[int] = field(default=None, init=False)
    date_created: Optional[datetime] = field(default=None, init=False)
    date_modified: Optional[datetime] = field(default=None, init=False)

    @property
    def content(self):
        if not self.content:
            self.content = self.process()
        return self.content

    @abstractmethod
    def _process(self):
        pass

    def __post_init__(self):
        """Extract metadata from the file"""
        self.name = self.path.name
        self.type = self.path.suffix
        self.size = self.path.stat().st_size
        self.date_created = datetime.fromtimestamp(self.path.stat().st_ctime)
        self.date_modified = datetime.fromtimestamp(self.path.stat().st_mtime)

    def __str__(self) -> str:
        return self.path.name

    def __repr__(self) -> str:
        return f"Content({self.name}, Path={self.path}, Type={self.type}, {self.size} bytes, Created={self.date_created}, Modified={self.date_modified}"


@dataclass
class RawText(FileRecord):
    """Text Based Files"""

    @with_temporary_copy
    def _process(self):
        with open(self.path, "r") as f:
            return f.read()


@dataclass
class StructuredText(FileRecord):
    """Structured Text Files (JSON, XML, CSV, TSV)"""

    @with_temporary_copy
    def _process(self):
        match self.type:
            case ".json":
                with open(self.path, "r") as f:
                    return json.load(f)
            case ".xml":
                with open(self.path, "r") as f:
                    return xmltodict.parse(f.read())
            case ".csv" | ".tsv":
                with open(self.path, "r") as f:
                    return list(csv.reader(f))


@dataclass
class Document(FileRecord):
    """Document content (DOCX, PPTX)"""

    @with_temporary_copy
    def _process(self):

        match self.path.type:

            case ".docx" | ".doc":
                doc = Docx(self.path)
                return "\n".join([p.text for p in doc.paragraphs])

            case ".pptx" | ".ppt":
                raise NotImplementedError("PowerPoint files are not yet supported")


@dataclass
class Image(FileRecord):
    """Analyze Image Content with OCR (JPG, PNG, WEBP)"""

    @with_temporary_copy
    def _process(self):
        image = Image.open(self.path)

        # Attempt to Rotate The Image If It's Not Upright
        try:
            osd = pytesseract.image_to_osd(
                image,
                output_type=pytesseract.Output.DICT,
                config="--psm 0 -c -min_characters_to_try=5",
            )
            angle_to_rotate = osd["rotate"]

            if angle_to_rotate != 0:
                image = image.rotate(angle_to_rotate, expand=True)

        except pytesseract.pytesseract.TesseractError as e:
            print("Error:", e)

        finally:
            return pytesseract.image_to_string(image)


@dataclass
class UnknownContent(FileRecord):
    """Unknown Type Fallback"""

    @with_temporary_copy
    def _process(self):
        raise NotImplementedError(f"Unknown File Type")
