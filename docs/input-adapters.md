# Input adapters

## 定位

Input adapter 把 mock source 转换成统一的 evidence package 输入。当前项目只支持 mock adapter，不支持真实微信、真实 Git、真实录音或远程仓库。

## 为什么只支持 mock

开源仓库不能接收真实案件材料。真实聊天、真实代码提交、真实录音、真实公司、人名、项目、地址、金额和手机号都可能构成隐私或可识别信息。

当前 adapter 只用于演示结构：

```text
mock source -> build_mock_package.py -> package JSON -> validator -> renderer
```

## mock messages 字段

`examples/mock-wechat-export/messages.jsonl` 每行一个 JSON object。

字段：

- `messageId`
- `sourceRowNum`
- `timestamp`
- `senderRole`
- `content`
- `eventId`
- `evidenceId`
- `sourceType`
- `quickLocator`
- `evidenceRole`
- `includeInPackage`
- `candidateId`
- `excludeReason`

规则：

- `includeInPackage: true` 生成 evidence item。
- `includeInPackage: false` 且有 `candidateId` 时生成 excluded candidate。
- `quickLocator` 必须是 `content` 的子串。
- `sourceRowNum` 应与 JSONL 行号一致。

## mock git log 字段

`examples/mock-git-log/git-log.json` 是 JSON array。

字段：

- `commit`
- `authorRole`
- `timestamp`
- `repository`
- `summary`
- `changedFiles`
- `eventId`
- `evidenceId`
- `quickLocator`
- `evidenceRole`
- `includeInPackage`

规则：

- `commit` 必须以 `mock-` 开头。
- `repository` 必须是 mock 仓库名。
- `changedFiles` 必须是 mock 路径。
- `includeInPackage: true` 才生成 Git evidence item。

## evidenceRole

允许值：

- `task_source`
- `work_process`
- `work_result`
- `git_output`
- `release_coordination`
- `review_note`

rules engine 使用 `evidenceRole` 推导证据强度、风险标记和复核动作。

## 未来扩展

未来可以增加更多 adapter，但只能以 mock 或本地脱敏数据为示例。任何真实输入适配器都不应出现在公开仓库中。
