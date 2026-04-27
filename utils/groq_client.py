"""
groq_client.py
--------------
Handles all communication with the Groq API.
Groq provides extremely fast LLM inference (llama3-8b-8192).

Model: llama3-8b-8192
- 8B parameter model, very fast on Groq's LPU hardware
- 8192 token context window
- Free tier available at console.groq.com
"""

import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_groq_client() -> Groq:
    """
    Initialize and return a Groq API client.

    Returns:
        Groq client instance.

    Raises:
        EnvironmentError: If GROQ_API_KEY is not set.
    """
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key or api_key == "your_groq_api_key_here":
        raise EnvironmentError(
            "GROQ_API_KEY is not set. "
            "Please add your key to the .env file. "
            "Get a free key at: https://console.groq.com"
        )

    return Groq(api_key=api_key)


def generate_answer(
    client: Groq,
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.2,
    max_tokens: int = 1024,
) -> str:
    """
    Send a prompt to Groq and return the generated response.

    Args:
        client: Groq client instance.
        system_prompt: Instructions for how the AI should behave.
        user_prompt: The actual question + context.
        temperature: 0.2 = more deterministic / factual answers.
        max_tokens: Max response length (1024 is good for student answers).

    Returns:
        String response from the AI model.

    Raises:
        Exception: On API errors (rate limit, invalid key, etc.)
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return response.choices[0].message.content

    except Exception as e:
        error_msg = str(e)

        # Provide helpful error messages for common issues
        if "401" in error_msg or "invalid_api_key" in error_msg:
            raise Exception(
                "Invalid Groq API key. Please check your .env file."
            )
        elif "429" in error_msg or "rate_limit" in error_msg:
            raise Exception(
                "Groq API rate limit reached. Please wait a moment and try again."
            )
        elif "503" in error_msg or "unavailable" in error_msg:
            raise Exception(
                "Groq API is temporarily unavailable. Please try again in a few seconds."
            )
        else:
            raise Exception(f"Groq API error: {error_msg}")
