# hello-agent

首次使用时，在项目根目录将公共包安装到虚拟环境：

```bash
uv pip install --python .venv/bin/python --no-deps -e .
source .venv/bin/activate
```

之后可以直接运行各个示例，无需设置 `PYTHONPATH`：

```bash
python sections/01-agent-loop/demo.py
```

各个示例通过 `from schema.model import ModelReply, ToolCall` 导入公共类型。
这里使用可编辑安装，修改 `schema/` 中的 Python 代码会直接生效，无需重新安装。
安装与运行需要使用同一个虚拟环境；新建虚拟环境后需重新安装。
