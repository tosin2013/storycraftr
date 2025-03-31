import os
import re
import shutil
from pathlib import Path
from storycraftr.agent.agents import (
    create_or_get_assistant,
    get_thread,
    create_message,
)
from rich.console import Console
from rich.progress import Progress
from typing import Optional

console = Console()


def save_to_markdown(file_path: str, content: str, create_backup: bool = True) -> None:
    """
    Save content to a markdown file with optional backup.
    
    Args:
        file_path: Path to the markdown file
        content: Content to write to the file
        create_backup: Whether to create a backup of existing file
    """
    file_path = Path(file_path)
    
    # Create backup if requested and file exists
    if create_backup and file_path.exists():
        backup_path = file_path.with_suffix(file_path.suffix + '.bak')
        shutil.copy2(file_path, backup_path)
    
    # Create parent directories if they don't exist
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write content
    file_path.write_text(content, encoding='utf-8')


def append_to_markdown(file_path: str, content: str) -> None:
    """
    Append content to a markdown file.
    
    Args:
        file_path: Path to the markdown file
        content: Content to append
    
    Raises:
        FileNotFoundError: If the file doesn't exist
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(content + "\n")


def read_from_markdown(file_path: str) -> str:
    """
    Read content from a markdown file.
    
    Args:
        file_path: Path to the markdown file
    
    Returns:
        str: Content of the file
    
    Raises:
        FileNotFoundError: If the file doesn't exist
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    return file_path.read_text(encoding='utf-8')


def consolidate_book_md(
    book_path: str, primary_language: str, translate: str = None
) -> str:
    """
    Consolidate all chapters of a book into a single markdown file.

    Args:
        book_path (str): The path to the book's directory.
        primary_language (str): The primary language of the book.
        translate (str, optional): If provided, translates the content to the specified language.

    Returns:
        str: The path to the consolidated markdown file.
    """
    chapters_dir = Path(book_path) / "chapters"
    output_file_name = (
        f"book-{primary_language}.md" if not translate else f"book-{translate}.md"
    )
    output_file_path = Path(book_path) / "book" / output_file_name

    # Ensure the "book" folder exists
    output_file_path.parent.mkdir(parents=True, exist_ok=True)

    # Create or get the assistant and thread for translation (if needed)
    assistant = create_or_get_assistant(book_path)
    thread = get_thread()

    # Collect chapters to process
    files_to_process = []

    # Add cover and back-cover if they exist
    for section in ["cover.md", "back-cover.md"]:
        section_path = chapters_dir / section
        if section_path.exists():
            files_to_process.append(section_path)

    # Add chapters in order
    chapter_files = sorted(
        [f for f in chapters_dir.iterdir() if re.match(r"chapter-\d+\.md", f.name)],
        key=lambda x: int(re.findall(r"\d+", x.name)[0]),
    )
    files_to_process.extend(chapter_files)

    # Add epilogue if it exists
    epilogue_path = chapters_dir / "epilogue.md"
    if epilogue_path.exists():
        files_to_process.append(epilogue_path)

    # Log start of consolidation
    if translate:
        console.print(
            f"Consolidating and translating to [bold]{translate}[/bold] for [bold]{book_path}[/bold]..."
        )
    else:
        console.print(
            f"Consolidating chapters for [bold]{book_path}[/bold] without translation..."
        )

    # Process files and consolidate into one markdown file
    with Progress() as progress:
        task_chapters = progress.add_task(
            "[cyan]Processing chapters...", total=len(files_to_process)
        )
        task_translation = (
            progress.add_task("[cyan]Translating content...", total=50)
            if translate
            else None
        )
        task_openai = progress.add_task("[green]Calling OpenAI...", total=1)

        with output_file_path.open("w", encoding="utf-8") as consolidated_md:
            for chapter_file in files_to_process:
                progress.update(
                    task_chapters, description=f"Processing {chapter_file.name}..."
                )
                with chapter_file.open("r", encoding="utf-8") as chapter_md:
                    content = chapter_md.read()

                    # Translate content if translation is requested
                    if translate:
                        progress.update(
                            task_translation,
                            description=f"Translating {chapter_file.name}...",
                        )
                        content = create_message(
                            book_path,
                            thread_id=thread.id,
                            content=content,
                            assistant=assistant,
                            progress=progress,
                            task_id=task_openai,
                        )

                    # Write (translated or original) content to consolidated file
                    consolidated_md.write(content)
                    consolidated_md.write("\n\\newpage\n")

                # Update progress for chapters
                progress.update(task_chapters, advance=1)

    # Log completion of consolidation
    progress.update(
        task_chapters,
        description=f"[green bold]Book consolidated[/green bold] at {output_file_path}",
    )

    return str(output_file_path)
