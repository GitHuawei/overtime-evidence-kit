# overtime-evidence-kit

程序员加班证据整理 SOP 与工具包。

本项目用于把聊天、群聊、Git、发布夜、线上问题处理等常见技术岗位证据形态，整理成可追溯、可复核、可脱敏的材料包。它提供通用 SOP、数据模型、mock 样例、基础校验器和基础报告渲染脚本。

## 不是什么

- 不是法律服务。
- 不替代律师意见。
- 不承诺仲裁、诉讼、协商或投诉结果。
- 不自动认定任何单位违法。
- 不保存、发布或迁移真实案件材料。

## 隐私与 mock 原则

仓库内所有证据数据必须是 mock。不得放入真实微信聊天记录、微信群聊记录、代码提交记录、录音、公司名、人名、项目名、金额、地址、手机号、身份证号、合同、工资流水或任何可识别真实案件的信息。

mock 数据应满足：

- 结构接近真实工作流，内容完全虚构。
- commit hash 使用 `mock-` 前缀，例如 `mock-a1b2c3d`。
- 公司、人员、项目、系统名称使用泛化名称，例如 `示例科技有限公司`、`员工-A`、`主管-B`、`订单系统`。
- 聊天内容只表达证据结构，不复用真实原句。

## 目录

```text
docs/       SOP、输入清单、证据包规格、隐私与服务边界
schema/     JSON Schema 数据模型
examples/   mock 微信导出、mock Git 日志、mock 证据包
scripts/    校验器与 mock 报告渲染脚本
tests/      校验器测试
```

## 快速验证

```powershell
python scripts/validate_evidence_package.py examples/mock-evidence-package/package.json
python scripts/render_mock_report.py examples/mock-evidence-package/package.json
python -m unittest discover -s tests -p "test_*.py"
```

## 基本流程

1. 准备并备份原始材料。
2. 先做隐私与敏感信息预处理。
3. 导入脱敏后的聊天、群聊、Git、录音目录索引。
4. 生成候选加班事件。
5. 分类为工作日延时、发布夜或休息日任务。
6. 评估证据强度、风险标记与复核动作。
7. 生成公开交付包。
8. 执行质量校验并交由用户复核。
