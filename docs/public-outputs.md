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

当前 CSV header 已中文化：

```text
证据ID,事件ID,事件类型,日期,来源类型,来源文件,来源行号,消息ID,快速定位,脱敏级别
```

这些字段用于人工快速定位 mock evidence item。package JSON key 和 schema field name 仍保持英文不变，CSV header 是面向人读的公开输出。CSV 文件使用 Excel-friendly UTF-8 with BOM，便于 Windows Excel 双击打开时正确识别中文。CSV 不应该暴露完整聊天原文、录音转写、源码或任何真实隐私信息。

## 机器值与展示标签

JSON package 保留机器字段和机器枚举值，便于 schema、validator、rules engine 和测试稳定运行。公开报告和 CSV evidence index 使用中文展示标签，便于人工阅读。

示例：

- `weekday_overtime` -> `工作日加班`
- `release_night` -> `发布夜处理`
- `rest_day_task` -> `休息日任务`
- `pass` -> `通过`
- `needs_review` -> `需复核`
- `single_source_only` -> `证据来源单一`
- `manual_review_required` -> `需要人工复核`
- `wechat` -> `单聊`
- `group_chat` -> `群聊`
- `git` -> `Git 记录`
- `strong` -> `强`
- `medium` -> `中`
- `weak` -> `弱`

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
