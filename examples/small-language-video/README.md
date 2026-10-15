# 小语种 AI 视频：真实资料研究案例

2026-10-15，使用 Product Idea Research，完成公开材料采集、竞品核查、合成访谈、反证复核与统一报告。

- [最终中文报告](report.md) · [HTML 文件](report.html)
- [证据、检索过程与完整合成访谈](evidence.md) · [HTML 文件](evidence.html)
- [冻结研究数据](study.json) · [报告草稿](report.json) · [引用检查](check.json) · [覆盖审计](audit.json)

## 结论与范围

优先验证越南语客户定稿字幕的对齐与交付工具，拟议测试范围为英语源片。
多语课程改版检查仍是相邻市场假设；Welsh教学模板、Darija吉祥物短课先观察。
具体客户、最强现有替代、个人可做的MVP、假设成本和停止条件见报告。

本轮读取25个社媒/社区讨论家族（首轮22、父侧补查3），核查7个软件/平台
的官方资料并补充1个人工服务案例；来源类型包含Reddit、LinkedIn、专业社区、
AppSumo问答、GitHub Discussions等。共50条记录，其中45条可引用，归为38个
可读材料组；追加摘录不增加独立讨论。它不是25个客户，更不是几百条市场普查。

X、小红书、Pantip没有取得可引用正文。部分官方报价相互冲突，API实际费用未测。
因此保留`partial`，不伪装为全面市场验证。未登录、试用、采购、上传客户视频或外联；
未做音视频质量实测。角色与9轮回答全部合成，只用于提出拒绝条件。

## 评估后做了什么

独立首轮报告保留在本地评估快照中；父侧增量阅读真实商业案例后，将优先建议
从宽泛配音服务收窄到客户提供译稿和审阅人的交付工具，并把通用多语文件管理
降为相邻市场观察项。已有流程能完成任务是反证，不能被写成新软件购买意愿。
语种方向、价格单位、模型/API门槛和仅由context承载的主张均经复核；删除了
没有直接摘录支持的Rask精确语言数等表述。所有试单价格与成本均是假设。

[本轮工具迭代与验证记录](../../evals/README.md)。这不是与Atypica的配对质量胜负测试。

## 离线重放

复制`study.json`为新目录的`research.json`，然后使用已安装的CLI：

```bash
mkdir -p /tmp/product-idea-live-replay
cp examples/small-language-video/study.json /tmp/product-idea-live-replay/research.json
product-idea-research check /tmp/product-idea-live-replay --report examples/small-language-video/report.json
product-idea-research audit /tmp/product-idea-live-replay --report examples/small-language-video/report.json
product-idea-research render /tmp/product-idea-live-replay --report examples/small-language-video/report.json --format both
```

重放只检查保存的数据与导出，不重新联网，也不证明网页当前仍相同。
分享HTML时同时保留evidence.html；GitHub直接预览建议使用Markdown。
