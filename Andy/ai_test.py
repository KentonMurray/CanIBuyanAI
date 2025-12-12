#lm studio test
#works alright

from openai import OpenAI

client = OpenAI(base_url="http://10.203.44.180:1234/v1", api_key="not-needed")

prompt =  """
User: Hello, explain gravity simply.
Assistant:
"""

response = client.completions.create(
    model="google/gemma-3-4b",  # or lmstudio-community/gemma-3-4b
    prompt=prompt,
    max_tokens=30
)

print(response.choices[0].text)

