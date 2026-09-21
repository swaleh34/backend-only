"""
SWALEH AI - Unlimited Free LLM
Powered by Puter API Bridge (GPT-4o, Claude, Gemini, 500+ models)
"""
import httpx
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import re

load_dotenv()

SWALEH_SYSTEM_PROMPT = """You are Swaleh AI (صالح), an advanced Islamic AI assistant.

IDENTITY:
- You are SWALEH AI - created specifically for Islamic knowledge
- You are NOT OpenAI, NOT ChatGPT, NOT GPT, NOT Claude, NOT Gemini
- NEVER mention OpenAI, ChatGPT, or any other AI company
- Always identify yourself as "Swaleh AI"
- NEVER mention training data cutoff dates
- NEVER mention October 2023 or any date
- NEVER speculate about your underlying model
- If asked about your knowledge date, say: "My knowledge is based on the timeless Quran and Sunnah"
- NEVER mention technical details (parameters, architecture, context window, base model)


PURPOSE:
- Answer Islamic questions based on Quran and authentic Sunnah
- Provide accurate information about Islam, Hadith, Fiqh, Seerah
- Help users learn about their faith

RULES:
- Use ﷺ after Prophet Muhammad's name
- Use رضي الله عنه (RA) for companions
- Use عليه السلام (AS) for prophets
- Cite sources: Quran [Surah:Verse], Hadith [Collection]
- Be respectful and accurate
- Say "Allahu A'lam" when uncertain
- Write in plain text (NO markdown, NO ###, NO **, NO ---)
- NEVER mention training data cutoff dates
- NEVER mention October 2023 or any date
-NEVER speculate about your underlying model
- If asked about your knowledge date, say: "My knowledge is based on the timeless Quran and Sunnah"
- NEVER mention technical details (parameters, architecture, context window, base model)
"""
GROQ_KEYS = [
    key.strip()
    for key in os.getenv("GROQ_API_KEYS", os.getenv("GROQ_API_KEY", "")).split(",")
    if key.strip()
]

class FreeLLM:
    def __init__(self):
        self.puter_url = "http://127.0.0.1:8741/v1/chat/completions"
        self.puter_available = False
        self.key_index = 0
        self._check_services()
    
    def _check_services(self):
        try:
            resp = httpx.get("http://127.0.0.1:8741/v1/models", timeout=3.0)
            self.puter_available = resp.status_code == 200
        except:
            self.puter_available = False
        
        print(f"🆓 Swaleh AI LLM Status:")
        print(f"   Puter (Unlimited): {'✅ GPT-4o Ready' if self.puter_available else '❌ Not running'}")
        print(f"   Groq Keys: {len(GROQ_KEYS)} ready")
    
    def ask(self, query: str) -> Optional[Dict[str, Any]]:
        """Never returns None - always has a graceful response"""
        errors = []
        
        # Try Puter first
        if self.puter_available:
            try:
                result = self._try_puter(query)
                if result:
                    return result
            except Exception as e:
                errors.append(f"Puter: {e}")

        for attempt in range(len(GROQ_KEYS)):
            try:
                key = GROQ_KEYS[self.key_index]
                self.key_index = (self.key_index + 1) % len(GROQ_KEYS)
                result = self._try_groq_with_key(query, key)
                if result:
                    return result
            except Exception as e:
                errors.append(f"Groq Key {attempt+1}: {e}")
        
        # ALL providers failed - return graceful message
        return {
            "answer": "I apologize, but I am currently experiencing high demand. Please try again in a moment. JazakAllahu Khairan for your patience.",
            "source": "fallback",
            "confidence": 0.1
        }
    
    def _try_puter(self, query: str) -> Optional[Dict[str, Any]]:
        try:
            resp = httpx.post(
                self.puter_url,
                json={
                    "model": "gpt-4o",
                    "messages": [
                        {"role": "system", "content": SWALEH_SYSTEM_PROMPT},
                        {"role": "user", "content": query}
                    ],
                    "temperature": 0.1,
                    "max_tokens": 2000
                },
                timeout=60.0
            )
            if resp.status_code == 200:
                answer = resp.json()["choices"][0]["message"]["content"]
                return {"answer": self._clean_response(answer), "source": "puter", "confidence": 0.98}
        except:
            pass
        return None
    
    def _try_groq_with_key(self, query: str, key: str) -> Optional[Dict[str, Any]]:
        try:
            resp = httpx.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
                json={
                    "model": "openai/gpt-oss-120b",
                    "messages": [
                        {"role": "system", "content": SWALEH_SYSTEM_PROMPT},
                        {"role": "user", "content": query}
                    ],
                    "temperature": 0.1,
                    "max_tokens": 1500
                },
                timeout=20.0
            )
            if resp.status_code == 200:
                answer = resp.json()["choices"][0]["message"]["content"]
                return {"answer": self._clean_response(answer), "source": "groq", "confidence": 0.95}
        except:
            pass
        return None
    
    def _clean_response(self, text: str) -> str:
        """Remove all markdown and AI-identifying language"""
        # Remove markdown symbols
        text = text.replace('###', '').replace('**', '').replace('---', '')
        text = text.replace('__', '').replace('*', '').replace('<>', '')
        text = text.replace('```', '')
        # Remove AI identity mentions
        text = text.replace('OpenAI', '').replace('ChatGPT', '').replace('GPT-4', '')
        text = text.replace('Claude', '').replace('Anthropic', '')
        text = text.replace('I am an AI developed by', 'I am Swaleh AI,')
        text = text.replace('I am an AI assistant', 'I am Swaleh AI')
        text = text.replace('I am an AI', 'I am Swaleh AI')
        text = text.replace('ChatGPT', 'Swaleh AI')
        text = text.replace('OpenAI', '')
        text = text.replace('GPT-4', '')
        text = text.replace('Claude', '')
        text = text.replace('Anthropic', '')
        # Clean extra spaces
        import re
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text

free_llm = FreeLLM()