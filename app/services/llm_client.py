# app/services/llm_client.py
import httpx

from app.core.config import settings
from app.core.exceptions import LLMError
from app.core.logging import get_logger

logger = get_logger(__name__)


class LLMClient:
    def __init__(self) -> None:
        self.base_url = settings.llm_base_url.rstrip("/")
        self.api_key = settings.llm_api_key
        self.model = settings.llm_model

    async def chat(self, messages: list[dict], temperature: float = 0.7) -> dict:
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.post(url, headers=headers, json=payload)
                resp.raise_for_status()
                return resp.json()
        except httpx.HTTPStatusError as e:
            logger.error("LLM HTTP error: %s", e.response.text)
            raise LLMError(f"LLM 返回错误：{e.response.status_code}") from e
        except httpx.RequestError as e:
            logger.error("LLM request error: %s", e)
            raise LLMError("LLM 网络错误") from e


llm_client = LLMClient()
