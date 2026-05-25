# Public Launch Notes

本文档用于准备 `overtime-evidence-kit` 的受控公开发布。它只是公开安全的发布准备说明，不会创建 GitHub Release，也不会创建 tag。

## 发布准备摘要

当前状态：`v0.1.0` 已发布。

本次公开发布收尾的目标 tag：`v0.2.0-public-preview`。它是 public preview release，不改变 mock-only 边界，不新增真实 adapter，不处理真实案件材料。

可以公开展示：

- mock-only evidence package 结构。
- JSON Schema validation。
- local validator。
- mock input builder。
- rules engine。
- Markdown report renderer。
- CSV evidence index renderer。
- Excel-friendly UTF-8 with BOM CSV output。
- 中文 README、FAQ、positioning、customer safety 和 service overview。
- CI-backed quality gate。
- 贡献、安全、issue template、PR template 和 release checklist。

不包含：

- 真实微信导入。
- 真实 Git 扫描。
- 真实录音或转写处理。
- SaaS、账号或上传工作流。
- 客户交付流程、paid pilot 材料或收费 SOP。
- 法律意见、法律结论或结果承诺。

## 公开前检查

公开或对外介绍前确认：

- 已运行 `python scripts/check_all.py`。
- 已运行 `python -m unittest discover -s tests -p "test_*.py"`。
- 已运行 `git diff --check`。
- `docs/plans/` 未暂存、未提交。
- README 首屏清楚说明 mock-only。
- `docs/demo.md` 说明 `python scripts/run_demo.py` 和 `outputs/demo/`。
- `docs/faq.md`、`docs/positioning.md`、`docs/customer-safety.md`、`docs/service-overview.md` 已更新，并保持公开安全。
- `CHANGELOG.md` 包含 known limitations。
- issue template 和 PR template 提醒不要提交真实证据。
- `v0.1.0` tag 和 GitHub Release 已创建。后续不要创建新的 tag 或 release，除非维护者另行明确批准；本次 `v0.2.0-public-preview` 属于维护者已批准的公开预览发布动作。

## GitHub description 建议

```text
Mock-only toolkit for structuring overtime evidence packages with schemas, validators, renderers, and release checks.
```

中文解释：这是一个 mock-only 工具包，用于演示加班证据包如何结构化、校验和渲染，不处理真实材料。

## 公开介绍文案

```text
overtime-evidence-kit 是一个 mock-only 开源工具包，用完全虚构的 mock 数据演示如何把加班线索整理成可校验、可复核、可展示的证据包。它包含虚构样例数据、JSON Schema、validator、rules engine、Markdown report renderer、Excel-friendly CSV evidence index renderer 和 release checks。它不处理真实证据，也不提供法律意见。
```

## 不要公开承诺的内容

不要声称本项目：

- 能处理真实案件。
- 能导入真实聊天、Git 仓库、录音或转写。
- 能生成法律结论。
- 能预测协商、仲裁、诉讼或执行结果。
- 提供 paid pilot、客户交付流程或私有服务 SOP。
- 接受在 issue、PR、discussion 或附件中提交私有证据。
- 在公开仓库中审查真实材料、报价或承诺服务结果。

## post-launch monitoring checklist

公开后关注：

- 新 issue 是否包含真实证据或隐私信息。
- PR 是否引入真实聊天、真实 Git、真实录音或可识别案件信息。
- CI 是否在 `master` 上保持通过。
- README 是否让用户误以为可以提交真实材料。
- FAQ、customer safety 和 service overview 是否继续阻止用户公开上传真实材料。
- issue template 和 PR template 是否足够清楚。
- GitHub Release 和 tag 是否仍作为单独维护者决策处理。
