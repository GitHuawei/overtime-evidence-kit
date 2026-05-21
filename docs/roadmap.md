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

状态：进行中。

- LICENSE。
- CONTRIBUTING.md。
- SECURITY.md。
- 开源边界文档。
- README 项目状态、适用场景、隐私警告和快速开始。
- `.idea/` 忽略规则。

## Phase 2: 更稳健的交付包工具

计划方向：

- 更清晰的 validator 输出格式。
- 可选的 Markdown/CSV 公开交付包生成。
- 更多 mock 示例场景。
- 更严格的公开输出字段白名单。
- 文档中的人工复核清单增强。

## Phase 3: 可扩展集成

计划方向：

- 可插拔输入适配器接口。
- 更细粒度的风险标记。
- 更完整的 preflight 与 post-validate 流程。
- 示例级 CLI 命令封装。

## 永不纳入路线图

- 真实案件材料。
- 真实客户原始证据。
- 真实聊天、真实 Git、真实录音。
- 自动承诺法律结果。
- 替代律师或主管机关判断。
