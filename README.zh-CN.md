# Research Workbench

**给 coding agent 的研究工作台：围绕问题研究，交付结论和可查阅的依据。**

给 Codex / Claude Code 用的开源研究 skill，配一个本地 Python CLI。
Agent 负责合成角色、访谈和分析，CLI 负责保存、检查引用和生成 Markdown / HTML。
不需要先建角色库，也不需要额外的模型 API key。调用宿主模型仍会消耗正常额度。

模拟访谈是目前已实现的一个研究模块，适用于工作、消费和生活场景。整体设计支持按需
组合社媒侦察、竞品研究、资料分析和模拟访谈；其他模块、角色库及批量采集尚未实现。
报告围绕研究问题交付结论，而不是展示所有研究过程。模拟结果用于提出和挑战假设，
不能当作真实需求或付费意愿验证。

## 安装

需要 Python 3.11+ 和 Git。

```bash
git clone https://github.com/YichenBC/research-workbench.git
cd research-workbench
python3 -m venv .venv
source .venv/bin/activate
python -m pip install .

research-workbench install --target codex --scope user
research-workbench install --target claude --scope user
```

按需安装其中一个宿主即可。启动 Agent 时保持此虚拟环境已激活，让 CLI 在 PATH 中；
也可用已有的 `uv tool install .` 或 `pipx install .` 安装。
Codex 用 `$research-workbench`，Claude Code 用 `/research-workbench` 调用。
同名 skill 不会被静默覆盖。[更多安装说明](docs/installation.md)。

## 给它一句任务

> 研究一个排班工具。按一线员工和审批者两个角色对比：员工班次稳定、现有表格够用；
> 审批者经常处理临时换班。合成两个角色，各做三轮模拟访谈，生成中文报告。
> 不联网，保存到 studies/scheduling。

也可以要求“只生成角色”“继续上次访谈”“只用已有记录更新报告”，或者自行指定研究方法。
角色不绑定行业，方法和数量由用户决定。

## 交付什么

- **主报告**：先展示结论、共识与分歧、建议和待验证问题，简要交代依据与局限。
- **证据附件**：单独保存角色设定、假设、方法与完整访谈；主报告引用可跳转到具体问答。
- **本地文件**：Markdown、HTML、研究及报告 JSON 快照；可续接，旧报告保留。

分享时带上整个报告目录即可保留附件链接；只阅读主报告也能理解主要结论。

[示例报告](examples/scheduling/report.md)来自明确标记的手工合成示例；
[验收记录](evals/README.md)另行说明两个宿主实际执行的情况。
CLI 本身不会生成内容，不会联网抓取或自动联系用户。

完整命令、数据格式和开发说明见 [English README](README.md) 与 [数据契约](docs/contract.md)。
