# 贡献指南

感谢你考虑贡献 `overtime-evidence-kit`。

## 基本原则

- 只提交 mock 数据。
- 不提交真实案件、真实聊天、真实 Git、真实录音、真实公司、人名、项目、金额、地址、手机号或任何可识别真实案件的信息。
- 文档应保持服务边界清晰：本项目做证据整理和材料结构化，不提供法律意见，不承诺结果。
- 新增 validator 行为必须补充测试。

## 开发流程

1. 从 `master` 创建主题分支。
2. 保持改动聚焦，一个 PR 解决一个主题。
3. 更新相关文档和测试。
4. 本地运行验证命令。
5. 提交 PR，并说明 mock-only 检查结果。

## 本地验证

```powershell
python scripts/validate_evidence_package.py examples/mock-evidence-package/package.json
python scripts/render_mock_report.py examples/mock-evidence-package/package.json
python -m unittest discover -s tests -p "test_*.py"
```

## Mock-only 要求

允许：

- `mock-*` 标识。
- 泛化角色，例如 `员工-A`、`主管-B`、`HR-C`。
- 泛化项目，例如 `订单系统`、`BI 报表服务`、`客服后台`。
- 结构真实但内容虚构的示例。

禁止：

- 真实聊天原文。
- 真实 commit hash 或仓库名。
- 真实录音摘要。
- 真实身份、公司、客户、项目、地址、手机号、金额。
- 可反推真实案件的日期和组合细节。

## 提交信息

建议使用清晰的 Conventional Commits 风格：

- `docs: update privacy boundary`
- `fix: tighten validator rule`
- `test: cover evidence coverage validation`
- `chore: update CI checks`

## Pull Request 清单

提交 PR 前请确认：

- 本地测试通过。
- 只包含 mock 数据。
- 文档没有承诺法律结果。
- 新增规则有测试覆盖。
- 没有提交 IDE、本地缓存或生成文件。
