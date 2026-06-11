import os
from groq import AsyncGroq
from app.core.config import settings
from typing import List, Dict

client = AsyncGroq(api_key=settings.GROQ_API_KEY)

async def generate_response(system_prompt: str, context: List[Dict[str, str]]) -> str:
    conversation_history = "\n".join([msg["content"] for msg in context])
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Here is the debate so far:\n{conversation_history}\n\nPlease provide your next response speaking as your persona. Remember the length constraints."}
    ]
    try:
        completion = await client.chat.completions.create(
            messages=messages,
            model=settings.GROQ_MODEL,
            temperature=0.7,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Groq Error: {e}")
        return "I am currently lost in thought."
