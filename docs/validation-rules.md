# Validator 规则

## Error 与 Warning

- Error：结构、安全或一致性问题，必须修复。
- Warning：需要人工复核，但不阻断当前 mock 包通过。

CLI 输出规则：

- 成功：`OK: <path> passed validation`
- 警告：`WARNING: ...`
- 失败：`ERROR: ...`

## 规则列表

### JSON Schema

检查必填字段、类型、枚举、`additionalProperties: false`、日期和时间格式。

### Event 引用

每个 `evidenceItems[].eventId` 必须引用已存在的 event。

### quickLocator 子串

`quickLocator` 必须是 `sourceQuote` 的子串。

### Git mock 前缀

Git evidence 的 `messageId` 必须以 `mock-` 开头。

### 时间顺序

每个 event 必须满足 `startTime < endTime`。

### duration 一致

`durationMinutes` 必须等于 `endTime - startTime` 的分钟差。

### Period 范围

`periodStart <= periodEnd`。

### workDate 范围

每个 `events[].workDate` 必须落在 package period 内。

### riskFlags 白名单

允许值：

- `missing_end_time`
- `single_source_only`
- `unclear_task_owner`
- `sensitive_content_present`
- `needs_legal_review`
- `weak_result_evidence`
- `manual_review_required`

### evidence coverage

每个 included event 至少需要一条 evidence item。

### strong event 多来源

`evidenceStrength: strong` 的 event 至少需要 2 条 evidence item，且来自至少 2 种 `sourceType`。

### excluded reason

`excludedCandidates[].reason` 必须说明排除原因，不能为空或过短。

### timestamp warning

如果 evidence timestamp 距离 linked event 的时间范围超过 24 小时，validator 输出 warning。

### sourceRowNum 对齐

对 mock JSONL 来源，validator 检查 `sourceRowNum` 对应行的 `messageId` 是否一致。

### evidenceRole

可选字段 `evidenceRole` 必须来自白名单：

- `task_source`
- `work_process`
- `work_result`
- `git_output`
- `release_coordination`
- `review_note`

Rules engine 使用该字段推导证据强度、风险标记和复核动作。

### 敏感信息扫描

检查：

- 手机号样式。
- 身份证号样式。
- 非 `mock-` commit hash。
- 禁止的真实输出路径。

手机号样式只触发 phone error，不应同时触发 commit hash error。

## 常见失败和修复

### 缺字段

修复：按 schema 补齐字段。

### quickLocator 不在 sourceQuote 中

修复：从 `sourceQuote` 中选择一段短文本作为 `quickLocator`。

### event 没证据

修复：新增 evidence item，或将事件移入 `excludedCandidates`。

### strong event 证据来源不足

修复：降低证据强度，或补充另一类 mock source。

### workDate 超出月份

修复：调整 `workDate`，或调整 package period。

### riskFlag 拼错

修复：使用白名单中的值。

### mock commit 没有 mock- 前缀

修复：改为 `mock-a1b2c3d` 这类明显虚构值。

### 出现手机号或疑似真实 hash

修复：删除该值，改用 mock 占位，并确认示例不是由真实材料改写。

## 边界提醒

Validator 不能：

- 判断法律胜算。
- 判断公司是否违法。
- 判断材料是否足以胜诉。
- 替代律师、仲裁委、法院或主管机关。
