# bailong-video

Python 库源码位于 `src/bailong_video`，由仓库根目录的 `pyproject.toml` 统一打包。

当前为可安装、可导入的包骨架。各 `agent.py`、`tools.py` 等文件只预留模块位置，不包含核心执行代码。

在仓库根目录运行：

```bash
python -m pip install .
```

后续模块沿用此包组织方式，应用层通过库接口接入。
