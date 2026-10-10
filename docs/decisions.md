# ADR-001: 用 pgvector 而不是 Pinecone

## 状态
已接受

## 背景
需要向量数据库支持 RAG 检索。

## 决策
用 PostgreSQL + pgvector。

## 理由
- 数据本地可控，不出内网
- 和 papers/chunks 关系表在同一个库，方便 join
- 成本低，无托管费用
- 支持 IVFFlat / HNSW 索引

## 代价
- 需要自己运维 PostgreSQL
- 大规模（>1 亿向量）时性能不如专用向量库

## 替代方案
Pinecone：托管，但数据要出本地，成本随规模涨。


# ADR-002: 用 BGE-M3 而不是 text-embedding-3-small

## 状态
已接受

## 背景
需要 Embedding 模型把论文分块向量化。

## 决策
用 BGE-M3（本地部署，1024 维）。

## 理由
- 本地跑，无 API 费用
- 中文英文都支持
- 1024 维，比 text-embedding-3-small 的 1536 维省存储
- 支持多语言、多粒度

## 代价
- 需要 GPU 或 CPU 推理，首次加载慢
- 需要自己维护模型版本

## 替代方案
text-embedding-3-small：OpenAI 托管，但按 token 收费，数据出本地。


# ADR-003: 用 DeepSeek 而不是 GPT-4

## 状态
已接受

## 背景
需要 LLM 做意图分类、RAG 回答、Agent 规划。

## 决策
用 DeepSeek API。

## 理由
- 价格便宜（约为 GPT-4 的 1/50）
- 中文支持好
- 兼容 OpenAI SDK，迁移成本低
- 有 deepseek-chat 和 deepseek-reasoner 两个模型

## 代价
- 生态不如 OpenAI 成熟
- 部分高级功能（如 function calling 的复杂 schema）可能不如 GPT-4

## 替代方案
GPT-4：贵，但生态好；Claude：贵，但长上下文好。

# ADR-004: 用 trace_id + 结构化日志

## 状态
已接受

## 背景
FastAPI 并发处理请求，普通日志无法区分哪几行属于同一次请求。
排查线上问题时，需要把一次请求的所有日志串起来。

## 决策
1. 用 ContextVar 存 trace_id，中间件生成并注入响应头 X-Trace-Id。
2. 用 structlog 输出 JSON 日志，每行带 trace_id。

## 理由
- trace_id 让一次请求的所有日志可 grep
- JSON 日志可被 LangFuse/ELK 采集
- ContextVar 天然协程安全，不污染全局

## 代价
- 日志体积变大（JSON 比纯文本长）
- structlog 用法和标准 logging 不同，需要适应

## 替代方案
- 只用标准 logging：无法结构化，采集困难
- 用 OpenTelemetry：功能更强，但 W1 阶段过重