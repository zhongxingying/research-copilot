# app/routers/chat.py
from fastapi import APIRouter

from app.core.cost_tracker import cost_tracker
from app.core.logging import get_logger, trace_id_var
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.llm_client import llm_client

router = APIRouter(prefix="/api", tags=["chat"])
logger = get_logger(__name__)


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    messages = [{"role": m.role, "content": m.content} for m in req.history]
    messages.append({"role": "user", "content": req.message})

    data = await llm_client.chat(messages)
    reply = data["choices"][0]["message"]["content"]
    usage = data.get("usage")
    if usage:
        cost_tracker.record(usage)

    return ChatResponse(
        reply=reply,
        trace_id=trace_id_var.get(),
        model=data.get("model", llm_client.model),
        usage=usage,
    )
