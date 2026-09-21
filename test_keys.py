import httpx
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_KEYS = [
    key.strip()
    for key in os.getenv("GROQ_API_KEYS", os.getenv("GROQ_API_KEY", "")).split(",")
    if key.strip()
]

if not GROQ_KEYS:
    print("No GROQ_API_KEY or GROQ_API_KEYS configured.")
    raise SystemExit(0)

for i, key in enumerate(GROQ_KEYS):
    try:
        resp = httpx.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'},
            json={'model': 'openai/gpt-oss-120b', 'messages': [{'role': 'user', 'content': 'Say hi'}]},
            timeout=10.0
        )
        status = 'WORKING' if resp.status_code == 200 else f'FAILED ({resp.status_code})'
        print(f'Key {i+1}: {status}')
    except Exception as e:
        print(f'Key {i+1}: ERROR ({e})')