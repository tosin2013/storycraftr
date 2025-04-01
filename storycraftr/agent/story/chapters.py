import os
from pathlib import Path
from storycraftr.agent.agents import (
    create_or_get_assistant,
    get_thread,
    create_message,
    update_agent_files,
)
from storycraftr.utils.core import load_book_config
from storycraftr.utils.markdown import save_to_markdown
from storycraftr.prompts.story.chapters import (
    CHAPTER_PROMPT_NEW,
    CHAPTER_PROMPT_REFINE,
    COVER_PROMPT,
    BACK_COVER_PROMPT,
    EPILOGUE_PROMPT_NEW,
    EPILOGUE_PROMPT_REFINE,
)
from rich.console import Console

console = Console()


def generate_chapter(book_path: str, chapter_number: int, prompt: str) -> str:
    """
    Generate a new or refined chapter based on the provided prompt.

    Args:
        book_path (str): The path to the book's directory.
        chapter_number (int): The number of the chapter to generate.
        prompt (str): The prompt to guide the chapter generation.

    Returns:
        str: The content of the generated or refined chapter.
    """
    console.print(f"[bold blue]Generating chapter {chapter_number}...[/bold blue]")

    assistant = create_or_get_assistant(book_path)
    thread = get_thread(book_path)

    chapter_file = f"chapter-{chapter_number}.md"
    file_path = Path(book_path) / "chapters" / chapter_file

    # Check if the chapter already exists to decide between new or refined content
    if file_path.exists():
        console.print(f"[yellow]Existing chapter found. Refining...[/yellow]")
        content = CHAPTER_PROMPT_REFINE.format(
            prompt=prompt, language=load_book_config(book_path).primary_language
        )
    else:
        console.print(
            f"[yellow]No existing chapter found. Generating new content...[/yellow]"
        )
        content = CHAPTER_PROMPT_NEW.format(
            prompt=prompt, language=load_book_config(book_path).primary_language
        )

    chapter_content = create_message(
        book_path,
        thread_id=thread.id,
        content=content,
        assistant=assistant,
        file_path=str(file_path),
    )

    # Save the generated chapter to markdown
    save_to_markdown(str(file_path), chapter_content)
    console.print(
        f"[bold green]✔ Chapter {chapter_number} generated successfully[/bold green]"
    )

    # Update assistant with new chapter information
    update_agent_files(book_path, assistant)

    return chapter_content


def generate_cover(book_path: str, prompt: str) -> str:
    """
    Generate the book cover based on the book's metadata and the given prompt.

    Args:
        book_path (str): The path to the book's directory.
        prompt (str): The prompt to guide the cover generation.

    Returns:
        str: The content of the generated book cover.
    """
    console.print("[bold blue]Generating book cover...[/bold blue]")

    config = load_book_config(book_path)
    assistant = create_or_get_assistant(book_path)
    thread = get_thread(book_path)

    prompt_content = COVER_PROMPT.format(
        title=config.book_name,
        author=config.default_author,
        genre=config.genre,
        alternate_languages=", ".join(config.alternate_languages),
        prompt=prompt,
        language=config.primary_language,
    )

    cover_content = create_message(
        book_path, thread_id=thread.id, content=prompt_content, assistant=assistant
    )

    save_to_markdown(str(Path(book_path) / "chapters" / "cover.md"), cover_content)
    console.print("[bold green]✔ Cover generated successfully[/bold green]")

    update_agent_files(book_path, assistant)
    return cover_content


def generate_back_cover(book_path: str, prompt: str) -> str:
    """
    Generate the back cover content based on the book's metadata and the given prompt.

    Args:
        book_path (str): The path to the book's directory.
        prompt (str): The prompt to guide the back cover generation.

    Returns:
        str: The content of the generated back cover.
    """
    console.print("[bold blue]Generating back cover...[/bold blue]")

    config = load_book_config(book_path)
    assistant = create_or_get_assistant(book_path)
    thread = get_thread(book_path)

    prompt_content = BACK_COVER_PROMPT.format(
        title=config.book_name,
        author=config.default_author,
        genre=config.genre,
        alternate_languages=", ".join(config.alternate_languages),
        prompt=prompt,
        language=config.primary_language,
        license=config.license,
    )

    back_cover_content = create_message(
        book_path, thread_id=thread.id, content=prompt_content, assistant=assistant
    )

    save_to_markdown(str(Path(book_path) / "chapters" / "back-cover.md"), back_cover_content)
    console.print("[bold green]✔ Back cover generated successfully[/bold green]")

    update_agent_files(book_path, assistant)
    return back_cover_content


def generate_epilogue(book_path: str, prompt: str) -> str:
    """
    Generate or refine the book's epilogue based on the provided prompt.

    Args:
        book_path (str): The path to the book's directory.
        prompt (str): The prompt to guide the epilogue generation.

    Returns:
        str: The content of the generated or refined epilogue.
    """
    console.print("[bold blue]Generating epilogue...[/bold blue]")

    assistant = create_or_get_assistant(book_path)
    thread = get_thread(book_path)

    file_path = Path(book_path) / "chapters" / "epilogue.md"

    # Determine if refining an existing epilogue or generating a new one
    if file_path.exists():
        console.print(f"[yellow]Existing epilogue found. Refining...[/yellow]")
        content = EPILOGUE_PROMPT_REFINE.format(
            prompt=prompt, language=load_book_config(book_path).primary_language
        )
    else:
        console.print(
            f"[yellow]No existing epilogue found. Generating new content...[/yellow]"
        )
        content = EPILOGUE_PROMPT_NEW.format(
            prompt=prompt, language=load_book_config(book_path).primary_language
        )

    epilogue_content = create_message(
        book_path,
        thread_id=thread.id,
        content=content,
        assistant=assistant,
        file_path=str(file_path),
    )

    save_to_markdown(str(file_path), epilogue_content)
    console.print("[bold green]✔ Epilogue generated successfully[/bold green]")

    update_agent_files(book_path, assistant)
    return epilogue_content
