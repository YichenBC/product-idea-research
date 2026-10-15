# 真实需求发现：帖子、评论、反证与可交付机会

2026-10-16。第二轮真实材料评测，独立首稿之后经过逐字段审查和增量核查。

[中文决策报告](report.md) · [HTML](report.html) · [需求池](needs.md) ·
[表格下载](needs.csv) · [来源与检索过程](evidence.md) · [评测与修改记录](../../evals/README.md)

## 这次找到什么

| 方向 | 当前判断 | 关键条件 |
|---|---|---|
| 批准译稿映射到源语字幕时间轴 | 先试按次交付 | 要胜过表格交接；不混同同语种音频对齐，不承诺所有小语种 |
| 卖家数据整理与既有工具初始配置 | 先试服务式交付 | 既有表格可能已足够，验证第二个月复用再考虑持续产品 |
| 项目版本与范围变更说明 | 观察 | 文件整理要能收费，不能期待软件解决客户拒绝守约 |
| 变体履约单、移动库存 | 分别观察 | 各只有一个原始讨论家族；需要第二个可复现任务 |
| 通用免费字幕翻译包装 | 本轮不优先 | 免费替代、已解决案例和低价诉求较多 |

价格、成本、获客方式和试验阈值均是假设；没有真实收费、外联或客户验证。

## 数量口径

- 基础材料：13篇Reddit正文、65条评论。
- 新增独立采集：12篇Reddit正文、78条保留评论，逐条有永久链接。
  [读取清单](reddit-read-manifest.json)另含43条未保留评论，不计入保留量。
- 父侧X/LinkedIn：3篇正文、3条保留评论；可见但未保留或截断的回复另行记录。
- 父侧小红书：2篇笔记、27条可见评论，最终保留2帖5评论共7条来源记录（9个短摘录）；
  [读取清单](xhs-read-manifest.json)。离线分析者只读这些提供材料，未冒充亲自浏览。
- 本报告选中187条记录，其中181条社媒或其提供摘录、6条可读官方资料。
  30个社媒来源讨论家族含2个提供材料家族，不等于30个独立买家。
- 需求池31张卡、14个簇。修正前的9张卡仍在台账，不重复计算需求。

这是便利样本，英文Reddit占主导，未穷尽评论或达到数百条独立需求。
记录数量不衡量市场规模；当年的旧帖也不能证明今天仍有同样缺口。

## 原始输出与修正

[独立首稿输入](../../evals/discovery-round2/first-report.json)及
[当时台账](../../evals/discovery-round2/first-study.json)保留，便于复现首次输出。
审查全部27卡的106个非unknown字段，发现12个字段的具体摘录引用不充分、
1项比较的引用缺口，以及时长分母与父回复上下文两个改进项。
[审查清单](../../evals/discovery-round2/semantic-review.json)与
[9张修正版卡映射](../../evals/discovery-round2/correction-map.json)公开。

新增小红书留出案例及Subtitle Edit官方文档后，保留原先两条试交付方向，但收紧字幕
输入条件。官方文档说明同语种音频对齐已有能力，不能把它包装成新需求。
`check`通过只证明引用合法；修正来自语义审查，不是CLI自动判断。

## 离线重放

在仓库根目录运行，使用一个新目录：

```bash
mkdir -p /tmp/product-idea-discovery-replay
cp examples/demand-discovery/study.json /tmp/product-idea-discovery-replay/research.json
product-idea-research check /tmp/product-idea-discovery-replay --report examples/demand-discovery/report.json
product-idea-research pool /tmp/product-idea-discovery-replay --report examples/demand-discovery/report.json --review
product-idea-research render /tmp/product-idea-discovery-replay --report examples/demand-discovery/report.json --format both
```

重放保存材料与导出，不重新采集，也不证明网页仍然相同。第一稿同理使用first-study.json
和first-report.json。分享导出时保留整个目录，使报告、需求池和证据的相互链接有效。
小红书地址去除了临时访问参数，后来访问者可能需要在授权会话里搜索标题。
