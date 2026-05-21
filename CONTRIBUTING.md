# Contributing

感谢你考虑贡献 `overtime-evidence-kit`。

本仓库是 mock-only 开源项目。所有贡献都必须适合公开发布，不能包含真实案件材料、隐私信息或可识别真实案件的组合细节。

## 基本原则

- 只提交 fictional mock data。
- 不提交真实微信聊天、群聊、截图、导出记录或 message ID。
- 不提交真实 Git commit、仓库名、分支名、源码或 commit hash。
- 不提交真实录音、转写、会议纪要或文件名。
- 不提交真实公司名、人名、项目名、客户名、地址、手机号、合同、工资、金额或身份标识。
- 不提交从真实案件改写、脱敏或总结而来的示例。
- 不添加法律结论、结果承诺、真实服务流程、收费交付 SOP 或 paid pilot 材料。
- 修改 validator、renderer、schema、rules engine 或 demo 行为时，应补充测试。

## 开发流程

1. 从 `master` 创建聚焦的主题分支。
2. 一个 PR 只解决一个主题。
3. 同步更新相关文档和测试。
4. 本地运行质量门。
5. 在 PR 中确认 mock-only 检查结果。

## 本地验证

```powershell
python scripts/run_demo.py
python scripts/check_all.py
python -m unittest discover -s tests -p "test_*.py"
git diff --check
```

## 允许的 mock 示例

允许：

- `mock-*` 标识。
- 泛化角色，例如 `technical worker`、`reviewer`、`coordinator`。
- 明显虚构的系统名和场景。
- 结构真实但内容虚构的时间线。

禁止：

- 真实聊天原文或导出。
- 真实 commit hash、仓库名、分支名、源码或日志。
- 真实录音摘要或转写。
- 真实身份、公司、客户、项目、地址、手机号、金额、合同或工资。
- 可以反推出真实案件的日期、时间线或组合细节。

## Pull Request checklist

提交 PR 前确认：

- `python scripts/check_all.py` 通过。
- `python -m unittest discover -s tests -p "test_*.py"` 通过。
- `git diff --check` 通过。
- 只包含 fictional mock data。
- 文档没有承诺法律结果。
- 新增规则、renderer 行为或 demo 行为有测试覆盖。
- 没有提交 IDE 文件、本地缓存、临时输出或私有材料。

## 隐私边界问题

如果发现隐私或 mock-only 边界风险，请使用 privacy boundary issue template 报告，并只使用 fictional reproduction steps。不要粘贴真实证据。
