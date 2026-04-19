import json
import re
from transformers import pipeline
from app.core.config import settings
from concurrent.futures import ThreadPoolExecutor, TimeoutError


class LLMService:
    def __init__(self):
        self.generator = pipeline(
            "text2text-generation",
            model=settings.MODEL_NAME,
            device=-1,  # CPU (use 0 if GPU available)
        )

        self.executor = ThreadPoolExecutor(max_workers=2)

    def generate(self, prompt: str, timeout: int = 5) -> dict | None:
        """
        Generate structured AI response with timeout & safe parsing
        """

        try:
            future = self.executor.submit(self._run_model, prompt)
            raw_output = future.result(timeout=timeout)

            # parsed = self._extract_json(raw_output)
            return raw_output
        
        except Exception as e:
            print("LLM ERROR:", repr(e))
            return None
        except TimeoutError:
            return None
        except Exception:
            return None

    def _run_model(self, prompt: str) -> str:
        response = self.generator(
            prompt,
            max_new_tokens=settings.MAX_TOKENS,
            do_sample=False,   # deterministic
            num_beams=3,
        )
        return response[0]["generated_text"]

    def _extract_json(self, text: str):
        if not text:
            return None

        try:
            # 🔥 Step 1: Try direct parse
            return json.loads(text)

        except:
            pass

        try:
            # 🔥 Step 2: Extract JSON-like content
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                return json.loads(match.group(0))
        except:
            pass

        try:
            # 🔥 Step 3: Fix common LLM issues
            fixed = text.strip()

            # Add braces if missing
            if not fixed.startswith("{"):
                fixed = "{" + fixed
            if not fixed.endswith("}"):
                fixed = fixed + "}"

            # Fix broken null
            fixed = fixed.replace('"null', 'null').replace('null"', 'null')

            # Fix trailing commas / quotes
            fixed = re.sub(r',\s*}', '}', fixed)

            return json.loads(fixed)

        except:
            return None


llm_service = LLMService()