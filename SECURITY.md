# Security Policy

## 支持范围

当前支持范围是 `master` 分支上的 `v0.1.0 Release Candidate`。

安全和隐私边界问题包括：

- 脚本、文档、测试或模板可能允许真实隐私信息进入仓库。
- validator 或质量门漏掉明显敏感模式。
- public output renderer 输出原始材料，而不是安全摘要。
- CI 与 `python scripts/check_all.py` 行为不一致。

## 不要公开提交敏感信息

不要在 issue、PR、discussion、commit、comment、附件或截图中包含真实案件材料。

永远不要提交：

- 真实微信聊天、群聊、截图、导出记录或 message ID。
- 真实 Git commit、仓库名、分支名、源码或 commit hash。
- 真实录音、转写、会议纪要或文件名。
- 真实公司名、人名、项目名、客户名、地址、手机号、合同、工资、金额或身份标识。
- 任何能够识别真实工作场所、争议、客户、项目或个人的信息组合。

请使用 fictional mock data 和 `mock-*` 标识描述问题。

## 报告方式

如发现安全或隐私边界问题，请通过 GitHub Security Advisories 或其他私下渠道报告。报告也必须保持 mock-only。

建议包含：

- 受影响文件或行为。
- fictional reproduction steps。
- 期望行为。
- 实际行为。
- 为什么它会造成隐私或 release readiness 风险。

不要附加真实证据或私有材料。

## 处理原则

- 隐私边界修复优先。
- 修复应尽量包含测试或质量门覆盖。
- public outputs 必须保持摘要和索引形式，不输出原始证据。
- 本项目不提供法律意见，不承诺法律结果。

## 服务咨询安全提醒

如果你希望咨询自己的材料，不要通过 GitHub issue、PR、discussion、commit、附件或截图发送真实证据。先确认授权范围、材料最小化、存储方式、保留和删除规则，以及是否需要律师或其他专业人士参与。
