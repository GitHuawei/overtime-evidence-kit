# overtime-evidence-kit

![CI](https://github.com/GitHuawei/overtime-evidence-kit/actions/workflows/ci.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

**用完全虚构的 mock 数据演示：如何把加班线索整理成可校验、可复核、可展示的证据包。**

`overtime-evidence-kit` 是一个 **mock-only** 的开源工具包，用于演示加班证据结构化整理方法。它不处理真实案件材料，而是用虚构数据展示一条本地可运行的链路：mock source -> evidence package -> rules evaluation -> validation -> Markdown report -> CSV evidence index。

## 为什么值得看

加班证据整理最难的不是把聊天记录堆在一起，而是把任务来源、处理过程、结果反馈、时间窗口和证据定位组织成一套可复核结构。这个项目把这件事拆成 schema、validator、rules engine、report 和 evidence index，让方法可以被阅读、运行和讨论。

## 快速开始：三分钟 demo

```powershell
python scripts/run_demo.py
```

默认输出：

```text
outputs/demo/package.json
outputs/demo/mock-report.md
outputs/demo/mock-evidence-index.csv
```

`mock-evidence-index.csv` 使用 Excel-friendly UTF-8 with BOM，可在 Windows Excel 中直接打开。

## demo 结果预览

Markdown report 摘要片段：

```markdown
## 摘要

- 纳入事件数：4
- 证据项数：11
- 质量门：需复核: 2, 通过: 2
- 证据强度：中: 1, 强: 3

## 事件概览

| 事件ID | 类型 | 日期 | 时长 | 强度 | 质量门 | 风险 |
| --- | --- | --- | ---: | --- | --- | --- |
| evt-mock-weekday-001 | 工作日加班 | 2026-02-03 | 150 分钟 | 强 | 通过 | 无 |
```

CSV evidence index 片段：

```csv
证据ID,事件ID,事件类型,日期,来源类型,来源文件,来源行号,消息ID,快速定位,脱敏级别
evd-mock-chat-005,evt-mock-release-001,发布夜处理,2026-02-11,群聊,mock-wechat-export/messages.jsonl,5,mock-msg-005,观察 mock 指标,mock
```

完整示例：

- [Mock report](examples/mock-evidence-package/mock-report.md)
- [Evidence index CSV](examples/mock-evidence-package/mock-evidence-index.csv)

## 当前状态

当前状态：**v0.1.0 正式发布版**。

当前公开预览发布目标：**v0.2.0-public-preview**。该版本不增加真实材料处理能力，只用于把现有 mock-only 中文 demo、公开报告、Excel-friendly CSV 和安全边界作为公开预览版本展示。

已经包含：

- fictional mock 月份样例。
- JSON Schema。
- validator、rules engine、renderer。
- 一条命令 demo：`python scripts/run_demo.py`。
- 一键质量门：`python scripts/check_all.py`。
- 中文 Markdown report。
- 中文 CSV evidence index，带 UTF-8 BOM。
- FAQ、定位、用户安全、公开服务概览和发布检查文档。

## 能做什么

- 从仓库内 mock source 构建 mock evidence package。
- 为 mock events 计算 `evidenceStrength`、`qualityGate`、`riskFlags`、`reviewAction`。
- 校验 schema、时间顺序、证据覆盖和 mock-only 边界。
- 生成中文 public report 和中文 evidence index。
- 演示 JSON 机器值与人读展示标签的分离。

## 不能做什么

- 不导入真实微信、真实 Git、真实录音或用户本地真实文件。
- 不处理真实案件材料。
- 不提供 SaaS、账号系统或上传工作流。
- 不提供法律意见、法律结论或结果承诺。
- 不在公开仓库中接收真实证据。
- 不包含私有服务 SOP、收费交付流程或 paid pilot 材料。

## mock-only 边界

不要在 issue、PR、discussion、commit、测试、文档或附件中提交：

- 真实聊天、截图、导出记录或 message ID。
- 真实 Git commit、仓库名、源码或 commit hash。
- 真实录音、转写或会议纪要。
- 真实公司名、人名、项目名、客户名、地址、手机号、合同、工资、金额或身份标识。
- 任何可识别真实案件的信息组合。

不要把真实材料“脱敏后”提交到本仓库。示例必须从结构层重新虚构。

## 安全咨询入口

如果你想了解证据结构化整理协助，请先阅读：

- [FAQ](docs/faq.md)
- [Service overview](docs/service-overview.md)
- [Customer safety](docs/customer-safety.md)
- [Public business boundary](docs/business-boundary.md)

不要在 GitHub issue、PR 或 discussion 中粘贴真实材料。任何可能的私下咨询都应先确认授权、隐私边界、材料范围、保留/删除规则，并且不应被理解为法律意见。

## 质量门

```powershell
python scripts/check_all.py
python -m unittest discover -s tests -p "test_*.py"
git diff --check
```

`check_all.py` 覆盖 UTF-8/文本腐败扫描、JSON/JSONL 解析、demo、committed output consistency、CSV BOM、release readiness、unit tests 和敏感模式扫描。

## 文档

- [Demo guide](docs/demo.md)
- [GitHub Release notes](docs/github-release-v0.2.0-public-preview.md)
- [FAQ](docs/faq.md)
- [Positioning](docs/positioning.md)
- [Service overview](docs/service-overview.md)
- [Customer safety](docs/customer-safety.md)
- [Public outputs](docs/public-outputs.md)
- [Mock month walkthrough](docs/mock-month-walkthrough.md)
- [Validation rules](docs/validation-rules.md)
- [Evidence package spec](docs/evidence-package-spec.md)
- [Repository settings](docs/repository-settings.md)
- [Release checklist](docs/release-checklist.md)
- [Roadmap](docs/roadmap.md)
- [Contributing](CONTRIBUTING.md)
- [Security policy](SECURITY.md)
- [Changelog](CHANGELOG.md)

## 路线图

近期方向包括更多 fictional mock 场景、更清晰的 validator 错误说明、更好的报告格式和 local-only privacy-first adapter 设计文档。永久不纳入公开仓库范围：真实证据处理、自动法律结论、通过 GitHub 接收私有材料。

## License

本项目使用 MIT License。详见 [LICENSE](LICENSE)。
