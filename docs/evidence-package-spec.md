# 证据包规格

## 包结构

证据包由三类对象组成：

- 加班事件：描述日期、类型、时间、摘要、证据强度和风险。
- 证据项：描述某条证据来自哪里、如何回查、对应哪个事件。
- 证据包：描述周期、主体角色、输入来源、事件列表、排除项和公开输出。

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

## 关键规则

- 每个 `evidenceItems[].eventId` 必须引用已存在的事件。
- 每个 `quickLocator` 必须是对应 `sourceQuote` 的子串。
- Git 证据的 commit hash 必须是 mock 值。
- 公开输出不得包含真实身份、真实公司、真实地址、手机号或真实案件细节。

