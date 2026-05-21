# Changelog

## Unreleased

- 暂无未发布变更。

## v0.1.0 - planned

`v0.1.0` 计划作为 `overtime-evidence-kit` 的第一个公开 Release Candidate 基础。它适合 mock-only 结构评审和本地 demo，不包含真实证据处理能力。

### Added

- fictional mock evidence package，用于演示完整月份结构。
- public mock evidence package boundaries。
- JSON Schema files。
- validator：覆盖 schema、event timing、evidence coverage、mock-only boundaries。
- mock input adapter 和 package builder。
- rules engine：计算 `evidenceStrength`、`qualityGate`、`riskFlags`、`reviewAction`。
- Markdown mock report renderer。
- CSV evidence index renderer。
- `scripts/run_demo.py` 一条命令 demo。
- `scripts/check_all.py` 本地质量门。
- GitHub Actions CI。
- 贡献、安全、issue template、PR template、release checklist 和 public launch 文档。

### Changed

- 项目状态推进到 `v0.1.0 Release Candidate`。
- README 改为中文优先，强调 demo、`outputs/demo/`、质量门和 mock-only 边界。
- demo 文档改为中文优先，说明输出、清理方式和不读取真实文件。
- public launch 与 repository settings 文档改为中文优先。
- release readiness checks 覆盖 demo 文档和公开发布关键提醒。

### Security

- 继续拦截 phone-number-like values、ID-card-like values、real-commit-like hashes、forbidden private-material markers 和文本腐败标记。
- 贡献者必须确认不提交真实聊天、真实 Git、真实录音、真实身份、真实组织、真实地址、真实手机号、真实金额或任何可识别案件信息。
- issue、PR、discussion、commit、测试和文档都必须保持 mock-only。

### Known limitations

- 不处理真实案件材料。
- 不导入真实微信聊天、群聊、截图或导出记录。
- 不扫描真实 Git 仓库、源码、分支或 commit hash。
- 不处理真实录音、转写、会议纪要或用户本地文件。
- 不提供 SaaS、账号系统、上传工作流、paid pilot 材料或收费交付 SOP。
- 不提供法律意见、法律结论或结果承诺。
- GitHub Release 和 tag 仍然是单独的维护者决策，本阶段没有创建。
