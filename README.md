# Research Copilot

一个能读论文、对比论文、写综述的科研助手。

## 怎么跑

### 1. 装依赖

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

### 2. 配环境变量

cp .env.example .env
# 编辑 .env，填入 LLM_API_KEY

### 3. 启 PostgreSQL

sudo service postgresql start
sudo -u postgres psql -c "CREATE DATABASE research_copilot;"
sudo -u postgres psql -d research_copilot -c "CREATE EXTENSION vector;"

### 4. 跑测试

pytest tests/ -v
