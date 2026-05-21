# 公开输出字段白名单

本文档说明 `overtime-evidence-kit` 的公开输出应该展示什么、不能展示什么。目标是让用户理解 evidence package 的结构，而不是暴露原始材料或生成法律结论。

## 当前公开输出

- Markdown report: `examples/mock-evidence-package/mock-report.md`
- CSV evidence index: `examples/mock-evidence-package/mock-evidence-index.csv`
- demo 生成目录：`outputs/demo/`

`python scripts/check_all.py` 会检查 committed sample output 是否与 renderer 输出一致，也会在临时目录运行 demo。

## Markdown report 允许展示

- `packageId`
- `periodStart` / `periodEnd`
- `subjectRole`
- event id
- event type
- work date
- time range
- duration
- evidence strength
- quality gate
- risk flags
- review action
- work summary
- evidence id
- source type
- source file name
- source row num
- quick locator
- redaction level

## CSV evidence index 允许字段

当前 CSV header：

```text
evidenceId,eventId,eventType,workDate,sourceType,sourceFileName,sourceRowNum,messageId,quickLocator,redactionLevel
```

这些字段用于人工快速定位 mock evidence item。它们不应该暴露完整聊天原文、录音转写、源码或任何真实隐私信息。

## 不允许展示

公开输出不应包含：

- 完整原始聊天。
- 完整录音转写。
- 源码内容。
- 客户数据。
- 真实姓名。
- 真实公司。
- 真实项目。
- 真实手机号。
- 真实地址。
- 真实金额。
- 私有服务流程。
- 法律结论或结果承诺。

## 原则

- 最小披露。
- 可追溯但不暴露原文。
- mock-only。
- 不替代法律意见。
- 公开输出必须可由 renderer 重新生成。
- demo 输出应写入被忽略的 `outputs/demo/`，不提交到仓库。
