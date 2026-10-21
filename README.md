# 🐉 Bailong Video Agent · 白龙娘视频工作流

**把视频创作拆成可组合的 Agent、工具与流程。**

> 白龙娘还在整理，核心实现将分批上传。
>
> 本次先开放工程结构、模块划分、流程配置草案与 Python 包骨架。后续会逐步开放可独立使用的模块，并配套示例与使用文档。

从热点选题到素材理解，从音乐分析到剪辑规划，再到成片输出，Bailong Video Agent 围绕创作中的不同任务划分模块。可以从热点发现开始，也可以跳过这一步，直接带着素材和想法进入创作流程。

## 流程设计

```mermaid
flowchart TD
    A["热点发现 / 舆情分析 · 可选"] --> B["素材检索与整理"]
    U["用户提供素材 / 参考视频"] --> C["素材理解与参考学习"]
    B --> C
    C --> D["理解用户需求 · 选择剪辑路线"]
    D --> E["卡点路线"]
    D --> F["故事路线"]
    E --> G["BGM 结构 / 节拍 / 底鼓 / 乐器线索"]
    F --> H["叙事结构 / 事件顺序 / 旁白规划"]
    G --> I["镜头选择与时间线规划"]
    H --> I
    I --> J["剪辑工程 / 渲染 / 成片检查"]
```

这里的“学习”指对素材、参考视频和剪辑规律的分析与整理，不等同于训练模型。用户可以提供 5～10 个素材或参考片段作为起点，数量按项目需要调整。

## 模块地图

| 模块 | 关注的问题 | 预留入口 |
| --- | --- | --- |
| 热点分析 | 现在有什么值得做？讨论焦点、来源与时效是什么？ | `modules/trends/` |
| 素材整理 | 有哪些可用镜头？如何检索、归档、去重与保留来源？ | `modules/media/` |
| 参考学习 | 素材讲了什么？参考片段如何安排镜头、节奏和转场？ | `modules/learning/` |
| 需求理解 | 用户更重视卡点、叙事、角色、时长还是画幅？ | `modules/intent/` |
| 音频分析 | 节拍、段落、底鼓与乐器线索如何辅助剪辑？ | `modules/audio/` |
| 剪辑规划 | 哪个镜头适合哪个位置？如何组织故事或音乐段落？ | `modules/editing/` |
| 输出与检查 | 如何对接剪辑工程、渲染文件并检查成片？ | `modules/render/` |

以上为模块划分与开放范围设计，发布进度见 [开放清单](docs/roadmap.md)。

## 仓库结构

```text
bailong-video-agent/
├── packages/
│   └── bailong-video/
│       └── src/bailong_video/
│           ├── agent.py         # 总调度入口预留
│           ├── tools.py         # 工具注册入口预留
│           ├── pipeline.py      # 流程编排入口预留
│           ├── models.py        # 数据契约入口预留
│           └── modules/
│               ├── trends/      # 热点与舆情
│               ├── media/       # 素材检索与整理
│               ├── learning/    # 素材理解与参考分析
│               ├── intent/      # 创作需求与路线选择
│               ├── audio/       # 音乐与音频分析
│               ├── editing/     # 卡点与故事剪辑
│               └── render/      # 工程输出与成片检查
├── apps/                        # CLI、Web 等使用入口规划
├── workflows/                   # 可组合流程草案
├── examples/                    # 输入清单与配置示例
├── docs/                        # 架构、工具边界与开放进度
└── pyproject.toml               # Python 包安装配置
```

采用 monorepo 组织方式，当前 Python 库集中在 `packages/bailong-video`；应用入口、流程配置和文档在同一仓库维护。

## 安装当前包骨架

需要 Python 3.10 或以上版本：

```bash
git clone https://github.com/Thedan-1/bailong-video-agent.git
cd bailong-video-agent
python -m pip install .
python -c "import bailong_video; print('bailong_video imported')"
```

当前安装内容为包骨架，不包含核心执行实现或可运行的剪辑命令。完整调用示例会随对应模块上传，暂不提供 PyPI 安装入口。

## 从哪里开始阅读

- [架构与数据流](docs/architecture.md)：模块如何衔接，哪些步骤可以跳过。
- [工具目录](docs/tools.md)：卡点、故事与素材分析分别需要哪些工具。
- [开放清单](docs/roadmap.md)：当前公开内容与后续整理顺序。
- [流程配置](workflows/README.md)：从热点开始，或直接使用本地素材。
- [输入示例](examples/README.md)：如何描述素材、参考片段和创作需求。

## 素材与贡献

仓库只收录工程结构与项目自身内容，不附带影视片源、商业音乐、账号凭据或私人创作资料。素材来源、使用许可和署名信息应随素材记录保留。

欢迎通过 Issue 交流模块建议、输入输出设计与使用场景。提交贡献前请阅读 [贡献说明](CONTRIBUTING.md)。

**代码与文档许可：** [MIT](LICENSE)。该许可不覆盖外部素材、角色、音乐或第三方服务。

—— 爱剪视频的白龙娘 · maintained by [Thedan-1](https://github.com/Thedan-1)
