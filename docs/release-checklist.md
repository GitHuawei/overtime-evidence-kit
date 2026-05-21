# Release Checklist

本清单用于把 `overtime-evidence-kit` 准备到可以受控公开的 `v0.1.0 Release Candidate` 状态。它不会创建 GitHub Release，不会创建 tag，也不会发布 package。

## 公开决策

公开仓库或对外介绍前确认：

- 仓库可见性变更是明确决策。
- README 首屏说明项目是 mock-only。
- README 说明如何运行 `python scripts/run_demo.py`。
- README 说明 `outputs/demo/` 生成什么。
- README 说明不处理真实案件材料。
- `CHANGELOG.md` 包含 Known limitations。
- `docs/public-launch.md` 和 `docs/repository-settings.md` 已更新。
- 未创建 GitHub Release 或 tag，除非维护者另行明确批准。

## 本地检查

运行：

```powershell
python scripts/run_demo.py
python scripts/check_all.py
python -m unittest discover -s tests -p "test_*.py"
git diff --check
git status -sb
git tag --list
```

期望结果：

- 所有检查通过。
- `docs/plans/` 未暂存、未提交。
- `outputs/demo/` 被忽略，未暂存。
- 没有本地临时文件被暂存。
- `git tag --list` 为空，除非维护者已明确批准创建 tag。

## 内容审计

确认：

- README 状态为 `v0.1.0 Release Candidate`。
- README 解释能做什么和不能做什么。
- README 链接 demo、公开输出和质量门。
- 文档不承诺法律结果。
- examples 全部是 fictional mock data。
- tests 不包含真实数据。
- scripts 不依赖私有本地路径。
- CI 调用 `python scripts/check_all.py`。
- issue template 和 PR template 存在，并提醒不要提交真实材料。

## 敏感信息审计

确认仓库不包含：

- 真实微信聊天或群聊。
- 真实 Git commit、仓库名、分支名、源码或 commit hash。
- 真实录音或转写。
- 真实人名。
- 真实公司名。
- 真实项目名。
- 真实客户名。
- 真实地址。
- 真实手机号。
- 真实金额、工资、合同或身份标识。
- 任何能够识别真实案件的信息组合。

## GitHub repository settings

公开前建议：

- repository description 强调 mock-only evidence package tooling。
- topics 不暗示法律意见或真实证据处理。
- homepage 为空，除非已有稳定公开文档站点。
- issues 仅在 issue templates 可见时开启。
- discussions 在 moderation 预期明确前保持关闭。
- 安全公告功能开启。
- PR template 可见。
- Actions badge 指向当前 CI workflow。

## tag / GitHub Release 决策

以下命令只是说明，不要自动执行：

```powershell
git tag -a v0.1.0 -m "v0.1.0 release candidate"
git push origin v0.1.0
```

不要创建 GitHub Release 或 tag，除非维护者明确要求。

如果未来批准 release：

- 以 `CHANGELOG.md` 为 release notes 基础。
- 保留 Known limitations。
- 不提真实案例、客户工作、私有交付流程、定价或法律结果。
- release title 不应暗示支持生产级真实证据处理。

## 最终边界检查

公开前再次确认：

- 仓库、issue、PR、discussion、截图和附件中没有真实证据。
- 所有示例都使用 mock-only data。
- 项目没有声称提供法律意见。
- public outputs 仍然是摘要和索引，不是原始证据 dump。
