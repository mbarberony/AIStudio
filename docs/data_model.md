# Data Model

> AIStudio — target state schema  
> Designed for single-user today, multi-user ready from day one.

---

## Design Principles

- **Multi-user ready from day one** — every entity carries ownership fields 
  even if only one user exists today; no schema redesign needed to add users
- **Files are first-class** — a file lives once on disk and in the vector 
  store, but can belong to multiple corpora
- **Conversations are self-describing** — every message records which model 
  and corpus produced it, so history is always reproducible
- **JSON files today, Postgres tomorrow** — the schema maps cleanly to 
  relational tables with no redesign; migration is a one-time ETL script

---

## Entities

### Corpus
```json
{
  "corpus_id": "uuid",
  "name": "string (slug, e.g. 'my_corpus')",
  "display_name": "string",
  "created_by": "user_id",
  "file_ids": ["uuid"],
  "status": "active | indexing | error",
  "created_at": "iso8601",
  "updated_at": "iso8601"
}
```

---

### File
```json
{
  "file_id": "uuid",
  "filename": "string",
  "filepath": "string (relative to repo root)",
  "file_hash": "string (sha256 — detect duplicates, avoid re-indexing)",
  "corpus_ids": ["uuid"],
  "mime_type": "string",
  "size_bytes": 0,
  "chunk_count": 0,
  "status": "indexed | pending | error",
  "error_message": "string | null",
  "uploaded_by": "user_id",
  "ingested_at": "iso8601"
}
```

Key design decision: corpus_ids [] is a many-to-many relationship — 
a file lives once on disk and is indexed once into the vector store, but 
can be tagged to multiple corpora. file_hash detects duplicates.

---

### Conversation
```json
{
  "conversation_id": "uuid",
  "title": "string (auto-generated from first query, editable)",
  "created_by": "user_id",
  "corpus_id": "uuid (active corpus when conversation started)",
  "model": "string (active model when conversation started)",
  "status": "active | archived | deleted",
  "tags": ["string"],
  "created_at": "iso8601",
  "updated_at": "iso8601",
  "messages": ["message_id"]
}
```

---

### Message
```json
{
  "message_id": "uuid",
  "conversation_id": "uuid",
  "author": "user_id | 'assistant'",
  "role": "user | assistant | system",
  "content": "string",
  "citations": [
    {
      "chunk_id": "string",
      "source": "string (filename)",
      "score": 0.87,
      "passage": "string (excerpt)"
    }
  ],
  "model": "string (which model generated this response)",
  "corpus_id": "uuid (which corpus was active for this message)",
  "tokens_used": {
    "prompt": 1240,
    "completion": 312
  },
  "created_at": "iso8601"
}
```

corpus_id and model are recorded per message because they can change 
mid-conversation. Every message is self-describing — history is always 
reproducible without external context.

---

### Model
```json
{
  "model_id": "uuid",
  "name": "string (e.g. 'llama3.1:70b')",
  "provider": "ollama | openai | anthropic | mistral | litellm",
  "type": "llm | embedding",
  "status": "available | downloading | unavailable",
  "size_gb": 0.0,
  "is_default": false,
  "added_at": "iso8601"
}
```

---

## Relationships

```
Corpus
 └── references → Files [] (via file_ids)

File
 └── belongs to → Corpora [] (via corpus_ids — many-to-many)

Conversation
 └── contains → Messages []

Message
 ├── belongs to → Conversation
 └── cites → File chunks []
```

---

## Storage Layout

```
data/
  conversations/
    {conversation_id}.json    <- includes messages[] inline
    current.json              <- active conversation (auto-saved)
  corpora/
    {corpus_id}/
      meta.json               <- corpus metadata
      files/
        {file_id}.json        <- per-file metadata
  models/
    registry.json             <- all known models and their status
```

---

## Multi-User Extension (Future)

When multi-user support is added, two entities join the schema:

User — user_id, display_name, email, role, preferences
Permission — resource_type, resource_id, granted_to, level

Every entity already carries a created_by: user_id field.
Adding users requires populating that field, not restructuring the schema.

---

## Migration Path to Relational DB

| JSON field | Relational table |
|---|---|
| file.corpus_ids[] | corpus_files(corpus_id, file_id) |
| conversation.messages[] | messages table with conversation_id FK |
| message.citations[] | citations table with message_id FK |

No schema redesign required — migration is a one-time ETL script.
