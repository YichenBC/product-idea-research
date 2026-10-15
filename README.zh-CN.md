# Product Idea Research

**让 Codex / Claude Code 从公开讨论、竞品和模拟访谈中形成有依据、可复查的研究结论。**

一个共享 Skill，加一个本地 Python CLI。社媒调研、竞品研究、模拟访谈可以
单独运行，也可以组合，最终汇总成一份研究报告。可以从想法、竞品、链接、已有
反馈或自定义方法开始，也可以接着已有研究往下做。

Agent 负责搜索、阅读、分析与模拟；CLI 负责保存证据、检查引用、提示重复材料和
导出 Markdown / HTML。无需额外模型 API key、Atypica 订阅、服务器或角色数据库；
仍会使用你的编程 Agent 本身的额度和工具。

[English](README.md) · [数据契约](docs/contract.md) · [验收记录](evals/README.md)

## 可以做什么

| 你提出的任务 | 交付 |
|---|---|
| 只看社媒上的需求、替代方法与反对意见 | 带上下文和出处的发现、证据空白与可验证机会 |
| 只比较几个竞品 | 功能/工作流/价格条件对照、未知项、选择建议 |
| 按我的方法合成角色并访谈，不联网 | 模拟结论、分歧与现实验证问题 |
| 社媒 + 竞品 + 模拟访谈 | 一份综合报告，区分外部材料、研究推断和模拟 |
| 分析我提供的反馈，不上网 | 保留原始定位和矛盾意见的材料分析 |
| 继续上次研究 / 只重新形成报告 | 新增研究轮次，或直接复用已保存材料 |

模块由用户选择，不强制从头跑完整流程。适用于工作与生活场景，不限于某个行业。
明确指定的数量、渠道、语言和研究方法会保留；访问受限时说明缺口，不虚构材料补数。

原名 **Research Workbench**。已有用户请先按[更名迁移说明](docs/installation.md#rename-from-research-workbench-v02-and-earlier)更新；旧 CLI 命令保留兼容，研究数据无需迁移。

## 安装

需要 Python 3.11+、Git，以及能使用终端和文件的 Codex / Claude Code。
在线调研还需要宿主提供搜索或浏览工具；也可以直接使用你提供的材料。

```bash
git clone https://github.com/YichenBC/product-idea-research.git
cd product-idea-research
python3 -m venv .venv
source .venv/bin/activate
python -m pip install .

product-idea-research install --target codex --scope user
product-idea-research install --target claude --scope user
```

Windows 用 `.venv\Scripts\Activate.ps1` 激活。启动 Agent 时保持环境激活，
或使用 `pipx install .` / `uv tool install .`。安装后可能需要重启 Agent 才能
发现 Skill。只装到当前项目时使用 `--scope project --directory /path/to/project`。
安装器不会覆盖已存在但内容不同的 Skill；[更新方式](docs/installation.md)。

## 怎么用

Codex 使用 `$product-idea-research`，Claude Code 使用 `/product-idea-research`。
接着自然描述任务：

> 调研视频团队审校翻译字幕的流程。看看公开讨论和已有工具，再用两个模拟角色
> 质疑我的想法。输出一份中文报告，保留现有办法已经够用的证据，推荐个人能交付的
> 小范围试验。

也可以只做一个模块：

> 只比较这三个产品对双人团队的适用性，核实官方功能与价格条件。不要做角色或访谈。

或完全不联网：

> 分析这份导出的用户反馈，不联网。保留相反意见，指出还缺哪些依据，形成研究报告。

## 真实调研示例

[字幕审校研究](examples/subtitle-research/README.md)：[综合报告](examples/subtitle-research/combined/report.md) · [纯社媒报告](examples/subtitle-research/social/report.md) · [纯竞品报告](examples/subtitle-research/competitor/report.md)。附原始证据、复审修订和可离线重放的数据。

## 报告是什么样

主报告呈现结论、分歧、竞品对照或机会选择、下一步与局限。原始来源摘录、采样方法、
角色卡和完整问答放在证据附件中，点击引用可以核查。模拟结论始终与外部材料区分。

每次导出产生独立目录：`report.md/html`、`evidence.md/html` 和冻结的研究/报告 JSON。
旧版本不会被覆盖；分享时保留整个目录即可保留附件链接。

[模拟报告示例](examples/scheduling/report.md) ·
[先前 Codex 实跑示例](examples/household/report.md)

## CLI 的职责

- `init / ingest`：初始化并分批保存不可变记录；失败批次不会部分写入。
- `status / check`：查看进度，校验所选材料、引用、报告版本与覆盖情况。
- `audit`：检查读取深度、讨论分组、重复 URL/摘录；不生成“真实性分数”。
- `render`：导出主报告、证据附件与快照。
- `install`：将同一份 Skill 安装给两种宿主。

CLI 不会自行搜索或生成内容。新一轮研究由 Agent 运行 Skill。

## 能力边界

不保证任何社媒平台都能访问；登录墙和不可读评论会保留为缺口。搜索摘要只能作为线索，
不能进入结论引用。同一讨论的多条评论不等于多个独立客户。公开帖子是作者自述，
官网是厂商声明，模拟回答是研究假设，都不能直接证明付费意愿或市场规模。

不包含托管界面、专用平台爬虫、共享角色库或自动外联。角色属性仍标记为假设/未知。
`complete` 只表示本次声明的研究范围完成，不表示需求已验证。

文件保存在本地，但研究材料仍可能通过宿主的模型与工具服务处理。实际宿主测试结果
与限制以[验收记录](evals/README.md)为准，不把目录安装成功当成模型工作流验证成功。

MIT 开源；Python 标准库运行时。开发：`python -m pip install -e '.[dev]'`，
`python -m pytest -q`，`python -m build`。
