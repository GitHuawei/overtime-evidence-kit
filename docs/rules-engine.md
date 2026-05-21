# Rules engine

## 定位

Rules engine 用透明、可测试的 mock-only 规则计算证据质量字段。它不做法律判断，不判断胜诉概率，也不认定任何单位违法。

## 运行

```powershell
python scripts/evaluate_mock_package.py examples/mock-evidence-package/package.json
```

输出为更新后的 package JSON。

## evidenceStrength

### strong

满足：

- evidence item 数量不少于 2。
- sourceType 不少于 2 种。
- 至少有一条任务来源证据。
- 至少有一条结果或产出证据。

### medium

满足任一：

- evidence item 数量不少于 2，但 sourceType 只有 1 种。
- 有任务来源或结果描述，但缺少辅助来源。

### weak

满足任一：

- evidence item 数量只有 1。
- 缺少明确任务来源。
- 缺少结果或产出证据。
- 时间线无效。

## qualityGate

### pass

- `evidenceStrength == strong`
- 无高风险 flag。

### needs_review

- `evidenceStrength == medium`
- 或存在 `single_source_only`
- 或存在 `weak_result_evidence`
- 或存在 `manual_review_required`

### blocked

- `evidenceStrength == weak`
- 或存在 `missing_end_time`
- 或存在 `sensitive_content_present`

## riskFlags

允许值：

- `missing_end_time`
- `single_source_only`
- `unclear_task_owner`
- `sensitive_content_present`
- `needs_legal_review`
- `weak_result_evidence`
- `manual_review_required`

推导规则：

- sourceType 只有 1 种：`single_source_only`
- 无结果证据：`weak_result_evidence`
- 休息日任务：`manual_review_required`
- 发现敏感模式：`sensitive_content_present`
- 起止时间无效：`missing_end_time`

## reviewAction

规则引擎会根据风险生成基础复核动作，例如：

- 多来源 strong/pass：复核 mock 时间线与多来源证据是否一致。
- 单来源：补充另一类 mock 来源。
- 结果证据弱：补充处理结果或产出确认记录。
- 休息日：人工确认休息日任务来源和处理结果是否足够。
- 敏感内容：移除或泛化敏感内容后再公开。

## 边界

Rules engine 只做结构化质量提示。它不能：

- 判断法律胜算。
- 判断公司是否违法。
- 判断材料是否足以胜诉。
- 替代律师、仲裁委、法院或主管机关。
