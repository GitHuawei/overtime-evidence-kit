# 完整 mock 月份 walkthrough

## 文件关系

- `examples/mock-wechat-export/messages.jsonl`：mock 聊天输入。
- `examples/mock-git-log/git-log.json`：mock Git 输入。
- `examples/mock-evidence-package/package.json`：整理后的结构化证据包。
- `examples/mock-evidence-package/mock-report.md`：人读摘要。
- `examples/mock-evidence-package/mock-evidence-index.csv`：证据索引。

这些文件全部是虚构数据，只用于理解结构。

## 建议阅读顺序

1. 先读 `mock-report.md`，了解月份摘要。
2. 再读 `package.json` 的 `events`。
3. 查看 `evidenceItems` 如何引用事件。
4. 回到 `messages.jsonl` 或 `git-log.json` 查 mock source。
5. 查看 `excludedCandidates` 理解保守口径。

## Included events

### evt-mock-weekday-001

- 类型：`weekday_overtime`。
- 场景：订单系统示例接口联调。
- 证据构成：2 条聊天证据，1 条 Git 证据。
- 证据强度：`strong`。
- 风险标记：无。
- 复核动作：确认聊天时间线与 mock Git 记录一致。

### evt-mock-weekday-002

- 类型：`weekday_overtime`。
- 场景：客服后台示例线上问题排查。
- 证据构成：2 条群聊证据。
- 证据强度：`medium`。
- 风险标记：`weak_result_evidence`。
- 复核动作：补充 mock 系统截图或更多结果确认记录。

### evt-mock-release-001

- 类型：`release_night`。
- 场景：BI 报表服务 mock 发布夜观察。
- 证据构成：2 条群聊证据，1 条 Git 证据。
- 证据强度：`strong`。
- 风险标记：无。
- 复核动作：复核发布观察记录与 mock Git 记录是否对应。

### evt-mock-rest-001

- 类型：`rest_day_task`。
- 场景：休息日 mock 数据修复任务。
- 证据构成：2 条聊天证据，1 条 Git 证据。
- 证据强度：`medium`。
- 风险标记：`manual_review_required`。
- 复核动作：人工确认休息日任务来源和处理结果是否足够。

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
3. 查看 `sourceRowNum`，定位到第 1 行。
4. 查看 `messageId`，确认第 1 行是 `mock-msg-001`。
5. 查看 `quickLocator`，确认它是 `sourceQuote` 的子串。

Git 证据类似，只是 `messageId` 使用 `mock-` commit 标识。

## 运行命令

```powershell
python scripts/check_all.py
python scripts/validate_evidence_package.py examples/mock-evidence-package/package.json
python scripts/render_mock_report.py examples/mock-evidence-package/package.json
python scripts/render_evidence_index.py examples/mock-evidence-package/package.json
```

## 重要提醒

该月份只是开源预览样例，不代表法律结论，也不应替换为真实材料后提交到公开仓库。
