# scripts/measure_context.py
import asyncio

from app.core.context_monitor import context_usage
from app.services.llm_client import llm_client


async def run_rounds(n: int) -> dict:
    messages = [{"role": "system", "content": "你是一个科研助手。"}]
    for i in range(n):
        messages.append({"role": "user", "content": f"第 {i+1} 轮：解释一下 Transformer。"})
        data = await llm_client.chat(messages)
        reply = data["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": reply})
    return context_usage(messages)


async def main():
    for n in [1, 5, 20]:
        usage = await run_rounds(n)
        print(f"轮数={n} usage={usage}")


if __name__ == "__main__":
    asyncio.run(main())
