from io import BytesIO
from pathlib import Path

from markitdown import MarkItDown, StreamInfo
from pydantic import Field


def binary_document_to_markdown(
    binary_data: bytes = Field(description="Raw binary content of the document file"),
    file_type: str = Field(description="File extension indicating document format: 'docx' for Word documents or 'pdf' for PDF files"),
) -> str:
    """Convert a Word document or PDF file to markdown-formatted text.

    Accepts the binary content of a .docx or .pdf file and returns the extracted
    text as markdown. Use this tool when you need to read or analyse the contents
    of a document supplied as raw bytes.

    Do not use for file formats other than docx and pdf (e.g. xlsx, pptx).

    Example:
        with open("report.pdf", "rb") as f:
            markdown = binary_document_to_markdown(f.read(), "pdf")
        # Returns: "# Report Title\\n\\nSection content..."
    """
    md = MarkItDown()
    file_obj = BytesIO(binary_data)
    stream_info = StreamInfo(extension=file_type)
    result = md.convert(file_obj, stream_info=stream_info)
    return result.text_content


def document_path_to_markdown(
    file_path: str = Field(description="Absolute or relative path to a .docx or .pdf file on disk"),
) -> str:
    """Convert a Word or PDF file on disk to markdown-formatted text.

    Reads the file at the given path and converts its contents to markdown.
    The file format is inferred from the file extension (.docx or .pdf).

    Use this tool when you have a file path. Use binary_document_to_markdown
    instead when you already have the raw bytes of the document.

    Do not use for file formats other than .docx and .pdf.

    Example:
        result = document_path_to_markdown("/reports/summary.pdf")
        # Returns: "# Summary\\n\\nContent..."
    """
    path = Path(file_path)
    extension = path.suffix.lstrip(".").lower()
    with open(path, "rb") as f:
        binary_data = f.read()
    return binary_document_to_markdown(binary_data, extension)
