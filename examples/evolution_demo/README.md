# 一次运行 Demo

这不是依赖剪映的工程。把本地视频复制到 `MEDIA/`，按 `assets.example.json` 填写路径和时间点，再运行：

```powershell
python apps/render_demo.py `
  --brief examples/evolution_demo/prompt.md `
  --manifest examples/evolution_demo/assets.example.json `
  --output outputs/evolution-demo.mp4
```

同一份提示词、同一份素材清单和同一版本代码，会得到同一套画面安排。模型的工作是把自然语言需求整理成这份提示词和 JSON 时间线；渲染本身是确定性的。

素材目录和 BGM 不进仓库。这个示例使用本地素材路径，方便在拥有素材使用权的机器上复现。
