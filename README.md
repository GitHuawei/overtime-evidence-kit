# overtime-evidence-kit

![CI](https://github.com/GitHuawei/overtime-evidence-kit/actions/workflows/ci.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

`overtime-evidence-kit` 是一个 **mock-only** 的加班证据包结构化演示工具。它用完全虚构的样例数据展示：如何把加班相关线索整理成可校验的 JSON package、Markdown report 和 CSV evidence index。

本仓库适合公开阅读、结构评审、本地 demo 和开源协作；**不处理真实案件材料**，不读取真实聊天、真实 Git、真实录音或任何可识别真实案件的信息。

## 当前状态

当前状态：**v0.1.0 Release Candidate**。

仓库已经包含：

- 完整的 fictional mock 月份样例。
- JSON Schema 数据结构。
- validator、rules engine、renderer。
- 一条命令 demo：`python scripts/run_demo.py`。
- 一键质量门：`python scripts/check_all.py`。
- GitHub Actions CI、issue template、PR template、贡献与安全文档。

## 这个项目能做什么

- 从仓库内 mock source 构建 mock evidence package。
- 为 mock events 计算 `evidenceStrength`、`qualityGate`、`riskFlags`、`reviewAction`。
- 校验 package schema、时间顺序、证据覆盖和 mock-only 边界。
- 生成公开可读的 `mock-report.md`。
- 生成便于人工扫描的 `mock-evidence-index.csv`。
- 在本地和 CI 中运行同一套质量门。

## 这个项目不能做什么

- 不导入真实微信聊天、群聊、截图或导出记录。
- 不扫描真实 Git 仓库、源码、分支或 commit hash。
- 不处理真实录音、转写、会议纪要或用户本地文件。
- 不提供 SaaS、账号系统、上传工作流或 paid pilot 材料。
- 不提供法律意见。
- 不承诺协商、仲裁、诉讼或执行结果。
- 不包含真实服务流程、私有交付细节或收费交付 SOP。

## mock-only 边界

所有证据数据必须是 fictional mock data。

不要在 issue、PR、discussion、commit、测试、文档或附件中提交、粘贴、迁移、改写或总结以下内容：

- 真实微信聊天、群聊、截图、导出记录或 message ID。
- 真实 Git commit、仓库名、分支名、源码或 commit hash。
- 真实录音、转写、会议纪要或文件名。
- 真实公司名、人名、项目名、客户名、地址、手机号、合同、工资、金额或身份标识。
- 任何能够识别真实案件、真实工作场所、真实客户、真实项目或真实个人的信息组合。

不要把真实材料“脱敏后”提交到本仓库。示例必须从结构层重新虚构。

## 快速开始

先运行完整质量门：

```powershell
python scripts/check_all.py
```

运行完整 mock demo：

```powershell
python scripts/run_demo.py
```

## demo 输出在哪里

默认输出目录：

```text
outputs/demo/
```

生成文件（面向人读的公开输出已经中文化，并使用中文展示标签）：

- `outputs/demo/package.json`
- `outputs/demo/mock-report.md`：中文 Markdown 摘要。
- `outputs/demo/mock-evidence-index.csv`：中文 CSV header 的证据索引。

`outputs/demo/` 已被 `.gitignore` 忽略，不应提交。

说明：`package.json` 仍保留 `eventType`、`qualityGate`、`riskFlags` 等机器字段和 `weekday_overtime`、`needs_review` 等机器值；`mock-report.md` 和 `mock-evidence-index.csv` 会显示中文标签，例如 `工作日加班`、`需复核`、`证据来源单一`、`群聊`、`Git 记录`。

自定义输出目录：

```powershell
python scripts/run_demo.py --output-dir tmp/demo-output
```

## 常用命令

校验 committed mock package：

```powershell
python scripts/validate_evidence_package.py examples/mock-evidence-package/package.json
```

渲染 Markdown report：

```powershell
python scripts/render_mock_report.py examples/mock-evidence-package/package.json
```

渲染 CSV evidence index：

```powershell
python scripts/render_evidence_index.py examples/mock-evidence-package/package.json
```

从 mock source 构建并评估 package：

```powershell
python scripts/build_mock_package.py
python scripts/evaluate_mock_package.py examples/mock-evidence-package/package.json
```

## 质量门

`python scripts/check_all.py` 会检查：

- UTF-8 和文本腐败标记。
- JSON / JSONL 解析。
- mock package build 和 rules evaluation。
- evidence package validation。
- renderer 是否可运行。
- committed sample output 是否与 renderer 一致。
- demo 是否能在临时目录完整跑通。
- release readiness 文件和 mock-only 关键提醒。
- unit tests。
- 敏感模式扫描。

GitHub Actions 运行同一条质量门。

## 示例输出

当前 mock 月份样例摘要：

- Included events: 4
- Evidence items: 11
- Excluded candidates: 3
- Quality gates: `pass: 2`, `needs_review: 2`
- Evidence strength: `strong: 3`, `medium: 1`

公开输出：

- [Mock report](examples/mock-evidence-package/mock-report.md)
- [Evidence index CSV](examples/mock-evidence-package/mock-evidence-index.csv)

公开输出已经中文化，并把机器枚举值渲染为中文展示标签，便于人工阅读。它只展示结构化摘要、证据定位、质量门、风险提示和复核建议，不输出完整聊天原文、录音转写、源码、私有流程或法律结论。

## 目录结构

```text
.github/    CI、issue template、PR template
docs/       SOP、边界、demo、公开发布、release checklist、roadmap 等文档
examples/   mock source、mock package、mock report、mock evidence index
schema/     JSON Schema
scripts/    validator、renderer、builder、rules engine、run_demo、check_all
tests/      unit tests
```

## 文档

- [Demo guide](docs/demo.md)
- [Mock month walkthrough](docs/mock-month-walkthrough.md)
- [Public outputs](docs/public-outputs.md)
- [Validation rules](docs/validation-rules.md)
- [Evidence package spec](docs/evidence-package-spec.md)
- [Input adapters](docs/input-adapters.md)
- [Package builder](docs/package-builder.md)
- [Rules engine](docs/rules-engine.md)
- [Privacy and redaction](docs/privacy-and-redaction.md)
- [Service boundary](docs/service-boundary.md)
- [Open-source boundary](docs/open-source-boundary.md)
- [Public launch notes](docs/public-launch.md)
- [Repository settings](docs/repository-settings.md)
- [Release checklist](docs/release-checklist.md)
- [Roadmap](docs/roadmap.md)
- [Contributing](CONTRIBUTING.md)
- [Security policy](SECURITY.md)
- [Changelog](CHANGELOG.md)

## 贡献

欢迎贡献 schema、validator、renderer、文档和测试改进，但必须遵守 mock-only 边界。

提交前运行：

```powershell
python scripts/check_all.py
python -m unittest discover -s tests -p "test_*.py"
git diff --check
```

不要在公开仓库中提交真实证据、私有材料或任何可识别真实案件的信息。

## License

本项目使用 MIT License。详见 [LICENSE](LICENSE)。
