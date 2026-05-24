# Changelog

## Unreleased

- 暂无未发布变更。

## v0.1.0 - planned

`v0.1.0` 计划作为 `overtime-evidence-kit` 的首个受控公开版本。它面向中文用户展示一条完整的 mock-only 证据包链路：用完全虚构的 mock 数据演示如何把加班线索整理成可校验、可复核、可展示的证据包。

### Launch-ready updates

- README 首屏更新为中文发布页，突出项目价值、mock-only 边界、一条命令 demo、质量门和服务咨询安全入口。
- 新增 `docs/faq.md`，回答真实用户常见问题：是否能处理真实微信、为什么 mock-only、是否法律意见、如何安全咨询。
- 新增 `docs/positioning.md`，解释为什么加班证据需要结构化、可追踪、可复核。
- 新增 `docs/service-overview.md`，公开安全地说明可能提供的证据结构化整理协助边界。
- 新增 `docs/customer-safety.md`，提醒用户不要在公开渠道上传真实聊天、Git、录音、身份、金额、合同或其他隐私材料。
- 更新公开路线图、release checklist、repository settings、demo 文档和 public outputs 文档，使其与正式公开准备一致。
- 强化 GitHub issue templates 和 PR template，继续禁止真实材料进入 issue、PR、discussion、commit 或附件。

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
- release readiness checks 覆盖 FAQ、positioning、service overview、customer safety、README 价值主张、CSV BOM、demo、mock-only 边界和公开发布关键提醒。
- 公开 Markdown report 和 CSV evidence index 使用中文展示标签，JSON package 继续保留机器字段和机器枚举值。
- CSV evidence index 使用 Excel-friendly UTF-8 with BOM，便于 Windows Excel 直接打开中文不乱码。

### Security

- 继续拦截 phone-number-like values、ID-card-like values、real-commit-like hashes、forbidden private-material markers 和文本腐败标记。
- 贡献者必须确认不提交真实聊天、真实 Git、真实录音、真实身份、真实组织、真实地址、真实手机号、真实金额或任何可识别案件信息。
- issue、PR、discussion、commit、测试和文档都必须保持 mock-only。
- 公开服务咨询说明只描述安全边界，不接收真实材料，不写私有交付 SOP，不承诺法律结果。

### Known limitations

- 不处理真实案件材料。
- 不导入真实微信聊天、群聊、截图或导出记录。
- 不扫描真实 Git 仓库、源码、分支或 commit hash。
- 不处理真实录音、转写、会议纪要或用户本地文件。
- 不提供 SaaS、账号系统、上传工作流、paid pilot 材料或收费交付 SOP。
- 不提供法律意见、法律结论或结果承诺。
- 不在公开仓库接收真实证据审查请求。
- GitHub Release 和 tag 仍然是单独的维护者决策，本阶段没有创建。
