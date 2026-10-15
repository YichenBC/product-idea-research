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

    def finish(self) -> str:
        return '\n\n'.join(self.parts) + ('\n</body></html>\n' if self.kind == 'html' else '\n')


def document(state: Study, report: JSONObject, kind: str) -> str:
    """Keep the primary reading path focused on conclusions and decisions."""
    rec = state['recipe']
    doc = Document(kind, report['title'], rec['language'].lower().startswith('zh'))
    tr = doc.tr
    selected = selected_interviews(state, report)
    positions = {item['id']: index for index, item in enumerate(selected, 1)}
    doc.heading(1, report['title'])
    doc.paragraph(tr('Interview evidence is simulated; conclusions remain hypotheses for real-world validation.'), notice=True)
    doc.heading(2, tr('Summary'))
    doc.paragraph(report['summary'])
    doc.paragraph(f'{tr("Question")}: {rec["question"]}')
    doc.paragraph(f'{tr("Status")}: {tr(report["status"])}')
    covered = len({i['persona_id'] for i in selected})
    doc.paragraph(f'{tr("Selected interviews / personas covered / planned")}: '
                  f'{len(selected)} / {covered} / {rec["persona_count"]}')
    doc.heading(2, tr('Findings'))
    for n, finding in enumerate(report['findings'], 1):
        doc.heading(3, f'{n}. {finding["statement"]}', f'finding-{n}')
        for key, label in (('support', 'Support'), ('counterevidence', 'Counterevidence')):
            doc.links(label, [(f'turn-interview-{positions[r["interview_id"]]}-{r["turn"]}',
                              f'{tr("Interview")} {positions[r["interview_id"]]} · {tr("Turn")} {r["turn"]}')
                             for r in finding[key]], filename=f'evidence.{kind}')
        doc.paragraph(tr('Limitations'))
        doc.items(finding['limitations'])
    doc.heading(2, tr('Real-world next steps'))
    doc.items(report['next_steps'])
    doc.heading(2, tr('Limitations'))
    doc.items(report['limitations'])
    return doc.finish()


def selected_interviews(state: Study, report: JSONObject) -> list[JSONObject]:
    interviews = {i['id']: i for i in state['interviews']}
    return [interviews[i] for i in report['interview_ids']]


def evidence_document(state: Study, report: JSONObject, kind: str) -> str:
    """Retain complete selected research material behind exact-turn citations."""
    rec = state['recipe']
    doc = Document(kind, report['title'], rec['language'].lower().startswith('zh'))
    tr = doc.tr
    selected = selected_interviews(state, report)
    people = {p['id']: p for p in state['personas']}
    anchors = {item['id']: f'interview-{index}' for index, item in enumerate(selected, 1)}
    person_anchors = {p['id']: f'persona-{index}' for index, p in enumerate(state['personas'], 1)}
    doc.heading(1, report['title'] + ' — ' + tr('Evidence appendix'))
    doc.paragraph(tr('Synthetic research') + ': ' + tr('All personas and interviews are simulations. These are hypotheses, not evidence of real customer demand.'), notice=True)
    doc.paragraph(f'{tr("Status")}: {tr(report["status"])} | {tr("Revision")}: {state["revision"]}')
    covered = len({i['persona_id'] for i in selected})
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
    selected_personas = {item['persona_id'] for item in selected}
    for p in state['personas']:
        if p['id'] not in selected_personas:
            continue
        doc.heading(3, f'{p["label"]} ({p["id"]})', person_anchors[p['id']])
        doc.paragraph(f'{tr("Recipe")}: {p["recipe_id"]}')
        doc.items(f'{k}: {val}' for k, val in p['traits'].items())
        doc.paragraph(tr('Attributes and assumptions'))
        doc.items(f'{a["name"]}: {a["value"]} [{tr(a["basis"])}] — {a["rationale"]}' for a in p['attributes'])
    doc.heading(2, tr('Full simulated transcripts'))
    for item in selected:
        doc.heading(3, f'{tr("Interview")}: {item["id"]}', anchors[item['id']])
        p = people[item['persona_id']]
        doc.links('Provenance', [(person_anchors[p['id']], f'{tr("Persona")}: {p["label"]} ({p["id"]})')])
        for n, turn in enumerate(item['turns'], 1):
            doc.heading(4, f'{tr("Turn")} {n}', f'turn-{anchors[item["id"]]}-{n}')
            doc.paragraph(f'{tr("Question")}: {turn["question"]}')
            doc.paragraph(f'{tr("Answer")}: {turn["answer"]}')
            doc.paragraph(tr('Assumptions'))
            doc.items(turn['assumptions'])
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
