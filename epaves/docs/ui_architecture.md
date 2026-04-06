# UI Architecture

> AIStudio / urCrew — target state interface design  
> Left-bar navigation model. Incremental implementation against a stable target.

---

## Design Principles

- **Left bar, not ribbon** — AIStudio is a mode-switching app, not a 
  pipeline app. Users are always in one of: Chat, Corpus, Models, Settings, 
  Observability. The left bar reflects this.
- **Chat is home** — 90% of time is spent in the Chat panel. Everything 
  else is configuration and management.
- **Query controls are inline** — temperature, k, threshold, model, and 
  corpus selector live in the Chat panel footer, not buried in Settings.
- **Native OS file picker everywhere** — all file selection uses the browser's 
  `<input type="file">` element, triggering the native macOS Finder interface 
  with search, favorites, and recent files. No drag-and-drop required.
- **Conversation persistence by default** — conversations auto-save after 
  every exchange and restore on page load. Users never lose work on refresh.

---

## Layout Overview

```
┌─────────────────────────────────────────────────────────────────┐
│  [Icon Rail 48px] │ [Context Panel 240px] │ [Main Canvas]       │
└─────────────────────────────────────────────────────────────────┘
```

Three permanent zones:

1. **Icon Rail** — always visible, 48px wide, mode switcher
2. **Context Panel** — expands when icon is clicked, mode-specific controls
3. **Main Canvas** — primary work area, defaults to Chat

---

## Icon Rail

Top-to-bottom layout:

```
 💬  Chat           ← default home, primary mode
 📚  Corpus
 🤖  Models
 ─────────────      ← divider
 📊  Metrics
 🐛  Debug
 ─────────────      ← divider
 👥  Admin          ← visible to ADMIN / SUPER_ADMIN only
 ⚙️  Settings
 ❓  Help
 ─────────────      ← bottom-pinned
 👤  [avatar]       ← current user — click for profile / logout
```

---

## Context Panels

### 💬 Chat Panel

```
[ + New Chat                      ]   ← clears current, archives previous
[ 🔍 Search conversations...      ]
──────────────────────────────────
  Today
  › Q3 risk analysis
  › Agentic AI limitations
  Yesterday
  › Wellington prep notes
  Last Week
  › ...
──────────────────────────────────
[ 🗑  Clear all history           ]
```

**Alpha:** `+ New Chat` only, no history list  
**Beta:** Full history list with date grouping  
**v1.0:** Search across conversations  

---

### 📚 Corpus Panel

```
[ + New Corpus                    ]   ← native OS folder picker
──────────────────────────────────
  My Corpora
  › BOEI_test          [2 files]
  › Wellington_prep    [8 files]

  Shared with me                      ← future, multi-user
  › Team Research      [14 files]
──────────────────────────────────
[ + Upload Files                  ]   ← native OS file picker,
                                          adds to selected corpus
```

Clicking a corpus shows its detail view in the Main Canvas:
- File list with status (indexed / pending / error)
- Chunk count, last indexed timestamp
- Re-index button
- Delete corpus / remove individual files

---

### 🤖 Models Panel

```
[ + Add Model                     ]   ← triggers ollama pull in backend
──────────────────────────────────
  Loaded in RAM
  ● llama3.1:70b       42GB  ✓
  
  On Disk
  ○ llama3.1:8b         5GB
  ○ nomic-embed-text    274MB

  Available to Pull
  ○ deepseek-r1:70b    40GB
  ○ qwen2.5:72b        40GB
  ○ mixtral:8x22b      80GB
──────────────────────────────────
  Embedding Model
  ● nomic-embed-text   [change]
```

**Alpha:** Read-only list, model set via config  
**Beta:** Add / remove models via UI, set default  
**v1.0:** Pull progress indicator, RAM usage display  

---

### 📊 Metrics Panel

```
  This Session
  Queries:          12
  Avg latency:      11.2s
  Avg chunks used:  8.3
  Cache hits:       3

──────────────────────────────────
  All Time
  Total queries:    847
  Corpora:          4
  Files indexed:    23
  Tokens used:      1.2M

──────────────────────────────────
  [ Export metrics CSV ]
```

---

### 🐛 Debug Panel

Power-user / developer only. Shows for most recent query:

```
  Last Query
  ──────────────────────────────
  Prompt sent:      [expand]
  Retrieved chunks: [expand]
  Chunk scores:     0.91, 0.87, 0.84...
  Tokens (prompt):  1,240
  Tokens (completion): 312
  Latency:          11.2s
  
  [ Copy raw prompt ]
  [ Copy raw context ]
```

---

### 👥 Admin Panel *(ADMIN / SUPER_ADMIN only)*

```
[ + Invite User                   ]
[ + Create Team                   ]
──────────────────────────────────
  Users
  › Manuel Barbero    [owner]

  Teams
  › (none yet)
──────────────────────────────────
  Access Control
  › Corpus permissions
  › Conversation sharing
──────────────────────────────────
  Audit Log
  › View recent activity
```

---

### ⚙️ Settings Panel

```
  Defaults
  Model:        [ llama3.1:70b  ▼ ]
  Corpus:       [ BOEI_test     ▼ ]
  Temperature:  [ 0.7          ±  ]
  K:            [ 8            ±  ]
  Threshold:    [ 0.6          ±  ]

──────────────────────────────────
  Integrations
  › LiteLLM / cloud models
  › MCP connectors
  › Web search

──────────────────────────────────
  Storage
  Data path:    ~/Developer/AIStudio/data
  Vector DB:    Chroma (local)
  Conversations: 12    [ Export all ]

──────────────────────────────────
  Appearance
  Theme:        [ Light / Dark  ▼ ]

──────────────────────────────────
  About
  Version:      alpha-0.1
  [ Check for updates ]
  [ View changelog    ]
```

---

## Main Canvas — Chat View (Default)

```
┌─────────────────────────────────────────────────────────────────┐
│  Q3 Risk Analysis               [corpus: BOEI_test ▼]      [⚙] │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   [conversation thread]                                         │
│                                                                 │
│   User: What are the limitations of agentic AI?                 │
│                                                                 │
│   Assistant: Agentic AI faces several core limitations [1][4]   │
│   ...                                                           │
│                                                                 │
│   REFERENCES                                                    │
│   [1] agentic_ai_pov.pdf — p.4 · Open ↗                        │
│   [4] agentic_ai_pov.pdf — p.11 · Open ↗                       │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│  Model: [llama3.1:70b ▼]  Temp: [0.7]  K: [8]  T: [0.6]       │
│  [🌐 Web]  [📎 +File]                        Research: 11.2s    │
├─────────────────────────────────────────────────────────────────┤
│  [ Ask anything...                                    ] [Send]  │
└─────────────────────────────────────────────────────────────────┘
```

**Header:** Conversation title (auto-generated, editable) + corpus selector  
**Thread:** Scrollable message history with inline citations  
**Footer bar:** Inline query controls — always visible, no navigation required  
**Input:** Full-width, Enter to send, Shift+Enter for newline  

### Footer Bar Controls

| Control | Description | Release |
|---|---|---|
| Model selector | Switch LLM per query | Beta |
| Temp / K / Threshold | Inline sliders | Alpha |
| 🌐 Web toggle | Enable web search via LiteLLM/MCP | v1.0 |
| 📎 +File | Attach file to this query | Beta |
| Research: Xs | Latency telemetry | Beta |

---

## Main Canvas — Corpus Detail View

Activated by clicking a corpus in the Corpus panel:

```
┌─────────────────────────────────────────────────────────────────┐
│  BOEI_test                              [ Re-index ] [ Delete ] │
├─────────────────────────────────────────────────────────────────┤
│  42 chunks · 1 file · Last indexed: 2026-03-08                  │
│                                                                 │
│  Files                                                          │
│  ──────────────────────────────────────────────────────         │
│  📄 agentic_ai_pov.pdf    42 chunks   indexed ✓   [ Remove ]    │
│                                                                 │
│  [ + Add Files ]          ← native OS file picker               │
└─────────────────────────────────────────────────────────────────┘
```

---

## Conversation Persistence

### Alpha (current release target)
- Auto-save to `data/conversations/current.json` after every exchange
- Restore on page load — refresh never loses the conversation
- `+ New Chat` archives current conversation with timestamp, starts fresh
- Export current conversation as Markdown

### Beta
- Named conversation history in Chat panel (date-grouped)
- Click any past conversation to reopen
- Rename and delete conversations

### v1.0
- Search across all conversations
- Export all conversations as ZIP

### v2.0
- Shared conversations (multiple participants)
- Conversation permissions via Permission entity

---

## File Selection — OS Native Picker

All file operations use the HTML `<input type="file">` element:

```html
<!-- Single file -->
<input type="file" accept=".pdf,.docx,.pptx,.xlsx,.md">

<!-- Multiple files -->
<input type="file" multiple accept=".pdf,.docx,.pptx,.xlsx,.md">

<!-- Folder (corpus creation) -->
<input type="file" webkitdirectory>
```

This surfaces the native macOS Finder interface automatically — 
with search, favorites, recent files, and tag filtering. 
No custom drag-and-drop UI required.

---

## Release Phasing Summary

| Feature | Alpha | Beta | v1.0 | v2.0 |
|---|---|---|---|---|
| Chat with citations | ✅ | | | |
| Corpus selector in chat | ✅ | | | |
| Inline query controls | ✅ | | | |
| Conversation auto-save | ✅ | | | |
| Conversation history list | | ✅ | | |
| Model switcher in UI | | ✅ | | |
| Latency telemetry | | ✅ | | |
| +File attachment | | ✅ | | |
| Corpus detail view | | ✅ | | |
| Web search toggle | | | ✅ | |
| Conversation search | | | ✅ | |
| Admin panel | | | | ✅ |
| Shared conversations | | | | ✅ |
| Access control UI | | | | ✅ |
| MCP connectors | | | | ✅ |
