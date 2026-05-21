# Repository Settings

本文档提供 GitHub repository settings 建议。它只是文档说明，不需要 API access，也不会修改远程仓库设置。

## Description

建议 GitHub description：

```text
Mock-only toolkit for structuring overtime evidence packages with schemas, validators, renderers, and release checks.
```

中文解释：该描述强调本项目是 mock-only，不暗示真实案件处理能力或法律服务。

## Topics

建议 topics：

```text
overtime
evidence-toolkit
mock-evidence
mock-data
json-schema
validation
documentation
python
open-source
```

避免使用会暗示法律意见、生产级真实证据处理或官方争议解决能力的 topics。

## Homepage

建议：保持为空，除非已经有稳定公开文档站点。

## Issues

建议：开启 issues，但必须保留现有 issue templates。

维护者应关闭或编辑包含真实证据、隐私数据、可识别案件信息的 issue。

## Discussions

建议：在明确 moderation 预期前保持关闭。

如果未来开启 discussions，应置顶 mock-only 警告，并禁止私有证据审查请求。

## Pull Requests

建议：允许公开 PR，但保留 PR template。

PR 必须确认：

- 只包含 fictional mock data。
- 不包含真实聊天、真实 Git、真实录音、真实身份、真实组织、真实地址、真实手机号、真实金额或真实案件细节。
- 不加入法律结论或结果承诺。

## Branch Protection

当协作者增加后，建议为 `master` 设置：

- 要求 CI 通过。
- 要求 review 后合并。
- 禁止 force push。
- 如需简单 release review，可优先保持线性历史。

## Security

建议：

- 开启 GitHub Security Advisories。
- 保持 `SECURITY.md` 可见。
- 要求报告者只使用 fictional mock reproduction steps。
- 不在公开或私下报告中索要真实证据。

## Releases and Tags

不要创建 GitHub Release 或 tag，除非维护者明确决定。

如果未来批准 release，请以 `CHANGELOG.md` 为 release notes 基础，并保留 known limitations。
