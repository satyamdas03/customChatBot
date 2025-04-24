import copy
from typing import List, Dict, Any

Document = List[Dict[str, Any]]  # your Slate document model

def set_font_size(doc: Document, paragraph_index: int, size: float) -> Document:
    new_doc = copy.deepcopy(doc)
    try:
        para = new_doc[paragraph_index]
        # apply fontSize to every text child
        for node in para.get("children", []):
            node.setdefault("marks", {})
            node["marks"]["fontSize"] = size
    except IndexError:
        pass
    return new_doc

def toggle_bold(doc: Document, paragraph_index: int) -> Document:
    new_doc = copy.deepcopy(doc)
    try:
        para = new_doc[paragraph_index]
        for node in para.get("children", []):
            marks = node.setdefault("marks", {})
            marks["bold"] = not marks.get("bold", False)
    except IndexError:
        pass
    return new_doc

def align_paragraph(doc: Document, paragraph_index: int, alignment: str) -> Document:
    new_doc = copy.deepcopy(doc)
    try:
        para = new_doc[paragraph_index]
        para["textAlign"] = alignment
    except IndexError:
        pass
    return new_doc
