# 公开输出字段白名单

## 目标

公开输出用于开源预览、教学和结构讨论。它应帮助用户理解 evidence package，而不是暴露原始材料或生成法律意见。

## Markdown report 允许字段

- package id。
- period。
- subject role。
- event id。
- event type。
- work date。
- time range。
- duration。
- evidence strength。
- quality gate。
- risk flags。
- review action。
- work summary。
- evidence id。
- source type。
- source file name。
- source row num。
- message id。
- quick locator。
- redaction level。

## CSV evidence index 允许字段

- `evidenceId`
- `eventId`
- `eventType`
- `workDate`
- `sourceType`
- `sourceFileName`
- `sourceRowNum`
- `messageId`
- `quickLocator`
- `redactionLevel`

## 不允许字段

- 完整原始聊天。
- 完整录音转写。
- 源码。
- 客户数据。
- 真实姓名。
- 真实公司。
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

## 当前输出

- Markdown: `examples/mock-evidence-package/mock-report.md`
- CSV: `examples/mock-evidence-package/mock-evidence-index.csv`

两个文件都应与 renderer 输出保持一致，`python scripts/check_all.py` 会检查这一点。
