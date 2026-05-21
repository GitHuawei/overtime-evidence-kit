# 证据包规格

## 包结构

证据包由三类核心对象和两类公开输出引用组成：

- 加班事件：描述日期、类型、时间、摘要、证据强度、风险和复核动作。
- 证据项：描述某条证据来自哪里、如何回查、对应哪个事件。
- 证据包：描述周期、主体角色、输入来源、事件列表、排除项和公开输出。
- mock report：面向人阅读的摘要。
- evidence index：面向回查的证据索引。

## 加班事件字段

- `eventId`
- `workDate`
- `eventType`
- `startTime`
- `endTime`
- `durationMinutes`
- `multiplier`
- `claimAmount`
- `workSummary`
- `evidenceStrength`
- `qualityGate`
- `riskFlags`
- `reviewAction`

`claimAmount` 在开源 mock 示例中保持 `0`，只作为结构占位，不代表真实主张金额。

## 证据项字段

- `evidenceId`
- `eventId`
- `sourceType`
- `sourceFileName`
- `sourceRowNum`
- `messageId`
- `timestamp`
- `senderRole`
- `sourceQuote`
- `quickLocator`
- `redactionLevel`
- `evidenceRole`

`quickLocator` 必须是 `sourceQuote` 的子串，便于从结构化证据项回查到 mock source。

`evidenceRole` 是可选字段，用于辅助 rules engine。允许值包括 `task_source`、`work_process`、`work_result`、`git_output`、`release_coordination`、`review_note`。

## 证据包字段

- `packageId`
- `periodStart`
- `periodEnd`
- `subjectRole`
- `inputSources`
- `events`
- `evidenceItems`
- `excludedCandidates`
- `validationReports`
- `publicOutputs`

## excludedCandidates

`excludedCandidates` 记录被排除的候选线索。它的意义是保持保守口径，说明并非所有晚间互动、周末消息或零散线索都应纳入。

每条排除项至少包含：

- `candidateId`
- `reason`

`reason` 必须非空，并说明为什么排除。

## riskFlags 白名单

允许值：

- `missing_end_time`
- `single_source_only`
- `unclear_task_owner`
- `sensitive_content_present`
- `needs_legal_review`
- `weak_result_evidence`
- `manual_review_required`

## validationReports

当前 MVP 中 `validationReports` 可以为空数组。实际校验结果由 validator CLI 输出，不要求写回 package。

## publicOutputs

`publicOutputs` 指向公开输出文件：

- `summaryMarkdown`: 例如 `mock-report.md`
- `evidenceIndexCsv`: 例如 `mock-evidence-index.csv`

公开输出不得包含真实隐私、真实案件事实或不必要的原始材料。

## 关键规则

- 每个 `evidenceItems[].eventId` 必须引用已存在的事件。
- 每个 included event 至少有一条证据项。
- `strong` 事件至少有 2 条证据，且来自至少 2 种 `sourceType`。
- 每个 `quickLocator` 必须是对应 `sourceQuote` 的子串。
- Git 证据的 commit 标识必须是 `mock-` 值。
- `workDate` 必须落在 package period 内。
- 公开示例只能使用 mock 数据。
