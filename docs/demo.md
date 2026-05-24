# Demo Guide

`scripts/run_demo.py` 提供一条命令的完整 mock demo。它只使用仓库内已经提交的 fictional mock source，不读取用户真实文件，不扫描真实 Git 仓库，不处理真实聊天或录音。

## 一条命令运行 demo

```powershell
python scripts/run_demo.py
```

运行后终端会打印简洁 summary，包含输出目录、生成文件、included events 数量、evidence items 数量，以及 mock-only 边界提醒。

## demo 做什么

demo 会按顺序执行：

1. 从 committed mock source 构建 mock evidence package。
2. 用 rules engine 评估 mock events。
3. 校验 evaluated package。
4. 渲染 Markdown report。
5. 渲染 CSV evidence index。
6. 打印输出路径和摘要。

## 生成文件

默认输出目录：

```text
outputs/demo/
```

生成文件（公开人读输出已中文化，并使用中文展示标签）：

- `outputs/demo/package.json`
- `outputs/demo/mock-report.md`：中文 Markdown 摘要。
- `outputs/demo/mock-evidence-index.csv`：中文 CSV header 的证据索引，使用 Excel-friendly UTF-8 with BOM，可在 Windows Excel 中直接打开。

`outputs/demo/` 已被 `.gitignore` 忽略，不应提交。

## 如何读取输出

- `package.json`：评估后的 mock evidence package，包含 `evidenceStrength`、`qualityGate`、`riskFlags`、`reviewAction` 等字段。
- `mock-report.md`：面向 GitHub 阅读的中文 Markdown 摘要，包含 `摘要`、`事件概览`、`纳入事件`、`复核提示` 和 `边界说明`。
- `mock-evidence-index.csv`：中文 CSV header 的证据索引表，字段稳定，使用 Excel-friendly UTF-8 with BOM，适合用 Windows Excel 直接打开并快速扫描。

`package.json` 保留机器字段和机器枚举值，例如 `eventType=weekday_overtime`、`qualityGate=needs_review`。公开报告和 CSV 会使用中文展示标签，例如 `工作日加班`、`需复核`、`证据来源单一`、`群聊`、`Git 记录`。

## 自定义输出目录

```powershell
python scripts/run_demo.py --output-dir tmp/demo-output
```

自定义目录也只应用于生成 mock output，不要放入真实材料。

## 如何清理输出

清理默认 demo 输出：

```powershell
Remove-Item -Recurse -Force outputs/demo
```

下一次运行 demo 会重新创建目录。

## demo 不会做什么

demo 不会：

- 读取真实微信聊天、群聊、截图、导出记录或 message ID。
- 扫描真实 Git 仓库、源码、分支或 commit hash。
- 读取真实录音、转写、会议纪要或用户本地文件。
- 处理真实公司名、人名、项目名、金额、地址、手机号、合同、工资或身份标识。
- 生成法律意见、法律结论或结果承诺。

如果要实验，请只创建 fictional mock data。不要把真实案件材料脱敏后放进本仓库。
