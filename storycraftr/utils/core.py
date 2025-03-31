import os
import secrets  # Para generar números aleatorios seguros
import yaml
import json
from typing import NamedTuple
from rich.console import Console
from rich.markdown import Markdown  # Importar soporte de Markdown de Rich
from storycraftr.prompts.permute import longer_date_formats
from storycraftr.state import debug_state  # Importar el estado de debug
from pathlib import Path

console = Console()

MODEL_CONFIG = {
    'openai': {
        'default_model': 'gpt-3.5-turbo-0125',
        'available_models': [
            'gpt-3.5-turbo-0125',
            'gpt-4-0125-preview',
            'gpt-4-turbo-preview',
            'gpt-4.5-preview'
        ],
        'api_base': 'https://api.openai.com/v1/'
    },
    'azure': {
        'default_model': 'gpt-3.5-turbo-0125',
        'available_models': [
            'gpt-3.5-turbo-0125',
            'gpt-4-0125-preview',
            'gpt-4-turbo-preview',
            'gpt-4.5-preview'
        ],
        'api_base': None  # Set during runtime based on Azure configuration
    },
    'deepseek': {
        'default_model': 'DeepSeek-V3-0324',
        'available_models': [
            'DeepSeek-V3-0324',
            'DeepSeek-R1-Distill-Qwen-32B'
        ],
        'api_base': 'https://api.deepseek.com/v1/'
    },
    'qwen': {
        'default_model': 'Qwen2.5-Omni-7B',
        'available_models': [
            'Qwen2.5-Omni-7B',
            'Qwen2.5-Coder-32B-Instruct',
            'Qwen2.5-14B-DeepSeek-R1-1M'
        ],
        'api_base': 'https://dashscope.aliyuncs.com/'
    },
    'gemini': {
        'default_model': 'Gemini-2.5-Pro-Experimental',
        'available_models': [
            'Gemini-2.5-Pro-Experimental',
            'Gemini-2.5'
        ],
        'api_base': 'https://api.gemini.google.com/v1/'
    },
    'together': {
        'default_model': 'together-gpt-neoxt-chat-20b',
        'available_models': ['together-gpt-neoxt-chat-20b'],
        'api_base': 'https://api.together.ai/v1/'
    },
    'deepinfra': {
        'default_model': 'Qwen2.5-Coder-32B-Instruct',
        'available_models': ['Qwen2.5-Coder-32B-Instruct'],
        'api_base': 'https://api.deepinfra.com/v1/'
    }
}

def get_model_config(provider='openai', model=None):
    """
    Get the configuration for a specific model provider and model.
    
    Args:
        provider (str): The model provider (e.g., 'openai', 'azure', 'deepseek')
        model (str, optional): Specific model to use. If None, uses provider's default
        
    Returns:
        dict: Model configuration including API base URL and model details
        
    Raises:
        ValueError: If provider or model is not supported
    """
    if provider not in MODEL_CONFIG:
        raise ValueError(f"Unsupported provider: {provider}")
        
    config = MODEL_CONFIG[provider].copy()
    
    if model:
        if model not in config['available_models']:
            raise ValueError(f"Model {model} not supported by provider {provider}")
        config['model'] = model
    else:
        config['model'] = config['default_model']
        
    return config

def generate_prompt_with_hash(original_prompt: str, date: str, book_path: str) -> str:
    """
    Generates a modified prompt by combining a random phrase from a list,
    a date, and the original prompt. Logs the prompt details in a YAML file.

    Args:
        original_prompt (str): The original prompt to be modified.
        date (str): The current date to be used in the prompt.
        book_path (str): Path to the book's directory where prompts.yaml will be saved.

    Returns:
        str: The modified prompt with the date and random phrase.
    """
    # Selecciona una frase aleatoria segura de la lista
    random_phrase = secrets.choice(longer_date_formats).format(date=date)
    modified_prompt = f"{random_phrase}\n\n{original_prompt}"

    # Define la ruta del archivo YAML
    yaml_path = Path(book_path) / "prompts.yaml"

    # Nueva entrada de log con fecha y prompt original
    log_entry = {"date": str(date), "original_prompt": original_prompt}

    # Verifica si el archivo YAML existe y carga los datos
    if yaml_path.exists():
        with yaml_path.open("r", encoding="utf-8") as file:
            existing_data = (
                yaml.safe_load(file) or []
            )  # Carga una lista vacía si está vacío
    else:
        existing_data = []

    # Añade la nueva entrada al log
    existing_data.append(log_entry)

    # Guarda los datos actualizados en el archivo YAML
    with yaml_path.open("w", encoding="utf-8") as file:
        yaml.dump(existing_data, file, default_flow_style=False)

    # Imprime el prompt modificado en Markdown si el modo debug está activado
    if debug_state.is_debug():
        console.print(Markdown(modified_prompt))

    return modified_prompt


class BookConfig(NamedTuple):
    """
    A NamedTuple representing the configuration of a book.

    Attributes:
        book_path (str): The path to the book's directory.
        book_name (str): The name of the book.
        primary_language (str): The primary language of the book.
        alternate_languages (list): A list of alternate languages.
        default_author (str): The default author of the book.
        genre (str): The genre of the book.
        license (str): The license type for the book.
        reference_author (str): A reference author for style guidance.
        keywords (str): Keywords for the paper (optional).
        cli_name (str): The name of the CLI tool used.
        openai_url (str): The URL of the OpenAI API.
        openai_model (str): The OpenAI model to use.
        multiple_answer (bool): Whether multiple answers are allowed.
    """

    book_path: str
    book_name: str
    primary_language: str
    alternate_languages: list
    default_author: str
    genre: str
    license: str
    reference_author: str
    keywords: str
    cli_name: str
    openai_url: str
    openai_model: str
    multiple_answer: bool


def load_book_config(book_path: str) -> BookConfig:
    """
    Loads the book's configuration from the storycraftr.json file.

    Args:
        book_path (str): The path to the book's directory.

    Returns:
        BookConfig: An instance of the BookConfig NamedTuple containing the book's settings.
        None: If the storycraftr.json file is not found or is in an invalid directory.
    """
    config_file = Path(book_path) / "storycraftr.json"

    try:
        with config_file.open("r", encoding="utf-8") as file:
            data = json.load(file)
            # Devuelve una instancia de BookConfig con los valores del archivo JSON
            return BookConfig(
                book_path=data["book_path"],
                book_name=data["book_name"],
                primary_language=data["primary_language"],
                alternate_languages=data["alternate_languages"],
                default_author=data["default_author"],
                genre=data["genre"],
                license=data["license"],
                reference_author=data["reference_author"],
                keywords=data["keywords"] if "keywords" in data else "",
                cli_name=data["cli_name"],
                openai_url=data["openai_url"],
                openai_model=data["openai_model"],
                multiple_answer=data["multiple_answer"],
            )
    except (FileNotFoundError, NotADirectoryError):
        console.print(
            f"[bold red]⚠[/bold red] Folder '[bold]{book_path}[/bold]' is not a storycraftr project.",
            style="red",
        )
        return None


def file_has_more_than_three_lines(file_path: str) -> bool:
    """
    Check if a file has more than three lines.

    Args:
        file_path (str): The path to the file.

    Returns:
        bool: True if the file has more than three lines, False otherwise.
    """
    try:
        with Path(file_path).open("r", encoding="utf-8") as file:
            # Itera sobre las primeras 4 líneas y devuelve True si hay más de 3 líneas
            for i, _ in enumerate(file, start=1):
                if i > 3:
                    return True
    except FileNotFoundError:
        console.print(f"[red bold]Error:[/red bold] File not found: {file_path}")
        return False
    return False
