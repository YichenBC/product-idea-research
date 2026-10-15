# Social access routes for Codex and Claude Code

The skill uses the host's tools; it does not bundle or silently install a crawler.
Choose an available route and record its actual depth. Keep credentials in the host's
secret/configuration mechanism, never in evidence, commands, reports or the repository.

| Surface | Useful available routes | What to verify before claiming coverage |
|---|---|---|
| Reddit | Host web search + original thread; configured Reddit MCP/API; authorized browser | Original post, visible replies, comment permalinks, parent/author updates; pagination/more-comments omitted or expanded |
| X | Configured X search/thread MCP/API; authorized browser search + status page; search as lead discovery | Expand long posts, inspect quoted posts and replies, paid-partnership label, author follow-up; status ID survives handle changes |
| LinkedIn | Configured connector that actually exposes posts/comments; authorized browser; public post pages | Post body and comment layer separately; professional/vendor affiliation; chronological/relevance sorting; missing exact dates |
| Xiaohongshu | Configured source connector; authorized browser note + comment pane; user-authorized export | Original note, folded comments, author answers, promotional disclosure; search snippets cannot establish note access |
| Forums/reviews/tasks | Public pages, host connectors or user exports | Accepted answer, edit/resolved state, seller promotion, quoted price versus paid job, deleted/expired listing |

A provider name is not a capability guarantee. Inspect available tool schemas for
search/post/thread/replies and test a sample. Prefer the tool already available over
adding an integration. If a named connector is absent, search the host plugin catalog
when supported; a connector for managing one's own posts is not social discovery.
No matching result does not prove no such plugin exists elsewhere.

Browser guidance: use visible navigation and supported automation APIs, retain only
relevant public material, and respect the host's browser policy. A logged-in browser
can display public posts; do not access messages, connections lists, private groups
or harvest contacts. Do not automate follows, likes, comments, DMs or connection
requests. Access barriers stay explicit rather than being bypassed.

When a route fails, record platform, route, failure and which content remains unread.
Try a materially different authorized route where useful. Do not repeatedly retry
a blocked endpoint or report a whole platform unavailable based on one failed fetch.
For reproducible/offline work, import a supplied source batch under the same schema;
retaining provenance does not make supplied text independently verified.
