# 完整 mock 月份 walkthrough

本文档帮助中文用户理解仓库内的 fictional mock 月份样例。所有数据都是虚构数据，只用于理解结构和本地 demo，不代表真实案件，也不提供法律意见。

## 文件关系

- `examples/mock-wechat-export/messages.jsonl`：mock chat source。
- `examples/mock-git-log/git-log.json`：mock Git source。
- `examples/mock-event-drafts/events.json`：mock event drafts。
- `examples/mock-evidence-package/package.json`：committed mock evidence package。
- `examples/mock-evidence-package/mock-report.md`：committed Markdown report。
- `examples/mock-evidence-package/mock-evidence-index.csv`：committed CSV evidence index。
- `outputs/demo/`：运行 `python scripts/run_demo.py` 后生成的 demo 输出目录。

## 推荐阅读顺序

1. 先读 `examples/mock-evidence-package/mock-report.md`，了解报告结构。
2. 再读 `examples/mock-evidence-package/mock-evidence-index.csv`，了解证据索引字段。
3. 查看 `examples/mock-evidence-package/package.json` 的 `events` 和 `evidenceItems`。
4. 回到 `examples/mock-wechat-export/messages.jsonl` 和 `examples/mock-git-log/git-log.json`，理解 mock source 如何映射到 evidence item。
5. 查看 `excludedCandidates`，理解为什么有些候选线索没有纳入 included events。

## 一条命令 demo

```powershell
python scripts/run_demo.py
```

demo 会把生成物写入：

```text
outputs/demo/
```

生成文件：

- `outputs/demo/package.json`
- `outputs/demo/mock-report.md`
- `outputs/demo/mock-evidence-index.csv`

`outputs/demo/` 已被 `.gitignore` 忽略，不应提交。

## 公开输出如何阅读

`mock-report.md` 面向 GitHub 阅读场景，包含：

- `Summary`：月份范围、事件数量、证据数量、质量门分布和证据强度分布。
- `Event Overview`：事件表格，适合快速扫描。
- `Evidence Index Preview`：每个事件关联的证据项简表。
- `Included Events`：逐个事件的摘要、时间、风险、复核动作和证据列表。
- `Review Notes`：需要人工复核的 mock events 和原因。
- `Boundaries`：mock-only 与非法律意见提醒。

`mock-evidence-index.csv` 面向证据定位，包含 event 类型、日期、source 文件名和 source 行号。它不包含完整 `sourceQuote`。

## 当前 included events

- `evt-mock-weekday-001`：weekday overtime mock event，证据强度为 `strong`，质量门为 `pass`。
- `evt-mock-weekday-002`：weekday overtime mock event，证据强度为 `medium`，质量门为 `needs_review`。
- `evt-mock-release-001`：release night mock event，证据强度为 `strong`，质量门为 `pass`。
- `evt-mock-rest-001`：rest day task mock event，证据强度为 `strong`，质量门为 `needs_review`。

这些事件只是结构示例，不代表真实工作安排、真实项目或真实案件。

## Excluded candidates 的意义

`excludedCandidates` 体现保守口径。不是所有晚间互动、周末消息或零散确认都应纳入 included events。

当前 mock 示例包含：

- 只有普通日间沟通，未进入加班时段。
- 只有确认收到，没有任务处理过程和结果。
- 时长不足且证据来源单薄。

## 如何回查 evidence item

以 `evd-mock-chat-001` 为例：

1. 查看 `eventId`，确认它属于 `evt-mock-weekday-001`。
2. 查看 `sourceFileName`，定位到 `mock-wechat-export/messages.jsonl`。
3. 查看 `sourceRowNum`，定位到对应 source 行。
4. 查看 `messageId` 和 `quickLocator`，确认定位信息。

Git evidence item 类似，只是 `messageId` 使用 `mock-` commit 标识。

## 常用命令

```powershell
python scripts/run_demo.py
python scripts/check_all.py
python scripts/validate_evidence_package.py examples/mock-evidence-package/package.json
python scripts/render_mock_report.py examples/mock-evidence-package/package.json
python scripts/render_evidence_index.py examples/mock-evidence-package/package.json
```

## 重要提醒

本仓库只接受 fictional mock data。不要把真实聊天、真实 Git、真实录音、真实公司名、人名、项目名、金额、地址、手机号或任何可识别真实案件的信息提交到公开仓库。
