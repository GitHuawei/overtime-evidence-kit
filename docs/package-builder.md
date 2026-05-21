# Package builder

## 命令

默认从仓库内 mock source 构建 package：

```powershell
python scripts/build_mock_package.py
```

指定输入：

```powershell
python scripts/build_mock_package.py `
  --messages examples/mock-wechat-export/messages.jsonl `
  --git-log examples/mock-git-log/git-log.json `
  --events examples/mock-event-drafts/events.json `
  --period-start 2026-02-01 `
  --period-end 2026-02-28 `
  --subject-role 技术岗位劳动者
```

## 输入文件

- `examples/mock-wechat-export/messages.jsonl`
- `examples/mock-git-log/git-log.json`
- `examples/mock-event-drafts/events.json`

## 输出

Builder 默认输出 package JSON 到 stdout，包含：

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

输出已经过 rules engine 计算基础质量字段。

## 验证输出

推荐运行：

```powershell
python scripts/check_all.py
```

如需手动检查临时文件：

```powershell
python scripts/build_mock_package.py | Set-Content -LiteralPath tmp-package.json -Encoding utf8
python scripts/validate_evidence_package.py tmp-package.json
python scripts/render_mock_report.py tmp-package.json
python scripts/render_evidence_index.py tmp-package.json
```

PowerShell 的原生 `>` 在部分环境中可能写出非 UTF-8 文件；建议使用 `Set-Content -Encoding utf8`。

## 常见失败

- mock Git commit 没有 `mock-` 前缀。
- `quickLocator` 不是 `content` 子串。
- event draft 缺少必填字段。
- JSONL 行不是 JSON object。
- 输入路径不存在。

## 边界

Builder 不读取真实微信、真实 Git 仓库、远程仓库或录音文件。它只处理仓库中的 mock source。
