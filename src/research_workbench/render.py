"""Conclusion reports with linked evidence appendices and frozen provenance."""

from __future__ import annotations

from collections.abc import Iterable
import html
import os
from pathlib import Path
import re
import shutil
import tempfile
from typing import Any, cast
from urllib.parse import quote, urlsplit

from . import store
from . import validation as v
from .types import JSONObject, JSONValue, PathInput, Study

ZH = {
    'Synthetic research': '合成研究',
    'All personas and interviews are simulations. These are hypotheses, not evidence of real customer demand.':
    '所有画像和访谈均为模拟。这些内容仅用于提出假设，不能作为真实客户需求的证据。',
    'Method': '研究方法', 'Question': '研究问题', 'Dimensions': '画像维度', 'Constraints': '约束',
    'Status': '完成状态', 'partial': '部分完成', 'complete': '完整', 'Revision': '修订号',
    'Personas: stored / planned / covered by selected interviews': '画像：已存储 / 计划 / 所选访谈覆盖',
    'Summary': '摘要', 'Role cards': '角色卡', 'Traits': '维度', 'Attributes and assumptions': '属性与假设',
    'assumed': '假设', 'unknown': '未知', 'Findings': '研究发现', 'Support': '支持材料',
    'Counterevidence': '反向材料', 'Limitations': '局限', 'Real-world next steps': '现实验证下一步',
    'Full simulated transcripts': '完整模拟访谈', 'Interview': '访谈', 'Persona': '画像',
    'Turn': '轮次', 'Answer': '回答', 'Assumptions': '假设', 'None supplied': '未提供',
    'Recipe': '研究方案', 'Provenance': '来源追溯', 'simulation': '模拟',
    'Evidence appendix': '研究材料附录',
    'Brief ID': '简报编号', 'Brief': '研究简报', 'Selected modules': '所选模块', 'Sources': '来源材料',
    'Discussion groups': '讨论组', 'Selected interviews': '所选访谈',
    'Read sources (full / excerpt)': '已读来源（全文／摘录）',
    'Snippet / unavailable': '仅摘要／无法访问',
    'Discussion groups (material families)': '讨论组（材料组）',
    'Source': '来源', 'Excerpt': '摘录', 'Run': '研究轮次', 'Module': '模块',
    'social': '社媒调研', 'competitor': '竞品调研', 'Objective': '目标', 'Queries': '检索词',
    'Source statement': '来源陈述', 'Inference': '推断', 'Simulation': '模拟', 'Mixed': '混合',
    'Evidence type': '证据类型', 'Source statements reflect saved material, not independently verified facts.':
    '来源陈述反映所保存材料的内容，并非独立核实的事实。',
    'Mixed reasoning combines source material and explicitly identified simulated responses.':
    '混合推理结合来源材料与明确标注的模拟回答。',
    'No eligible evidence was collected; no findings can be supported yet.':
    '尚未收集到可用证据，暂时无法形成有支持材料的发现。',
    'Alternative comparisons': '替代方案比较', 'Alternative': '替代方案', 'Category': '类别',
    'Dimension': '比较维度', 'Assessment': '评估', 'Comparison': '比较',
    'direct': '直接竞品', 'indirect': '间接替代', 'manual': '人工方式', 'do_nothing': '维持现状',
    'Opportunities': '机会', 'Opportunity': '机会', 'Priority': '优先级', 'Proposal': '方案',
    'Audience': '目标群体', 'Problem': '问题', 'Rationale': '判断理由', 'Risks': '风险',
    'Validation': '验证方式', 'test_now': '立即测试', 'watch': '观察', 'drop': '放弃',
    'Platform': '平台', 'Source type': '来源类型', 'Published': '发布日期', 'Accessed': '访问日期',
    'Language': '语言', 'Access': '访问范围', 'Discussion group': '讨论组', 'Context': '上下文',
    'Original URL': '原始链接', 'Locator': '原文位置', 'Source ID': '来源编号',
    'post': '帖子', 'comment': '评论', 'review': '评价', 'official': '官方材料',
    'article': '文章', 'provided': '提供的材料', 'full': '完整', 'excerpt': '摘录',
    'snippet': '搜索摘要', 'unavailable': '无法访问',
    'Discussion groups are material families, not independent customers.':
    '讨论组表示材料所属的讨论或文档组，不代表独立客户。',
    'Snippet or unavailable material cannot support findings.': '搜索摘要或无法访问的材料不能支持研究发现。',
    'Selected interviews / personas covered / planned': '所选访谈 / 覆盖画像 / 计划画像',
    'Interview evidence is simulated; conclusions remain hypotheses for real-world validation.':
    '访谈材料为模拟生成；结论仍是假设，需要现实验证。',
}


def md_escape(value: Any) -> str:
    # Numeric entities survive Markdown rendering without creating formatting,
    # links, raw HTML, fenced code, or block syntax from untrusted prose.
    return ''.join('&#%d;' % ord(c) if c in '&<>\\`*_{}[]()#+-.!|~:\"\'' else c
                   for c in str(value)).replace('\r', '&#13;').replace('\n', '<br>')


class Document:
    def __init__(self, kind: str, title: str, chinese: bool) -> None:
        self.kind = kind
        self.chinese = chinese
        self.parts: list[str] = []
        if kind == 'html':
            self.parts.append('<!doctype html><html lang="' + ('zh' if chinese else 'en') + '"><head>'
                              '<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
                              '<title>' + html.escape(title) + '</title><style>'
                              'body{max-width:960px;margin:auto;padding:2rem;font:16px/1.6 system-ui,sans-serif;color:#162333}'
                              'h1,h2,h3{line-height:1.25}h2{margin-top:2.5rem;border-bottom:1px solid #ccd3dc}'
                              'p,li{overflow-wrap:anywhere;white-space:pre-wrap}a{color:#075eb5}'
                              '.notice{padding:1rem;background:#fff2cd;border:2px solid #947000;border-radius:6px}'
                              '.table-wrap{overflow-x:auto}table{width:100%;border-collapse:collapse;margin:1rem 0}'
                              'th,td{text-align:left;vertical-align:top;padding:.65rem;border:1px solid #ccd3dc;overflow-wrap:anywhere}'
                              'th{background:#eef3f7}td{white-space:pre-wrap}'
                              'blockquote{margin:1rem 0;padding:.5rem 1rem;border-left:4px solid #9baec4;background:#f4f7fa}'
                              '</style></head><body>')

    def tr(self, text: str) -> str:
        return ZH.get(text, text) if self.chinese else text

    def escape(self, text: Any) -> str:
        return html.escape(str(text)) if self.kind == 'html' else md_escape(text)

    def heading(self, level: int, text: str, anchor: str | None = None) -> None:
        safe = self.escape(text)
        if self.kind == 'html':
            attr = f' id="{anchor}"' if anchor else ''
            self.parts.append(f'<h{level}{attr}>{safe}</h{level}>')
        else:
            if anchor:
                self.parts.append(f'<a id="{anchor}"></a>')
            self.parts.append('#' * level + ' ' + safe)

    def paragraph(self, text: str, notice: bool = False) -> None:
        safe = self.escape(text)
        self.parts.append(f'<p class="notice">{safe}</p>' if self.kind == 'html' and notice else
                          f'<p>{safe}</p>' if self.kind == 'html' else safe)

    def quotation(self, text: str) -> None:
        """Distinguish verbatim source excerpts from the report author's prose."""
        safe = self.escape(text)
        self.parts.append(f'<blockquote><p>{safe}</p></blockquote>' if self.kind == 'html' else f'> {safe}')

    def items(self, texts: Iterable[str]) -> None:
        texts = list(texts)
        if not texts:
            self.paragraph(self.tr('None supplied'))
        elif self.kind == 'html':
            self.parts.append('<ul>' + ''.join('<li>' + self.escape(t) + '</li>' for t in texts) + '</ul>')
        else:
            self.parts.append('\n'.join('- ' + self.escape(t) for t in texts))

    def links(self, label: str, refs: Iterable[tuple[str, str]], filename: str = '') -> None:
        self.paragraph(self.tr(label))
        links = []
        for anchor, text in refs:
            safe = self.escape(text)
            # Both filename and anchor are generated here, never taken from user IDs.
            target = f'{filename}#{anchor}'
            links.append(f'<a href="{target}">{safe}</a>' if self.kind == 'html' else f'[{safe}]({target})')
        self.parts.append((' · '.join(links)) if links else self.escape(self.tr('None supplied')))

    def table(self, headers: list[str], rows: Iterable[list[str]]) -> None:
        """Render plain-text cells; citations and long details follow the table."""
        safe_headers = [self.escape(self.tr(h)) for h in headers]
        safe_rows = [[self.escape(cell) for cell in row] for row in rows]
        if self.kind == 'html':
            self.parts.append('<div class="table-wrap"><table><thead><tr>' +
                              ''.join('<th scope="col">' + h + '</th>' for h in safe_headers) +
                              '</tr></thead><tbody>' +
                              ''.join('<tr>' + ''.join('<td>' + c + '</td>' for c in row) + '</tr>'
                                      for row in safe_rows) + '</tbody></table></div>')
        else:
            self.parts.append('\n'.join(['| ' + ' | '.join(safe_headers) + ' |',
                                         '| ' + ' | '.join('---' for _ in headers) + ' |'] +
                                        ['| ' + ' | '.join(row) + ' |' for row in safe_rows]))

    def external_link(self, url: str) -> None:
        """Escape a validated original URL separately from its visible text."""
        label = self.escape(url)
        if self.kind == 'html':
            self.parts.append(f'<p><a href="{html.escape(url, quote=True)}">{label}</a></p>')
        else:
            # Percent-encode destination delimiters while preserving URL semantics.
            # Escape ampersands too: Markdown parsers decode HTML entities in URLs.
            destination = quote(url, safe=":/?#@!$&*+,;=%-._~")
            if urlsplit(url).netloc.startswith('['):
                # IPv6 authority brackets must remain literal for a usable URL.
                # Brackets are safe inside a Markdown destination; path/query
                # brackets remain encoded, along with all parentheses and quotes.
                destination = destination.replace('%5B', '[', 1).replace('%5D', ']', 1)
            destination = html.escape(destination, quote=True)
            self.parts.append(f'[{label}]({destination})')

    def finish(self) -> str:
        return '\n\n'.join(self.parts) + ('\n</body></html>\n' if self.kind == 'html' else '\n')


def selected_interviews(state: Study, report: JSONObject) -> list[JSONObject]:
    interviews = {i['id']: i for i in state['interviews']}
    return [interviews[i] for i in report['interview_ids']]


class Selection:
    """A deterministic citation namespace shared by both exported documents."""

    def __init__(self, state: Study, report: JSONObject) -> None:
        runs = {run['id']: run for run in state.get('runs', [])}
        self.runs = [runs[ident] for ident in report.get('run_ids', [])]
        sources = {source['id']: source for source in state.get('sources', [])}
        source_ids = dict.fromkeys(ident for run in self.runs for ident in run['source_ids'])
        self.sources = [sources[ident] for ident in source_ids]
        self.interviews = selected_interviews(state, report)
        self.interview_positions = {item['id']: n for n, item in enumerate(self.interviews, 1)}
        self.excerpt_positions = {(source['id'], excerpt['id']): (n, m)
                                  for n, source in enumerate(self.sources, 1)
                                  for m, excerpt in enumerate(source['excerpts'], 1)}

    def references(self, doc: Document, refs: Iterable[JSONObject]) -> list[tuple[str, str]]:
        result = []
        for ref in refs:
            if 'source_id' in ref:
                source, excerpt = self.excerpt_positions[(ref['source_id'], ref['excerpt_id'])]
                result.append((f'source-{source}-excerpt-{excerpt}',
                               f'{doc.tr("Source")} {source} · {doc.tr("Excerpt")} {excerpt}'))
            else:
                interview = self.interview_positions[ref['interview_id']]
                result.append((f'turn-interview-{interview}-{ref["turn"]}',
                               f'{doc.tr("Interview")} {interview} · {doc.tr("Turn")} {ref["turn"]}'))
        return result


def report_document(state: Study, report: JSONObject, kind: str) -> Document:
    brief_or_recipe = state.get('brief') or state['recipe']
    return Document(kind, report['title'], brief_or_recipe['language'].lower().startswith('zh'))


def decision_tables(doc: Document, report: JSONObject, selected: Selection) -> None:
    """Keep tables narrow and put detailed judgments and exact citations below."""
    tr = doc.tr
    comparisons = report.get('comparisons', [])
    if comparisons:
        doc.heading(2, tr('Alternative comparisons'))
        doc.table(['Alternative', 'Dimension', 'Assessment'],
                  [[f'{n}. {row["alternative"]} ({tr(row["category"])})', row['dimension'], row['assessment']]
                   for n, row in enumerate(comparisons, 1)])
        for n, row in enumerate(comparisons, 1):
            doc.heading(3, f'{tr("Comparison")} {n}: {row["alternative"]}')
            doc.links('Support', selected.references(doc, row['support']), f'evidence.{doc.kind}')
            doc.paragraph(tr('Limitations'))
            doc.items(row['limitations'])
    opportunities = report.get('opportunities', [])
    if opportunities:
        doc.heading(2, tr('Opportunities'))
        doc.table(['Opportunity', 'Priority', 'Proposal'],
                  [[f'{n}. {row["title"]}', tr(row['priority']), row['proposal']]
                   for n, row in enumerate(opportunities, 1)])
        for n, row in enumerate(opportunities, 1):
            doc.heading(3, f'{tr("Opportunity")} {n}: {row["title"]}')
            for key, label in (('audience', 'Audience'), ('problem', 'Problem'), ('alternative', 'Alternative'),
                               ('rationale', 'Rationale'), ('validation', 'Validation')):
                doc.paragraph(f'{tr(label)}: {row[key]}')
            doc.links('Support', selected.references(doc, row['support']), f'evidence.{doc.kind}')
            doc.paragraph(tr('Risks'))
            doc.items(row['risks'])


def document(state: Study, report: JSONObject, kind: str) -> str:
    """Keep the primary reading path focused on conclusions and decisions."""
    doc = report_document(state, report, kind)
    tr = doc.tr
    selected = Selection(state, report)
    brief_or_recipe = state.get('brief') or state['recipe']
    doc.heading(1, report['title'])
    doc.heading(2, tr('Summary'))
    doc.paragraph(report['summary'])
    if selected.interviews:
        doc.paragraph(tr('Interview evidence is simulated; conclusions remain hypotheses for real-world validation.'), notice=True)
    doc.paragraph(f'{tr("Question")}: {brief_or_recipe["question"]}')
    doc.paragraph(f'{tr("Status")}: {tr(report["status"])}')
    if selected.runs:
        doc.paragraph(tr('Selected modules') + ': ' + '; '.join(
            f'{tr(run["module"])} ({tr(run["status"])})' for run in selected.runs))
        read_count = sum(source['access'] in ('full', 'excerpt') for source in selected.sources)
        doc.paragraph(f'{tr("Sources")}: {len(selected.sources)} | '
                      f'{tr("Read sources (full / excerpt)")}: {read_count} | '
                      f'{tr("Snippet / unavailable")}: {len(selected.sources) - read_count} | '
                      f'{tr("Discussion groups (material families)")}: {len({s["group_id"] for s in selected.sources})} | '
                      f'{tr("Selected interviews")}: {len(selected.interviews)}')
        doc.paragraph(tr('Discussion groups are material families, not independent customers.'))
    if selected.interviews:
        covered = len({i['persona_id'] for i in selected.interviews})
        doc.paragraph(f'{tr("Selected interviews / personas covered / planned")}: '
                      f'{len(selected.interviews)} / {covered} / {state["recipe"]["persona_count"]}')
    doc.heading(2, tr('Findings'))
    if not report['findings']:
        doc.paragraph(tr('No eligible evidence was collected; no findings can be supported yet.'))
    if any(finding['kind'] in ('source', 'inference', 'mixed') for finding in report['findings']):
        doc.paragraph(tr('Source statements reflect saved material, not independently verified facts.'))
    labels = {'source': 'Source statement', 'inference': 'Inference', 'simulation': 'Simulation', 'mixed': 'Mixed'}
    for n, finding in enumerate(report['findings'], 1):
        doc.heading(3, f'{n}. {finding["statement"]}', f'finding-{n}')
        doc.paragraph(f'{tr("Evidence type")}: {tr(labels[finding["kind"]])}')
        if finding['kind'] == 'mixed':
            doc.paragraph(tr('Mixed reasoning combines source material and explicitly identified simulated responses.'))
        for key, label in (('support', 'Support'), ('counterevidence', 'Counterevidence')):
            doc.links(label, selected.references(doc, finding[key]), filename=f'evidence.{kind}')
        doc.paragraph(tr('Limitations'))
        doc.items(finding['limitations'])
    decision_tables(doc, report, selected)
    doc.heading(2, tr('Real-world next steps'))
    doc.items(report['next_steps'])
    doc.heading(2, tr('Limitations'))
    doc.items(report['limitations'])
    return doc.finish()


def source_evidence(doc: Document, selected: Selection) -> None:
    tr = doc.tr
    if selected.runs:
        doc.heading(2, tr('Selected modules'))
    for n, run in enumerate(selected.runs, 1):
        doc.heading(3, f'{tr("Run")} {n}: {tr(run["module"])} ({run["id"]})', f'run-{n}')
        for key, label in (('status', 'Status'), ('objective', 'Objective'), ('method', 'Method')):
            doc.paragraph(f'{tr(label)}: {tr(run[key]) if key == "status" else run[key]}')
        doc.paragraph(tr('Queries'))
        doc.items(run['queries'])
        positions = {source['id']: n for n, source in enumerate(selected.sources, 1)}
        doc.links('Sources', [(f'source-{positions[ident]}', f'{tr("Source")} {positions[ident]}')
                              for ident in run['source_ids']])
        doc.paragraph(tr('Limitations'))
        doc.items(run['limitations'])
    if selected.sources:
        doc.heading(2, tr('Sources'))
    for n, source in enumerate(selected.sources, 1):
        doc.heading(3, f'{tr("Source")} {n}: {source["title"]}', f'source-{n}')
        for key, label in (('id', 'Source ID'), ('platform', 'Platform'), ('source_type', 'Source type'),
                           ('published_at', 'Published'), ('accessed_at', 'Accessed'), ('language', 'Language'),
                           ('access', 'Access'), ('group_id', 'Discussion group')):
            value = source[key] if source[key] is not None else tr('unknown')
            if key in ('source_type', 'access'):
                value = tr(value)
            doc.paragraph(f'{tr(label)}: {value}')
        doc.paragraph(tr('Original URL'))
        if source['url']:
            doc.external_link(source['url'])
        else:
            doc.paragraph(tr('None supplied'))
        doc.paragraph(f'{tr("Context")}: {source["context"]}')
        if source['access'] in ('snippet', 'unavailable'):
            doc.paragraph(tr('Snippet or unavailable material cannot support findings.'))
        for m, excerpt in enumerate(source['excerpts'], 1):
            doc.heading(4, f'{tr("Excerpt")} {m} ({excerpt["id"]})', f'source-{n}-excerpt-{m}')
            doc.paragraph(f'{tr("Locator")}: {excerpt["locator"]}')
            doc.quotation(excerpt['text'])
        doc.paragraph(tr('Limitations'))
        doc.items(source['limitations'])


def interview_evidence(doc: Document, state: Study, selected: Selection) -> None:
    rec = state['recipe']
    tr = doc.tr
    people = {p['id']: p for p in state['personas']}
    anchors = {item['id']: f'interview-{index}' for index, item in enumerate(selected.interviews, 1)}
    person_anchors = {p['id']: f'persona-{index}' for index, p in enumerate(state['personas'], 1)}
    covered = len({i['persona_id'] for i in selected.interviews})
    doc.paragraph(f'{tr("Personas: stored / planned / covered by selected interviews")}: '
                  f'{len(people)} / {rec["persona_count"]} / {covered}')
    doc.heading(2, tr('Method'))
    doc.paragraph(f'{tr("Recipe")}: {rec["id"]}')
    doc.paragraph(f'{tr("Question")}: {rec["question"]}')
    doc.paragraph(rec['method'])
    doc.heading(3, tr('Dimensions'))
    doc.items(f'{d["name"]}: ' + ', '.join(d['values']) for d in rec['dimensions'])
    doc.heading(3, tr('Constraints'))
    doc.items(rec['constraints'])
    doc.heading(2, tr('Role cards'))
    selected_personas = {item['persona_id'] for item in selected.interviews}
    for p in state['personas']:
        if p['id'] not in selected_personas:
            continue
        doc.heading(3, f'{p["label"]} ({p["id"]})', person_anchors[p['id']])
        doc.paragraph(f'{tr("Recipe")}: {p["recipe_id"]}')
        doc.items(f'{k}: {val}' for k, val in p['traits'].items())
        doc.paragraph(tr('Attributes and assumptions'))
        doc.items(f'{a["name"]}: {a["value"]} [{tr(a["basis"])}] — {a["rationale"]}' for a in p['attributes'])
    doc.heading(2, tr('Full simulated transcripts'))
    for item in selected.interviews:
        doc.heading(3, f'{tr("Interview")}: {item["id"]}', anchors[item['id']])
        p = people[item['persona_id']]
        doc.links('Provenance', [(person_anchors[p['id']], f'{tr("Persona")}: {p["label"]} ({p["id"]})')])
        for n, turn in enumerate(item['turns'], 1):
            doc.heading(4, f'{tr("Turn")} {n}', f'turn-{anchors[item["id"]]}-{n}')
            doc.paragraph(f'{tr("Question")}: {turn["question"]}')
            doc.paragraph(f'{tr("Answer")}: {turn["answer"]}')
            doc.paragraph(tr('Assumptions'))
            doc.items(turn['assumptions'])


def evidence_document(state: Study, report: JSONObject, kind: str) -> str:
    """Retain selected source excerpts and complete interviews with exact anchors."""
    doc = report_document(state, report, kind)
    tr = doc.tr
    selected = Selection(state, report)
    doc.heading(1, report['title'] + ' — ' + tr('Evidence appendix'))
    if selected.interviews:
        doc.paragraph(tr('Synthetic research') + ': ' + tr('All personas and interviews are simulations. These are hypotheses, not evidence of real customer demand.'), notice=True)
    doc.paragraph(f'{tr("Status")}: {tr(report["status"])} | {tr("Revision")}: {state["revision"]}')
    brief = state.get('brief')
    if brief:
        doc.heading(2, tr('Brief'))
        doc.paragraph(f'{tr("Brief ID")}: {brief["id"]}')
        doc.paragraph(f'{tr("Question")}: {brief["question"]}')
        doc.paragraph(f'{tr("Language")}: {brief["language"]}')
        doc.paragraph(tr('Constraints'))
        doc.items(brief['constraints'])
    source_evidence(doc, selected)
    if selected.interviews:
        interview_evidence(doc, state, selected)
    return doc.finish()


def render(directory: PathInput, report: JSONValue, output_format: str) -> JSONObject:
    directory = Path(directory)
    with store.lock(directory):
        state = store.load(directory)
        v.report(report, state)
        report = cast(JSONObject, report)
        reports = directory / 'reports'
        reports.mkdir(exist_ok=True)
        numbers = [int(p.name) for p in reports.iterdir() if re.fullmatch(r'\d+', p.name)]
        number = max(numbers, default=0) + 1
        final = reports / f'{number:03d}'
        temporary = Path(tempfile.mkdtemp(prefix='.render-', dir=reports))
        try:
            store.write_json(temporary / 'study.json', state)
            store.write_json(temporary / 'report.json', report)
            formats = ('md', 'html') if output_format == 'both' else (output_format,)
            for kind in formats:
                for name, build in (('report', document), ('evidence', evidence_document)):
                    with (temporary / f'{name}.{kind}').open('w', encoding='utf-8') as handle:
                        handle.write(build(state, report, kind))
                        handle.flush()
                        os.fsync(handle.fileno())
            v.require(not final.exists(), f'Report directory already exists: {final}')
            os.rename(temporary, final)
        finally:
            if temporary.exists():
                shutil.rmtree(temporary)
    return {'ok': True, 'directory': str(final.resolve()), 'revision': state['revision'], 'formats': list(formats)}
