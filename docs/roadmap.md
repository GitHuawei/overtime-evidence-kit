# Roadmap

## 已完成

### Phase 0: MVP Skeleton

- README、SOP、service boundary、privacy 文档。
- event、evidence item、evidence package 的核心 schema。
- mock source 和 mock evidence package。
- 基础 validator 和 mock report renderer。
- 单元测试。

### Phase 1: Validation Enhancements

- GitHub Actions CI。
- JSON Schema validation。
- 时间顺序校验。
- `durationMinutes` 一致性检查。
- event evidence coverage validation。
- `quickLocator` 子串校验。
- mock-only sensitive pattern scanning。

### Open Source Readiness

- `LICENSE`。
- `CONTRIBUTING.md`。
- `SECURITY.md`。
- open-source boundary 文档。
- README 隐私提醒、快速开始和项目范围。
- `.idea/` ignore rule。

### Open Source Preview

- 完整 mock 月份 walkthrough。
- 一键质量门。
- CI 对齐 `scripts/check_all.py`。
- validator 输出和规则增强。
- mock report 和 evidence index 输出增强。
- public outputs 文档。
- 关键验证和渲染行为测试。

### Phase A: Input Adapter MVP

- mock source adapter fields。
- `scripts/build_mock_package.py`。
- `docs/input-adapters.md`。
- `docs/package-builder.md`。
- build -> validate -> render workflow。

### Phase B: Rules Engine MVP

- `scripts/rules_engine.py`。
- `scripts/evaluate_mock_package.py`。
- `docs/rules-engine.md`。
- 自动计算 `evidenceStrength`、`qualityGate`、`riskFlags`、`reviewAction`。

### Phase C: Public Output Polish

- GitHub-readable mock report structure。
- stable public evidence index fields。
- renderer consistency checks。
- public outputs 阅读说明。

### Phase D: Open Source Release Candidate

- README 状态更新为 `v0.1.0 Release Candidate`。
- `CHANGELOG.md`。
- release checklist。
- GitHub issue templates。
- Pull request template。
- 更强的 contribution、security、open-source boundary 文案。
- `scripts/check_all.py` release readiness audit。

### Phase E: Public Launch Prep

- README 首屏发布准备文案。
- `CHANGELOG.md` Known limitations。
- public release checklist 更新。
- public launch notes。
- repository settings 建议。
- launch readiness checks。

### Phase F: Demo Experience

- `scripts/run_demo.py` 一条命令 demo。
- 默认输出到 `outputs/demo/`。
- demo 输出被 `.gitignore` 忽略。
- demo 文档和测试。
- `scripts/check_all.py` 在临时目录运行 demo。

### Phase G: Chinese Localization and Demo Clarity

- README 中文优先。
- demo、public launch、repository settings、release checklist 中文优先。
- CHANGELOG、CONTRIBUTING、SECURITY 中文可读。
- release readiness 文案检查同步为中文优先。
- 外部文本腐败扫描纳入验证。

## 后续方向

- 更严格的 mock input adapter validation。
- 可配置 rules-engine thresholds。
- local-only redaction workflow design。
- 更好的 CLI UX。
- 更多 fictional mock scenarios。
- 更清晰的 validator error grouping 和 remediation messages。

## 永久不纳入范围

- 真实案件材料。
- 真实客户原始证据。
- 真实微信、真实 Git、真实录音导入。
- 自动法律结论。
- 替代律师、仲裁员、法院、监管机构或专业判断。
