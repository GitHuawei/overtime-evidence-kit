# overtime-evidence-kit

程序员加班证据整理 SOP 与工具包。

`overtime-evidence-kit` 用于演示如何把技术岗位常见的聊天、群聊、Git、发布夜和休息日任务线索，整理成可追溯、可复核、可脱敏的 mock 证据包。它提供通用 SOP、JSON Schema、完整 mock 月份、validator、公开报告 renderer、证据索引 renderer 和一键检查脚本。

## 项目状态

当前处于 Open Source Preview Milestone。项目可以用于阅读、运行 mock 示例和参与早期设计讨论，但仍不处理真实案件材料。

已经包含：

- 完整 mock 月份示例。
- JSON Schema 数据模型。
- Validator 和一键检查脚本。
- Markdown mock report 与 CSV evidence index renderer。
- GitHub Actions CI。
- 开源边界、贡献、安全和路线图文档。

尚未包含：

- SaaS 服务。
- 真实材料导入。
- 真实 Git 仓库扫描。
- 真实录音处理。
- 法律意见生成。
- 客户交付模板。

## 适用场景

适合用于：

- 学习技术岗位加班证据如何结构化。
- 用 mock 数据理解事件、证据项、报告和索引的关系。
- 在本地验证脱敏证据包结构是否满足基础规则。
- 讨论开源证据包字段设计、质量门禁和 mock-only 边界。

## 不适用场景

不适合用于：

- 上传真实聊天记录到公开仓库。
- 替代律师意见。
- 承诺协商、投诉、仲裁或诉讼结果。
- 自动认定任何单位违法。
- 处理未授权的他人隐私、客户数据、源码或商业秘密。
- 托管真实案件材料。

## 隐私警告

仓库内所有证据数据必须是 mock。不得提交、复制、迁移或粘贴以下内容：

- 真实微信聊天记录或群聊记录。
- 真实代码提交记录、仓库名、commit hash。
- 真实录音、录音文件名或录音转写。
- 真实公司名、人名、项目名、客户名、业务系统名。
- 真实金额、地址、手机号、身份证号、合同、工资流水。
- 任何可识别真实案件的信息或可反推真实案件事实的组合细节。

mock 示例也不能由真实材料改写而来。日期、角色、项目、金额和事件组合本身也可能构成可识别信息，因此示例必须从结构层面重新虚构。

## 快速开始

推荐先运行一键检查：

```powershell
python scripts/check_all.py
```

单独运行 validator：

```powershell
python scripts/validate_evidence_package.py examples/mock-evidence-package/package.json
```

渲染 mock 报告：

```powershell
python scripts/render_mock_report.py examples/mock-evidence-package/package.json
```

渲染证据索引：

```powershell
python scripts/render_evidence_index.py examples/mock-evidence-package/package.json
```

## Build package from mock inputs

从 mock source 重新构建 package：

```powershell
python scripts/build_mock_package.py
```

计算规则字段：

```powershell
python scripts/evaluate_mock_package.py examples/mock-evidence-package/package.json
```

端到端链路：

```powershell
python scripts/build_mock_package.py | Set-Content -LiteralPath tmp-package.json -Encoding utf8
python scripts/evaluate_mock_package.py tmp-package.json | Set-Content -LiteralPath tmp-evaluated-package.json -Encoding utf8
python scripts/validate_evidence_package.py tmp-evaluated-package.json
```

`tmp-package.json` 和 `tmp-evaluated-package.json` 是本地临时文件，不应提交。

## 完整 mock 月份示例

入口：

- [mock 月份 walkthrough](docs/mock-month-walkthrough.md)
- [mock package](examples/mock-evidence-package/package.json)
- [mock report](examples/mock-evidence-package/mock-report.md)
- [mock evidence index](examples/mock-evidence-package/mock-evidence-index.csv)

该示例只包含虚构数据，用于理解结构，不代表法律结论。

## 目录

```text
docs/       SOP、输入清单、证据包规格、隐私、边界、路线图和预览说明
schema/     JSON Schema 数据模型
examples/   mock 微信导出、mock Git 日志、mock 证据包和公开输出
scripts/    validator、renderer 和一键检查脚本
tests/      单元测试
```

## 核心流程

1. 准备并备份原始材料。
2. 先做隐私与敏感信息预处理。
3. 导入脱敏后的聊天、群聊、Git、录音目录索引。
4. 生成候选加班事件。
5. 分类为工作日延时、发布夜或休息日任务。
6. 评估证据强度、风险标记与复核动作。
7. 生成公开交付包。
8. 执行质量校验并交由用户复核。

## 文档

- [SOP](docs/SOP.md)
- [适用场景](docs/use-cases.md)
- [mock 月份 walkthrough](docs/mock-month-walkthrough.md)
- [证据包规格](docs/evidence-package-spec.md)
- [输入适配器](docs/input-adapters.md)
- [package builder](docs/package-builder.md)
- [rules engine](docs/rules-engine.md)
- [validator 规则](docs/validation-rules.md)
- [隐私与脱敏原则](docs/privacy-and-redaction.md)
- [服务边界](docs/service-boundary.md)
- [开源边界](docs/open-source-boundary.md)
- [路线图](docs/roadmap.md)
- [贡献指南](CONTRIBUTING.md)
- [安全政策](SECURITY.md)

## 许可证

本项目使用 MIT License。详见 [LICENSE](LICENSE)。
