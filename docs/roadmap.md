# Roadmap

`overtime-evidence-kit` 的公开路线图围绕一个原则展开：只用完全虚构的 mock 数据演示证据结构化方法，不在公开仓库处理真实案件材料。

## 当前状态

当前公开版本：`v0.1.0`。

已经具备的能力：

- 一条命令运行 mock demo：`python scripts/run_demo.py`。
- 从 committed mock source 构建 mock evidence package。
- 运行 rules engine，生成 `evidenceStrength`、`qualityGate`、`riskFlags` 和 `reviewAction`。
- 使用 JSON Schema 和 validator 校验证据包结构、时间顺序、证据覆盖和 mock-only 边界。
- 渲染中文 Markdown report。
- 渲染中文 CSV evidence index，并使用 Excel-friendly UTF-8 with BOM。
- 运行 `python scripts/check_all.py` 做本地质量门。
- 使用 GitHub Actions 对齐本地质量门。

## v0.1.0 发布后校准

- README 和 roadmap 反映正式 `v0.1.0` 状态。
- FAQ、positioning、customer safety、service overview 和 business boundary 保持公开安全。
- issue templates 和 PR template 继续阻止真实材料进入公开渠道。
- `docs/plans/`、`outputs/demo/` 和 release notes 临时文件不提交。
- 公开输出必须能重新生成，并通过 UTF-8、文本腐败、敏感模式、CSV BOM 和 demo 检查。

## 近期可能方向

- 改进 validator error grouping，让修复建议更容易理解。
- 增加更多完全虚构的 mock scenarios，用于覆盖不同证据来源组合。
- 增强 CLI 体验，例如更清晰的 summary 和失败定位。
- 为 rules engine 增加可配置阈值，但仍只面向 mock package。
- 完善 local-only redaction workflow design 文档，但不接入真实数据。

## 服务咨询相关方向

公开仓库可以说明“证据结构化整理协助/咨询”的安全边界，但不能接收真实材料，也不能公开私有交付流程。

可公开讨论：

- 如何理解 evidence package 结构。
- 如何用 mock 数据复现结构问题。
- 如何区分机器字段和人读输出。
- 如何在不暴露真实材料的前提下提出需求。

不可公开讨论：

- 真实聊天、真实 Git、真实录音、真实身份、真实金额、真实合同或真实案件细节。
- 私有服务 SOP、定价细节、客户材料处理细节。
- 法律意见、法律结论、胜率判断或结果承诺。

## 永久不纳入公开仓库范围

- 真实案件材料。
- 真实客户原始证据。
- 真实微信、真实 Git、真实录音导入。
- 扫描用户真实本地文件或真实仓库。
- 自动法律结论。
- 替代律师、仲裁员、法院、监管机构或专业判断。
- 付费服务交付 SOP、真实客户材料、报价细节或 paid pilot 材料。
