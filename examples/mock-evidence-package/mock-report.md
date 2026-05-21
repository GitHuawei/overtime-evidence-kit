# Mock Evidence Report: pkg-mock-2026-02

> Mock-only notice: this report is generated from fictional sample data. It is for structure review and does not provide legal advice.

## Summary

- Period: 2026-02-01 to 2026-02-28
- Subject role: 技术岗位劳动者
- Included events: 4
- Evidence items: 11
- Excluded candidates: 3
- Quality gates: needs_review: 2, pass: 2
- Evidence strength: medium: 1, strong: 3

## Event Overview

| Event ID | Type | Work date | Duration | Strength | Gate | Risks |
| --- | --- | --- | ---: | --- | --- | --- |
| evt-mock-weekday-001 | weekday_overtime | 2026-02-03 | 150 min | strong | pass | none |
| evt-mock-weekday-002 | weekday_overtime | 2026-02-06 | 90 min | medium | needs_review | single_source_only |
| evt-mock-release-001 | release_night | 2026-02-11 | 200 min | strong | pass | none |
| evt-mock-rest-001 | rest_day_task | 2026-02-21 | 150 min | strong | needs_review | manual_review_required |

## Evidence Index Preview

| Event ID | Linked evidence |
| --- | --- |
| evt-mock-weekday-001 | evd-mock-chat-001 (wechat); evd-mock-git-001 (git); evd-mock-chat-002 (wechat) |
| evt-mock-weekday-002 | evd-mock-chat-003 (group_chat); evd-mock-chat-004 (group_chat) |
| evt-mock-release-001 | evd-mock-chat-005 (group_chat); evd-mock-git-002 (git); evd-mock-chat-006 (group_chat) |
| evt-mock-rest-001 | evd-mock-chat-007 (wechat); evd-mock-git-003 (git); evd-mock-chat-008 (wechat) |

## Included Events

### evt-mock-weekday-001

- Type: weekday_overtime
- Work date: 2026-02-03
- Time: 2026-02-03T19:00:00+08:00 to 2026-02-03T21:30:00+08:00
- Duration minutes: 150
- Evidence strength: strong
- Quality gate: pass
- Risk flags: none
- Review action: 复核 mock 时间线与多来源证据是否一致。
- Summary: 订单系统示例接口联调与 mock 验证结果整理。
- Evidence:
  - evd-mock-chat-001: wechat, mock-wechat-export/messages.jsonl:1, quickLocator `示例接口联调`
  - evd-mock-git-001: git, mock-git-log/git-log.json:1, quickLocator `mock-a1b2c3d`
  - evd-mock-chat-002: wechat, mock-wechat-export/messages.jsonl:2, quickLocator `mock 环境联调`

### evt-mock-weekday-002

- Type: weekday_overtime
- Work date: 2026-02-06
- Time: 2026-02-06T19:30:00+08:00 to 2026-02-06T21:00:00+08:00
- Duration minutes: 90
- Evidence strength: medium
- Quality gate: needs_review
- Risk flags: single_source_only
- Review action: 补充另一类 mock 来源，例如 Git、群聊或系统截图索引。
- Summary: 客服后台示例线上问题排查与 mock 告警恢复确认。
- Evidence:
  - evd-mock-chat-003: group_chat, mock-wechat-export/messages.jsonl:3, quickLocator `mock 工单列表`
  - evd-mock-chat-004: group_chat, mock-wechat-export/messages.jsonl:4, quickLocator `示例告警数量`

### evt-mock-release-001

- Type: release_night
- Work date: 2026-02-11
- Time: 2026-02-11T20:00:00+08:00 to 2026-02-11T23:20:00+08:00
- Duration minutes: 200
- Evidence strength: strong
- Quality gate: pass
- Risk flags: none
- Review action: 复核 mock 时间线与多来源证据是否一致。
- Summary: BI 报表服务 mock 发布夜观察与示例问题处理。
- Evidence:
  - evd-mock-chat-005: group_chat, mock-wechat-export/messages.jsonl:5, quickLocator `观察 mock 指标`
  - evd-mock-git-002: git, mock-git-log/git-log.json:3, quickLocator `mock-d4e5f6g`
  - evd-mock-chat-006: group_chat, mock-wechat-export/messages.jsonl:6, quickLocator `示例指标保持稳定`

### evt-mock-rest-001

- Type: rest_day_task
- Work date: 2026-02-21
- Time: 2026-02-21T10:00:00+08:00 to 2026-02-21T12:30:00+08:00
- Duration minutes: 150
- Evidence strength: strong
- Quality gate: needs_review
- Risk flags: manual_review_required
- Review action: 人工确认休息日任务来源和处理结果是否足够。
- Summary: 休息日 mock 数据修复任务与示例导入结果复核。
- Evidence:
  - evd-mock-chat-007: wechat, mock-wechat-export/messages.jsonl:7, quickLocator `mock 数据修复任务`
  - evd-mock-git-003: git, mock-git-log/git-log.json:4, quickLocator `mock-r7s8t9u`
  - evd-mock-chat-008: wechat, mock-wechat-export/messages.jsonl:8, quickLocator `示例导入结果`

## Excluded Candidates

- cand-mock-daytime-001: 只有普通日间沟通，未进入加班时段。
- cand-mock-ack-only-001: 只有确认收到，没有任务处理过程和结果。
- cand-mock-short-001: 时长不足且证据来源单薄，暂不纳入。

## Review Notes

The following mock events need human review before reuse:

- evt-mock-weekday-002: gate=needs_review, risks=single_source_only
- evt-mock-rest-001: gate=needs_review, risks=manual_review_required

This report is a structure preview only. It is not legal advice.

## Boundaries

- Uses mock-only data.
- Does not include full source quotes, chat transcripts, recordings, source code, private delivery details, or legal conclusions.
- Keep real case materials out of this repository, issues, pull requests, and discussions.
