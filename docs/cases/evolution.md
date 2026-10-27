# EVOLUTION · 可复现交付案例

这是本地《双城之战》视觉剪辑的整理版。仓库只保存方法、提示词、时间线和校验信息；影视片源、BGM、角色语音和完整工程媒体不随仓库分发。

## 一次运行

```powershell
python -m bailong_video.demo `
  --brief examples/evolution_demo/prompt.md `
  --manifest examples/evolution_demo/assets.example.json `
  --output outputs/evolution-demo.mp4
```

运行只依赖本地 FFmpeg、一个提示词和一份素材清单，不需要打开剪映。提示词负责表达目标风格，JSON 负责保存已经确认的画面、时间点和位置；因此同一输入会产生可重复的结果。

## 复用原则

- 先重新分析新 BGM 的重拍和碎拍，再生成 `beats`。
- 先给素材建立动作方向、主体位置和来源记录，再选择镜头。
- 小窗、文字和闪白只服务节拍与视觉阅读，不覆盖主画面。
- 输出后运行清晰度、帧率、黑帧、音频峰值和重复素材检查。

## 本次交付索引

交付文件的本地位置记录在 `examples/deliverables_manifest.json`。视频和工程体积较大，应上传到网盘或对象存储，再把下载地址写入该清单；GitHub 保留代码和说明。
