# ShuYou Mintlify Docs

Documentation site for ShuYou AI APIs, structured similar to [EvoLink API Manual](https://docs.evolink.ai/en/api-manual/image-series/nanobanana/nanobanana-2-image-generate).

## Structure

```
en/ | zh/
├── api-reference/           # API reference (Evolink-style)
│   ├── language-series/  # OpenAI, Anthropic, Vertex AI
│   ├── image-series/     # Image generation (OpenAPI + playground)
│   ├── video-series/     # Veo, Seedance, …
│   ├── file-series/      # OpenAI-compatible Files API
│   ├── task-management/  # Async jobs, get generation
│   ├── account-management/
├── guide/                # Integration & user guides
docs.json                 # Navigation, redirects, theme
openapi.json              # Shared OpenAPI (legacy aggregate)
```

OpenAPI-driven API pages use a paired `.json` + `.mdx` under `api-reference/`:

```mdx
---
title: Upload File
openapi: en/api-reference/file-series/upload-stream.json POST /v1/files
---

> - Bullet intro (left column)
> - Interactive **Try it** + cURL + response (right column, from OpenAPI)
```

Long-form field docs live in `*-reference.mdx` files (linked from the playground page, not in the sidebar).

## Local preview

```bash
npx mintlify@latest dev
```

Run from the repository root.
