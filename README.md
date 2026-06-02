# ShuYou Mintlify Docs

Documentation site for ShuYou AI APIs, structured similar to [EvoLink API Manual](https://docs.evolink.ai/en/api-manual/image-series/nanobanana/nanobanana-2-image-generate).

## Structure

```
en/ | zh/
├── api-manual/           # API reference (Evolink-style)
│   ├── language-series/  # OpenAI, Anthropic, Vertex AI
│   ├── image-series/     # Image generation (OpenAPI + playground)
│   ├── video-series/     # Veo, Seedance, …
│   ├── file-series/      # OpenAI-compatible Files API
│   ├── task-management/  # Async jobs, get generation
│   ├── account-management/
│   └── platform-management/
├── guide/                # Integration & user guides
docs.json                 # Navigation, redirects, theme
openapi.json              # Shared OpenAPI (legacy aggregate)
```

OpenAPI-driven endpoints use a paired `.json` + `.mdx` under `api-manual/` (see `image-series/gemini/gemini-flash-image-generate`).

## Local preview

```bash
npx mintlify@latest dev
```

Run from the repository root.
