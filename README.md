# overtime-evidence-kit

程序员加班证据整理 SOP 与工具包。

`overtime-evidence-kit` 面向技术岗位劳动者的证据整理场景，提供通用 SOP、证据包数据模型、mock 示例、基础校验器和 mock 报告渲染脚本。项目目标是帮助用户把分散材料整理成可追溯、可复核、可脱敏的材料包，再由用户决定是否咨询律师、协商、投诉或仲裁。

## 项目状态

当前处于 Open Source Readiness Phase。

已经包含：

- SOP 与证据包规格文档。
- mock 微信导出、mock Git 日志、mock 证据包示例。
- JSON Schema 数据模型。
- 本地 validator 与 mock report renderer。
- GitHub Actions CI。
- 贡献、安全、开源边界和路线图文档。

尚未包含：

- SaaS 服务。
- 真实案件导入。
- 完整法律文书生成。
- 面向真实客户的交付流程。

## 适用场景

适合用于：

- 学习如何组织技术岗位加班证据材料。
- 基于 mock 数据理解证据项、事件和证据包之间的关系。
- 在本地验证脱敏证据包结构是否满足基础规则。
- 为开源工具、内部流程或教学材料提供安全的参考骨架。

## 不适用场景

不适合用于：

- 替代律师意见。
- 承诺仲裁、诉讼、协商或投诉结果。
- 自动认定任何单位违法。
- 处理未脱敏真实聊天、真实 Git、真实录音、真实合同或真实工资流水。
- 公开托管任何真实案件材料。

## 隐私警告

仓库内所有证据数据必须是 mock。不得提交、复制、迁移或粘贴以下内容：

- 真实微信聊天记录或群聊记录。
- 真实代码提交记录、仓库名、commit hash。
- 真实录音、录音文件名或录音转写。
- 真实公司名、人名、项目名、客户名、业务系统名。
- 真实金额、地址、手机号、身份证号、合同、工资流水。
- 任何可识别真实案件的信息或可反推真实案件事实的组合细节。

mock 数据应满足：

- 结构接近真实工作流，内容完全虚构。
- commit hash 使用 `mock-` 前缀，例如 `mock-a1b2c3d`。
- 人员、公司、项目和系统名称使用泛化名称。
- 聊天内容只表达证据结构，不复用真实原句。

## 快速开始

运行 mock 证据包校验：

```powershell
python scripts/validate_evidence_package.py examples/mock-evidence-package/package.json
```

渲染 mock 报告：

```powershell
python scripts/render_mock_report.py examples/mock-evidence-package/package.json
```

运行单元测试：

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

## 目录

```text
docs/       SOP、输入清单、证据包规格、隐私、边界、路线图
schema/     JSON Schema 数据模型
examples/   mock 微信导出、mock Git 日志、mock 证据包
scripts/    校验器与 mock 报告渲染脚本
tests/      validator 单元测试
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
- [证据包规格](docs/evidence-package-spec.md)
- [隐私与脱敏原则](docs/privacy-and-redaction.md)
- [服务边界](docs/service-boundary.md)
- [开源边界](docs/open-source-boundary.md)
- [路线图](docs/roadmap.md)
- [贡献指南](CONTRIBUTING.md)
- [安全政策](SECURITY.md)

## 许可证

本项目使用 MIT License。详见 [LICENSE](LICENSE)。
