import os
from typing import Optional


def get_openai_api_key() -> str:
    """
    Get the OpenAI API key from environment variables.
    
    Returns:
        The OpenAI API key as a string
        
    Raises:
        ValueError: If the API key is not found in environment variables
    """
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable is not set. "
            "Please set it before using the slide generator."
        )
    
    return api_key

