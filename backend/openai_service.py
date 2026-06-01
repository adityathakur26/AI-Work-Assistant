import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def generate_ai_coach(data):

    prompt = f"""
You are an elite productivity coach.

Analyze this productivity data:

{data}

Return ONLY valid JSON:

{{
  "summary":"",
  "assessment":"",
  "recommendations":[
      "",
      "",
      ""
  ]
}}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4
    )

    return response.choices[0].message.content