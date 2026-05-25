# v0.2.0-public-preview

## Release title

`v0.2.0-public-preview - Mock-only overtime evidence demo`

## 简短定位

这是 `overtime-evidence-kit` 的 public preview release。它用完全虚构的 mock 数据演示如何把加班线索整理成可校验、可复核、可展示的 evidence package、中文 Markdown report 和 Excel-friendly CSV evidence index。

## What's included

- 一条命令运行 mock demo：`python scripts/run_demo.py`
- 中文 public report：`outputs/demo/mock-report.md`
- 中文 CSV evidence index：`outputs/demo/mock-evidence-index.csv`
- CSV 使用 Excel-friendly UTF-8 with BOM。
- JSON Schema、validator、rules engine 和 renderer。
- 一键质量门：`python scripts/check_all.py`
- FAQ、customer safety、service overview、public outputs 和 release checklist。

## Quick start

```powershell
python scripts/run_demo.py
python scripts/check_all.py
```

生成文件：

```text
outputs/demo/package.json
outputs/demo/mock-report.md
outputs/demo/mock-evidence-index.csv
```

## Mock-only boundary

本仓库不处理真实案件材料。不要在 GitHub issue、PR、discussion、commit、截图或附件中提交真实微信、真实 Git、真实录音、真实公司、人名、项目、金额、地址、手机号、合同、工资或任何可识别真实案件的信息。

所有示例都必须是 fictional mock data。不要把真实材料“脱敏后”放入本仓库。

## Not included

- 不导入真实微信。
- 不扫描真实 Git 仓库。
- 不读取用户真实文件。
- 不处理真实录音、合同、工资或身份材料。
- 不提供法律意见、法律结论或结果承诺。
- 不承诺协商、仲裁、诉讼或执行结果。
- 不包含私有服务 SOP、报价或 paid pilot 材料。

## Validation

本版本发布前应通过：

```powershell
python scripts/run_demo.py
python scripts/check_all.py
python -m unittest discover -s tests -p "test_*.py"
git diff --check
```

## Safety note

公开渠道只适合讨论 mock-only reproduction、schema、validator、renderer 和文档改进。不要在 GitHub issue、PR 或 discussion 中粘贴真实材料。如果你想讨论自己的材料，请先阅读 `docs/customer-safety.md` 和 `docs/service-overview.md`，并且不要通过公开渠道发送原始证据。
