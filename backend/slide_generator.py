import json
import os
from openai import OpenAI
from backend.config import get_openai_api_key


def generate_slides(prompt: str) -> dict:
    """
    Generate slides using OpenAI GPT-4o API based on the given prompt.
    
    Args:
        prompt: A string describing what slides to generate
        
    Returns:
        A dictionary containing a list of slides, where each slide has:
        - title: string
        - content: list of strings (bullet points)
        - theme: string (e.g., 'professional', 'creative')
        
    Raises:
        Exception: If the API call fails or response is invalid
    """
    api_key = get_openai_api_key()
    client = OpenAI(api_key=api_key)
    
    system_prompt = """You are a presentation slide generator. Generate a JSON object containing a list of slides.
Each slide should have:
- title: A concise title for the slide (string)
- content: A list of bullet points as strings (list of strings)
- theme: A theme name like 'professional', 'creative', 'modern', 'minimalist', etc. (string)

Return ONLY valid JSON in this exact format:
{
  "slides": [
    {
      "title": "Slide Title",
      "content": ["Bullet point 1", "Bullet point 2", "Bullet point 3"],
      "theme": "professional"
    }
  ]
}

Make sure the JSON is valid and properly formatted. Generate 3-8 slides based on the user's prompt."""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )
        
        # Extract the JSON response
        content = response.choices[0].message.content
        
        # Parse the JSON
        slides_data = json.loads(content)
        
        # Validate the structure
        if "slides" not in slides_data:
            raise ValueError("Response missing 'slides' key")
        
        if not isinstance(slides_data["slides"], list):
            raise ValueError("'slides' must be a list")
        
        # Validate each slide
        for slide in slides_data["slides"]:
            if not isinstance(slide, dict):
                raise ValueError("Each slide must be a dictionary")
            if "title" not in slide or "content" not in slide or "theme" not in slide:
                raise ValueError("Each slide must have 'title', 'content', and 'theme' keys")
            if not isinstance(slide["title"], str):
                raise ValueError("Slide title must be a string")
            if not isinstance(slide["content"], list):
                raise ValueError("Slide content must be a list")
            if not isinstance(slide["theme"], str):
                raise ValueError("Slide theme must be a string")
        
        return slides_data
        
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse JSON response: {str(e)}")
    except Exception as e:
        raise Exception(f"Error generating slides: {str(e)}")

