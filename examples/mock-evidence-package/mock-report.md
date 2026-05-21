# Mock 加班证据报告：pkg-mock-2026-02

> mock-only 提醒：本报告由完全虚构的样例数据生成，只用于结构演示和本地验证，不提供法律意见。

## 摘要

- 期间：2026-02-01 至 2026-02-28
- 主体角色：技术岗位劳动者
- 纳入事件数：4
- 证据项数：11
- 排除候选数：3
- 质量门：needs_review: 2, pass: 2
- 证据强度：medium: 1, strong: 3

## 事件概览

| 事件ID | 类型 | 日期 | 时长 | 强度 | 质量门 | 风险 |
| --- | --- | --- | ---: | --- | --- | --- |
| evt-mock-weekday-001 | weekday_overtime | 2026-02-03 | 150 分钟 | strong | pass | 无 |
| evt-mock-weekday-002 | weekday_overtime | 2026-02-06 | 90 分钟 | medium | needs_review | single_source_only |
| evt-mock-release-001 | release_night | 2026-02-11 | 200 分钟 | strong | pass | 无 |
| evt-mock-rest-001 | rest_day_task | 2026-02-21 | 150 分钟 | strong | needs_review | manual_review_required |

## 证据索引预览

| 事件ID | 关联证据 |
| --- | --- |
| evt-mock-weekday-001 | evd-mock-chat-001 (wechat); evd-mock-git-001 (git); evd-mock-chat-002 (wechat) |
| evt-mock-weekday-002 | evd-mock-chat-003 (group_chat); evd-mock-chat-004 (group_chat) |
| evt-mock-release-001 | evd-mock-chat-005 (group_chat); evd-mock-git-002 (git); evd-mock-chat-006 (group_chat) |
| evt-mock-rest-001 | evd-mock-chat-007 (wechat); evd-mock-git-003 (git); evd-mock-chat-008 (wechat) |

## 纳入事件

### evt-mock-weekday-001

- 类型：weekday_overtime
- 日期：2026-02-03
- 时间：2026-02-03T19:00:00+08:00 至 2026-02-03T21:30:00+08:00
- 时长分钟：150
- 证据强度：strong
- 质量门：pass
- 风险标记：无
- 复核动作：复核 mock 时间线与多来源证据是否一致。
- 摘要：订单系统示例接口联调与 mock 验证结果整理。
- 证据：
  - evd-mock-chat-001: wechat, mock-wechat-export/messages.jsonl:1, 快速定位 `示例接口联调`
  - evd-mock-git-001: git, mock-git-log/git-log.json:1, 快速定位 `mock-a1b2c3d`
  - evd-mock-chat-002: wechat, mock-wechat-export/messages.jsonl:2, 快速定位 `mock 环境联调`

### evt-mock-weekday-002

- 类型：weekday_overtime
- 日期：2026-02-06
- 时间：2026-02-06T19:30:00+08:00 至 2026-02-06T21:00:00+08:00
- 时长分钟：90
- 证据强度：medium
- 质量门：needs_review
- 风险标记：single_source_only
- 复核动作：补充另一类 mock 来源，例如 Git、群聊或系统截图索引。
- 摘要：客服后台示例线上问题排查与 mock 告警恢复确认。
- 证据：
  - evd-mock-chat-003: group_chat, mock-wechat-export/messages.jsonl:3, 快速定位 `mock 工单列表`
  - evd-mock-chat-004: group_chat, mock-wechat-export/messages.jsonl:4, 快速定位 `示例告警数量`

### evt-mock-release-001

- 类型：release_night
- 日期：2026-02-11
- 时间：2026-02-11T20:00:00+08:00 至 2026-02-11T23:20:00+08:00
- 时长分钟：200
- 证据强度：strong
- 质量门：pass
- 风险标记：无
- 复核动作：复核 mock 时间线与多来源证据是否一致。
- 摘要：BI 报表服务 mock 发布夜观察与示例问题处理。
- 证据：
  - evd-mock-chat-005: group_chat, mock-wechat-export/messages.jsonl:5, 快速定位 `观察 mock 指标`
  - evd-mock-git-002: git, mock-git-log/git-log.json:3, 快速定位 `mock-d4e5f6g`
  - evd-mock-chat-006: group_chat, mock-wechat-export/messages.jsonl:6, 快速定位 `示例指标保持稳定`

### evt-mock-rest-001

- 类型：rest_day_task
- 日期：2026-02-21
- 时间：2026-02-21T10:00:00+08:00 至 2026-02-21T12:30:00+08:00
- 时长分钟：150
- 证据强度：strong
- 质量门：needs_review
- 风险标记：manual_review_required
- 复核动作：人工确认休息日任务来源和处理结果是否足够。
- 摘要：休息日 mock 数据修复任务与示例导入结果复核。
- 证据：
  - evd-mock-chat-007: wechat, mock-wechat-export/messages.jsonl:7, 快速定位 `mock 数据修复任务`
  - evd-mock-git-003: git, mock-git-log/git-log.json:4, 快速定位 `mock-r7s8t9u`
  - evd-mock-chat-008: wechat, mock-wechat-export/messages.jsonl:8, 快速定位 `示例导入结果`

## 排除候选

- cand-mock-daytime-001: 只有普通日间沟通，未进入加班时段。
- cand-mock-ack-only-001: 只有确认收到，没有任务处理过程和结果。
- cand-mock-short-001: 时长不足且证据来源单薄，暂不纳入。

## 复核提示

以下 mock events 在复用前需要人工复核：

- evt-mock-weekday-002: gate=needs_review, risks=single_source_only
- evt-mock-rest-001: gate=needs_review, risks=manual_review_required

本报告只用于结构预览，不是法律意见。

## 边界说明

- 仅使用 mock-only 数据。
- 不包含完整聊天原文、录音转写、源码、私有交付流程或法律结论。
- 不要在本仓库、issue、PR 或 discussion 中提交真实案件材料。
