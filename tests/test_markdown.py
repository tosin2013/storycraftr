import os
import pytest
from pathlib import Path
from storycraftr.utils.markdown import (
    save_to_markdown,
    append_to_markdown,
    read_from_markdown,
    consolidate_book_md,
)


# Mocks comunes para todos los tests
@pytest.fixture
def mock_console():
    with mock.patch("storycraftr.cli.console") as mock_console:
        yield mock_console


@pytest.fixture
def test_dir(tmp_path):
    """Create a temporary directory for test files."""
    return tmp_path


def test_save_to_markdown_backup(test_dir):
    """Test saving markdown with backup."""
    file_path = test_dir / "test.md"
    content = "# Test Content"
    
    # First save
    save_to_markdown(str(file_path), content, create_backup=True)
    assert file_path.exists()
    assert file_path.read_text() == content
    
    # Second save with backup
    new_content = "# Updated Content"
    save_to_markdown(str(file_path), new_content, create_backup=True)
    backup_file = test_dir / "test.md.bak"
    assert backup_file.exists()
    assert backup_file.read_text() == content
    assert file_path.read_text() == new_content


def test_save_to_markdown_no_backup(test_dir):
    """Test saving markdown without backup."""
    file_path = test_dir / "test.md"
    content = "# Test Content"
    
    save_to_markdown(str(file_path), content, create_backup=False)
    assert file_path.exists()
    assert file_path.read_text() == content
    
    backup_file = test_dir / "test.md.bak"
    assert not backup_file.exists()


def test_append_to_markdown_success(test_dir):
    """Test appending to markdown file."""
    file_path = test_dir / "test.md"
    initial_content = "# Initial Content\n"
    append_content = "## Appended Content"
    
    # Create initial file
    file_path.write_text(initial_content)
    
    # Append content
    append_to_markdown(str(file_path), append_content)
    
    # Verify content
    expected = initial_content + append_content + "\n"
    assert file_path.read_text() == expected


def test_read_from_markdown_success(test_dir):
    """Test reading from markdown file."""
    file_path = test_dir / "test.md"
    content = "# Test Content\n## Section"
    
    # Create test file
    file_path.write_text(content)
    
    # Read and verify
    read_content = read_from_markdown(str(file_path))
    assert read_content == content


def test_read_from_markdown_nonexistent(test_dir):
    """Test reading from non-existent markdown file."""
    file_path = test_dir / "nonexistent.md"
    
    with pytest.raises(FileNotFoundError):
        read_from_markdown(str(file_path))
