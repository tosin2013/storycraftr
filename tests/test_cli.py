import os
import sys
import pytest
import requests
from unittest import mock
from pathlib import Path
from click import ClickException
from storycraftr.cli import (
    load_openai_api_key,
    download_file,
    verify_book_path,
    is_initialized,
    project_not_initialized_error,
    init_structure_story,
    init_structure_paper,
    cli,
)
from click.testing import CliRunner
import click


# Mock the console object to avoid printing to the console during tests
@pytest.fixture
def mock_console():
    with mock.patch("storycraftr.cli.console") as mock_console:
        yield mock_console


# Test download_file function
@mock.patch("requests.get")
def test_download_file_success(mock_get, mock_console):
    mock_response = mock.Mock()
    mock_response.text = "file content"
    mock_response.raise_for_status = mock.Mock()
    mock_get.return_value = mock_response

    save_dir = "test_dir"
    filename = "test_file.txt"

    with mock.patch("pathlib.Path.mkdir") as mock_mkdir, mock.patch(
        "pathlib.Path.write_text"
    ) as mock_write:
        download_file("http://example.com", save_dir, filename)

        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
        mock_write.assert_called_once_with("file content", encoding="utf-8")
        mock_console.print.assert_called_with(
            "[green]File downloaded successfully from http://example.com[/green]"
        )


@mock.patch("requests.get", side_effect=requests.exceptions.RequestException("Error"))
def test_download_file_failure(mock_get, mock_console):
    with pytest.raises(SystemExit):
        download_file("http://example.com", "test_dir", "test_file.txt")

    mock_console.print.assert_called_with(
        "[red]Error downloading the file from http://example.com: Error[/red]"
    )


# Test verify_book_path function
@mock.patch("os.path.exists")
def test_verify_book_path_success(mock_exists, mock_console):
    mock_exists.return_value = True
    assert verify_book_path("test_path") == "test_path"


@mock.patch("os.path.exists")
def test_verify_book_path_failure(mock_exists, mock_console):
    mock_exists.return_value = False
    with pytest.raises(ClickException):
        verify_book_path("invalid_path")


# Test is_initialized function
@mock.patch("os.path.exists")
def test_is_initialized_true(mock_exists, mock_console):
    mock_exists.return_value = True
    assert is_initialized("test_path")


@mock.patch("os.path.exists")
def test_is_initialized_false(mock_exists, mock_console):
    mock_exists.return_value = False
    assert not is_initialized("test_path")


# Test project_not_initialized_error function
def test_project_not_initialized_error(mock_console):
    project_not_initialized_error("test_path")

    mock_console.print.assert_called_with(
        "[red]✖ Project 'test_path' is not initialized. Run 'storycraftr init {book_path}' first.[/red]"
    )


def test_cli_init():
    """Test the init command."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Create a behavior file
        with open("behavior.txt", "w") as f:
            f.write("Test behavior")
        
        result = runner.invoke(cli, ['init', 'test_project', '--behavior', 'behavior.txt'])
        assert result.exit_code == 0


def test_cli_chat():
    """Test the chat command."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Create necessary files for chat
        os.makedirs("test_project")
        with open("test_project/storycraftr.json", "w") as f:
            f.write('{"name": "test_project"}')
        
        result = runner.invoke(cli, ['chat'])
        assert result.exit_code == 0


def test_story_commands():
    """Test story-related commands."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Create necessary files for story commands
        os.makedirs("test_project")
        with open("test_project/storycraftr.json", "w") as f:
            f.write('{"name": "test_project", "type": "story"}')
        
        # Create behavior file
        with open("behavior.txt", "w") as f:
            f.write("Test behavior")
        
        # Initialize project first
        result = runner.invoke(cli, ['init', 'test_project', '--behavior', 'behavior.txt'])
        assert result.exit_code == 0
        
        # Change to project directory
        os.chdir("test_project")
        
        # Test story outline with prompt
        result = runner.invoke(cli, ['story', 'outline', '--help'])
        assert result.exit_code == 0


def test_paper_commands():
    """Test paper-related commands."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Create necessary files for paper commands
        os.makedirs("test_project")
        with open("test_project/storycraftr.json", "w") as f:
            f.write('{"name": "test_project", "type": "paper"}')
        
        # Create behavior file
        with open("behavior.txt", "w") as f:
            f.write("Test behavior")
        
        # Initialize project first
        result = runner.invoke(cli, ['init', 'test_project', '--behavior', 'behavior.txt'])
        assert result.exit_code == 0
        
        # Change to project directory
        os.chdir("test_project")
        
        # Create a test-specific CLI instance with paper commands
        from storycraftr.cmd.paper import paper
        test_cli = click.Group()
        test_cli.add_command(paper)
        
        # Test paper define with prompt
        result = runner.invoke(test_cli, ['paper', 'define', '--help'])
        assert result.exit_code == 0
