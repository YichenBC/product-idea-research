# 修正版002/003独立语义复核

复核日期：2026-10-16。对象：study_revision 12、report-revised.json、study/reports/002、最终003及claim-review-revised.json。

结论：原SEM-001至SEM-011的纠正均得到支持。14个修改后的need字段、修正的比较和发现没有保留已指出的引用缺口；新增小红书卡及Subtitle Edit结论未观察到会改变产品排序的无依据断言。002另有一处不影响选择的计数措辞；003已改为7条provided来源记录、9个短摘录并复核通过。本次所检查的纠正项无未关闭问题。本结论是指定修正和新增材料的语义复核，不是总体准确率，也不证明之后的新请求会自动避免同类错误。

## 范围和分母

- 9张-r2卡中14个实际修改字段全部复核：12个引用修正、1个频率措辞、1个父问题上下文。
- 修正的比较2和f-seller各1项。
- 新增4张小红书卡全部11个non-unknown字段（其中2个payment、0个frequency），7条provided来源记录、9个短excerpt。
- 新增f-existing-caption、f-xhs共2项finding；Subtitle Edit比较1项；字幕机会及下一步变更全部检查。
- 官方4个URL均独立公开重开核对；小红书只核对提供摘录与上下文，没有冒称独立阅读全文。
- 002研究快照保存完整台账188来源/40需求；报告明确选择187来源/31需求，9张旧卡没有重复进入选择。187来源由174既有社媒、7 provided、6可读官方组成。保留1条失败官方记录在台账。
- 001/study.json和001/report.json的SHA-256与首次审查记录一致；原27张卡在新台账中逐项保持原内容，9张-r2追加。初审时report-revised.json与002/report.json一致；末次复核与003/report.json一致。002原封保留；003研究台账与002逐字节一致，报告仅两处摘录计数措辞发生变化。

## 14个修改字段逐项复核

| 新字段 | 修正后精确support | 判定 |
|---|---|---|
| n-mobile-r2.outcome | s2-post:e1, s2-post:e2, s2-post:e3 | 支持；在外也能快速更新并导入历史Excel |
| n-mobile-r2.friction | s2-post:e1, s2-post:e2 | 支持；手机Excel体验不理想，不愿手工重新录入数百项 |
| n-mobile-r2.payment | s2-post:e3 | 支持；有条件愿付费，不是已付费 |
| n-spromo-r2.outcome | s3-post:e1, s3-post:e2 | 支持；出售整合表格 |
| n-spromo-r2.payment | s3-post:e2, s3-post:e3 | 支持；20美元为卖方拟价；评论有免费副本激励 |
| n-style-r2.friction | fw-v2-post:e1, fw-v2-post:e2 | 支持；频繁收到标点、大小写和漏改意见 |
| n-caption-batch-r2.friction | fw-v5-post:e1, fw-v5-post:e2 | 支持；同步、语法修正耗时 |
| n-variants-r2.actor | s1-post:e1, s1-post:e2 | 支持；3D打印灯具卖家 |
| n-stalled-r2.outcome | fx-post:e1, fx-post:e3 | 支持；获得及时反馈并保持客户关系 |
| n-stalled-r2.workaround | fx-post:e2 | 支持；约定V1–V3和反馈截止时间 |
| n-stalled-r2.friction | fx-post:e3 | 支持；客户接受流程但不提供反馈 |
| n-align-r2.outcome | fw-v3-post:e1, fw-v3-c21:e1, fw-v3-c15:e1, fw-v3-c15:e2 | 支持；保留指定译文并正确导出定时SRT |
| n-sheet-enough-r2.frequency | fw-s3-c11:e1 | 支持；每月一至两次，自述数小时；时长是单次还是月总量不明确 |
| n-revision-r2.friction | fw-f1-c12:e1, fw-f1-c11:e1 | 支持；没有明确合同流程 |

SEM-009：比较2现增fw-s3-c13:e1/e2，明确Etsy和Shopify的表格组合；c19只承担记账员培训证据。修复通过。

SEM-010：f-seller与n-sheet-enough-r2.frequency统一成一至两次/月、数小时分母不明，不再把单次与月总量混用。修复通过。

SEM-011：n-revision-r2.friction同时保留c11合同问题与c12否定回答，与首次已读raw/f1.txt上下文一致。它仍指合同修订流程不明确，不应扩大为所有业务流程均缺失。现有具体字段可接受。

## 小红书新增卡：逐项审计

| 卡及字段 | 精确依据 | 判断 |
|---|---|---|
| need-timing.actor | xhs-timing-clarification:e1 | 从时间轴麻烦推断做字幕的人，职业和付费身份保留未知，适当。 |
| need-timing.outcome | xhs-timing-clarification:e1 | 降低麻烦为明确标注的推断，未添加技术交付约束。 |
| need-timing.friction | xhs-timing-clarification:e1 | “打时间轴很麻烦”被忠实保留。 |
| need-timing.payment | xhs-timing-post:e1 | 条件性低价愿付，不是金额、成交或订阅意愿。 |
| need-alignment-resolved.actor | xhs-align-post:e1 | 人工对齐者，职业未知，推断适当。 |
| need-alignment-resolved.outcome | xhs-align-post:e2 | 获得对齐版本是可支持的推断。 |
| need-alignment-resolved.workaround | xhs-align-post:e1/e2 | 手动波形之后找到版本；先后关系来自提供context，不冒充独立验证。 |
| need-alignment-resolved.friction | xhs-align-post:e1 | 仅推断存在人工步骤；当前剩余痛点与成本保留未知。 |
| need-free-alternative.workaround | xhs-timing-free:e1 + xhs-timing-domain:e1 | 免费说法与域名由同评论者同链条补充；不算两个成功案例。 |
| need-free-alternative.payment | xhs-timing-free:e1 | 免费是评论者描述，非价格实测或付款，限定适当。 |
| need-subeasy-unclear.workaround | xhs-align-tip:e1 | 只有推荐；作者OK在反证/局限中不被升级成试用成功。 |

3张非candidate卡（resolved、adjacent、unclear）全部审：已解决分类仅限作者自述找到版本，未验证文件；免费建议不等于作者已满足；SubEasy推荐不构成新增买家，也没有凭未知关联判为推广。报告f-xhs保留了这些区分。2个讨论家族没有算成2个同类付费需求；AI写的实验回顾未当模型成绩、API成本或真实支付证据。

提供材料的定位限制明确：全部7项source_type=provided、access=excerpt。部分来源只有“OK”“免费的”等极短文本，角色及回复链需依赖上游context/parent_source_id；本复核不能独立证明上游捕获真实完整。报告没有隐去该限制。

## Subtitle Edit官方证据与推断范围

| 页面 | 独立重开核对 | 报告使用是否越界 |
|---|---|---|
| [文档首页](https://subtitleedit.github.io/subtitleedit/) | L8明确免费开源及Subtitle Edit 5版本。 | 仅厂商声明，未称实测，合适。 |
| [Import Plain Text](https://subtitleedit.github.io/subtitleedit/features/import-plain-text.html) | L29–37描述给定文本对音频强制对齐、原文保留；L47另有转写后匹配路径。 | 报告只说已有保持文本的音频对齐，没有推广为任意语种和输入下都可靠。 |
| [Import Spreadsheets](https://subtitleedit.github.io/subtitleedit/features/import-csv-xlsx.html) | L7–11与49–61支持表格导入、自定义文字/时间列；只有文字列也可导入。 | 能导入不等于能自动判断外语译文与源语句子的语义对应。报告正确保留区别。 |
| [Improve Time Codes](https://subtitleedit.github.io/subtitleedit/features/improve-time-codes.html) | L7、12、85–88限定对齐到实际音频；原文有“in the spoken language”和“a translation cannot be aligned”。同页还说明粗同步、语言支持及误配限制。 | 报告限定到此功能，没有推出整个Subtitle Edit或所有竞品都不支持跨语种工作流。 |

f-existing-caption、比较4、机会1及下一步共同表达的是“先按输入拆分任务并同任务比较”，而不是宣布技术空白。方案仍需人审时轴、语义和断句，且承认上游表格交接可能更便宜。只有一个历史批准译稿痛点的限制仍保留。标题改为源语字幕映射后，还移除了相邻重切卡n-recut作为该机会的need链接，减少混同。

## 已关闭的新增措辞问题：来源记录数与摘录数

002的f-xhs.limitations[0]和末尾limitations[0]曾将中文提供材料写成“7条摘录”。实际是：

- xhs-align-post：2个excerpt。
- xhs-timing-post：2个excerpt。
- 其余5条来源：各1个excerpt。

合计7条来源记录、9个excerpt。003两处均已统一写“7条提供来源记录（9个短摘录）”，复核关闭。这不影响任何产品选择或需求判断；28个直接社媒组与2个provided家族在报告局限中已分别解释，不需要把它们混成28或30位买家。

## 结论边界

本次能关闭SEM-001至SEM-011的已知修正项，并确认新增11个小红书字段及4页官方文档没有引入所检查范围内的过断言。X原帖的独立核验限制仍沿用首次审查；尚无竞品实际运行、真实客户交付或付款验证。不能把针对审查反馈的修正等同于盲测泛化能力。

输入标识：

- .eval-runs/discovery-forward/study/reports/002/study.json: 41e41a5a5659c916c146c3695c99ba309301bc47342e448a7a09e3b7fa562aee
- .eval-runs/discovery-forward/study/reports/002/report.json: da9388488ee852503fc0ab93f611934bf53c5a2cd9d7878825d7e1c51c9ac32f
- .eval-runs/discovery-forward/claim-review-revised.json: 27f30296592ae5a9197232cd3be961ab71b685ae734473f136e9b3eebc288042
- 最终 .eval-runs/discovery-forward/study/reports/003/study.json: 41e41a5a5659c916c146c3695c99ba309301bc47342e448a7a09e3b7fa562aee
- 最终 .eval-runs/discovery-forward/study/reports/003/report.json: e3dbfc9f57b095c8a5010580a01e64ce5e59cf012fced0a05c7c247d83966d86
