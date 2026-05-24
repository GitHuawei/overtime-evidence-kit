# Public-safe Method Overview

本文档只说明 `overtime-evidence-kit` 在公开仓库中展示的高层方法。它不是客户交付 SOP，不是收费服务流程，不包含真实材料处理步骤，也不提供法律意见。

## 目标

用完全虚构的 mock 数据演示：如何把加班线索整理为结构化、可追踪、可复核、可展示的 evidence package、Markdown report 和 Excel-friendly CSV evidence index。

## 高层流程

1. 使用仓库内 committed mock source。
2. 构建 mock evidence package。
3. 运行 rules engine，为 mock events 生成 `evidenceStrength`、`qualityGate`、`riskFlags` 和 `reviewAction`。
4. 运行 validator，检查 schema、时间顺序、证据覆盖和 mock-only 边界。
5. 渲染中文 Markdown report。
6. 渲染中文 CSV evidence index。
7. 运行 `python scripts/check_all.py` 作为质量门。

## 公开输出原则

- 只展示摘要、索引、质量门、风险提示和复核建议。
- 不输出真实原始材料。
- 不输出完整聊天、录音转写、源码或客户数据。
- 不把真实材料脱敏后放入示例。
- 不写法律结论、胜率判断或结果承诺。

## mock-only 边界

公开仓库不接收、不读取、不处理真实微信、真实 Git、真实录音、真实公司、人名、项目、金额、地址、手机号、合同、工资或任何可识别真实案件的信息。

如果需要讨论真实材料相关的咨询边界，请先阅读 `docs/customer-safety.md` 和 `docs/service-overview.md`，不要通过公开 GitHub 渠道提交材料。
