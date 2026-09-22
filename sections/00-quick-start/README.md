# LangGraph quickstart

在项目根目录运行 `uv sync` 安装依赖。

在根目录 `.env` 中填写以下配置（也可以通过终端 export 设置）：

```dotenv
OPENROUTER_API_KEY=你的 OpenRouter API key
OPENROUTER_MODEL=openai/gpt-4.1-mini
```

脚本使用 `ChatOpenRouter`，只需要 OpenRouter key。模型需要支持工具调用。
已有环境变量优先于 `.env` 中的值。`.env.example` 提供配置模板。

```bash
uv run sections/00-quick-start/quick-start.py
```

示例计算 3 + 4，并打印消息和工具调用结果。真实请求使用 OpenRouter 账户额度。
如需生成流程图，加上 `--draw-graph`；此选项需要访问 Mermaid 绘图服务，
图片保存为脚本同目录下的 `graph.png`。

若返回服务商权限或条款相关的 403，请检查 OpenRouter Activity 中的失败记录；
配置正确并不保证账户有权访问所有模型。

原始教程：https://docs.langchain.com/oss/python/langgraph/quickstart
