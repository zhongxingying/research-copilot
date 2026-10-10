from dataclasses import dataclass

from app.core.logging import get_logger

logger = get_logger(__name__)

# 单位：元 / 百万 token
PRICE_INPUT = 1.0
PRICE_OUTPUT = 2.0


@dataclass
class CostRecord:
    input_tokens: int
    output_tokens: int

    @property
    def cost(self) -> float:
        return (
            self.input_tokens / 1_000_000 * PRICE_INPUT
            + self.output_tokens / 1_000_000 * PRICE_OUTPUT
        )


class CostTracker:
    def __init__(self) -> None:
        self.records: list[CostRecord] = []

    def record(self, usage: dict) -> CostRecord:
        rec = CostRecord(
            input_tokens=usage.get("prompt_tokens", 0),
            output_tokens=usage.get("completion_tokens", 0),
        )
        self.records.append(rec)
        logger.info(
            "cost_record",
            input_tokens=rec.input_tokens,
            output_tokens=rec.output_tokens,
            cost=round(rec.cost, 6),
        )
        return rec

    @property
    def total_cost(self) -> float:
        return sum(r.cost for r in self.records)


cost_tracker = CostTracker()
