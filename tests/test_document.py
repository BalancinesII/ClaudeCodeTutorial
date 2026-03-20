import os
import pytest
from tools.document import binary_document_to_markdown, document_path_to_markdown


class TestBinaryDocumentToMarkdown:
    # Define fixture paths
    FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
    DOCX_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.docx")
    PDF_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.pdf")

    def test_fixture_files_exist(self):
        """Verify test fixtures exist."""
        assert os.path.exists(self.DOCX_FIXTURE), (
            f"DOCX fixture not found at {self.DOCX_FIXTURE}"
        )
        assert os.path.exists(self.PDF_FIXTURE), (
            f"PDF fixture not found at {self.PDF_FIXTURE}"
        )

    def test_binary_document_to_markdown_with_docx(self):
        """Test converting a DOCX document to markdown."""
        # Read binary content from the fixture
        with open(self.DOCX_FIXTURE, "rb") as f:
            docx_data = f.read()

        # Call function
        result = binary_document_to_markdown(docx_data, "docx")

        # Basic assertions to check the conversion was successful
        assert isinstance(result, str)
        assert len(result) > 0
        # Check for typical markdown formatting - this will depend on your actual test file
        assert "#" in result or "-" in result or "*" in result

    def test_binary_document_to_markdown_with_pdf(self):
        """Test converting a PDF document to markdown."""
        # Read binary content from the fixture
        with open(self.PDF_FIXTURE, "rb") as f:
            pdf_data = f.read()

        # Call function
        result = binary_document_to_markdown(pdf_data, "pdf")

        # Basic assertions to check the conversion was successful
        assert isinstance(result, str)
        assert len(result) > 0
        # Check for typical markdown formatting - this will depend on your actual test file
        assert "#" in result or "-" in result or "*" in result


class TestDocumentPathToMarkdown:
    FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
    DOCX_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.docx")
    PDF_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.pdf")

    # Test 1: PDF happy path — returns string with expected content
    def test_convert_pdf(self):
        result = document_path_to_markdown(self.PDF_FIXTURE)
        assert isinstance(result, str)
        assert "MCP" in result or "Model Context Protocol" in result

    # Test 2: DOCX happy path — returns string with expected content
    def test_convert_docx(self):
        result = document_path_to_markdown(self.DOCX_FIXTURE)
        assert isinstance(result, str)
        assert "MCP" in result or "Model Context Protocol" in result

    # Test 3: Return type is always str
    def test_return_type_is_string(self):
        assert isinstance(document_path_to_markdown(self.PDF_FIXTURE), str)
        assert isinstance(document_path_to_markdown(self.DOCX_FIXTURE), str)

    # Test 4: Markdown structure — DOCX headings render as # headings
    def test_markdown_headings_present(self):
        result = document_path_to_markdown(self.DOCX_FIXTURE)
        assert "#" in result, "No markdown headings found in DOCX output"

    # Test 5: Uppercase extension (.PDF) is handled
    def test_uppercase_pdf_extension(self, tmp_path):
        import shutil
        upper = tmp_path / "mcp_docs.PDF"
        shutil.copy(self.PDF_FIXTURE, upper)
        result = document_path_to_markdown(str(upper))
        assert isinstance(result, str)
        assert len(result) > 0

    # Test 6: Mixed-case extension (.Docx) is handled
    def test_mixedcase_docx_extension(self, tmp_path):
        import shutil
        mixed = tmp_path / "mcp_docs.Docx"
        shutil.copy(self.DOCX_FIXTURE, mixed)
        result = document_path_to_markdown(str(mixed))
        assert isinstance(result, str)
        assert len(result) > 0
