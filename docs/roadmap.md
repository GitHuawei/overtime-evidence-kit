# 路线图

## Phase 0: MVP 骨架

状态：已完成。

- README、SOP、服务边界和隐私文档。
- 三类核心 schema：加班事件、证据项、证据包。
- mock 微信导出、mock Git 日志、mock 证据包。
- 基础 validator 与 mock report renderer。
- 单元测试。

## Phase 1: 校验增强

状态：已完成。

- GitHub Actions CI。
- JSON Schema 校验。
- 时间顺序校验。
- `durationMinutes` 与时间差一致性校验。
- 事件证据覆盖校验。
- `quickLocator` 子串校验。
- mock-only 敏感模式扫描。

## Open Source Readiness Phase

状态：已完成。

- LICENSE。
- CONTRIBUTING.md。
- SECURITY.md。
- 开源边界文档。
- README 项目状态、适用场景、隐私警告和快速开始。
- `.idea/` 忽略规则。

## Open Source Preview Milestone

状态：已完成。

- 完整 mock 月份案例。
- 一键检查脚本。
- CI 收敛到一键检查脚本。
- validator 输出和规则增强。
- mock 报告和证据索引输出增强。
- README 与文档补充完整案例说明。
- 关键规则测试覆盖。

## 后续方向

- 输入适配器设计，但只以 mock 或本地脱敏数据为示例。
- 更多完整 mock 场景。
- 公开输出字段白名单。
- 本地-only 脱敏流程设计。
- 人工复核清单增强。
- 更清晰的 validator 错误分组与修复建议。

## 永不纳入路线图

- 真实案件材料。
- 真实客户原始证据。
- 真实聊天、真实 Git、真实录音。
- 自动承诺法律结果。
- 替代律师、仲裁委、法院或主管机关判断。
