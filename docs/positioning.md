# Positioning

## 问题

加班证据整理最难的不是把聊天记录、提交记录或截图堆在一起，而是让这些线索能够回答几个基础问题：

- 任务从哪里来？
- 什么时候开始和结束？
- 处理过程是否连续？
- 结果是否有反馈？
- 证据能否定位回来源？
- 哪些地方需要人工复核？

## 方法

`overtime-evidence-kit` 用完全虚构的 mock 数据演示一套结构化方法：

- 用 event 表达候选加班事件。
- 用 evidence item 表达可定位的证据点。
- 用 quality gate 和 risk flags 标记复核重点。
- 用 Markdown report 和 CSV evidence index 生成可读输出。

## 为什么需要结构化证据包？

结构化证据包能帮助人工复核者快速看到时间线、证据来源、缺口和风险。它强调可追踪、可复核，而不是把材料堆在一起。它不会替代判断，但能减少材料混乱带来的误读。

## 为什么公开仓库只做 mock-only？

公开仓库适合展示方法、讨论 schema、运行 demo 和改进质量门，不适合接收真实隐私材料。mock-only 是为了让项目可公开协作，同时保护用户。

## 公开仓库证明了什么？

它证明了一条本地可运行的链路：mock source -> package -> rules evaluation -> validation -> Markdown report -> CSV index。

## 公开范围之外

公开仓库不处理真实案件，不接收真实证据，不提供法律意见，不承诺任何结果，也不包含私有服务 SOP 或收费交付材料。
