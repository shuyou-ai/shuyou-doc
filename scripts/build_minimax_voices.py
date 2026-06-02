#!/usr/bin/env python3
"""Generate MiniMax speech-2.8-hd voice docs from voices.tsv."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TSV = ROOT / "en/api-reference/audio-series/minimax/voices.tsv"
LANG_JSON = ROOT / "en/api-reference/audio-series/minimax/languages.json"
OUT_JSON = ROOT / "en/api-reference/audio-series/minimax/speech-2.8-hd-voices.json"


def parse_tsv(text: str) -> list[dict]:
    rows = []
    for line in text.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) < 4:
            continue
        rows.append({
            "no": int(parts[0]),
            "language": parts[1],
            "voice_id": parts[2],
            "voice_name": parts[3],
        })
    return rows


def mdx_table(rows: list[dict], lang_col: str, name_col: str = "Voice name") -> str:
    lines = [
        f"| # | {lang_col} | `voice` | {name_col} |",
        "| --- | --- | --- | --- |",
    ]
    for r in rows:
        lines.append(
            f"| {r['no']} | {r['language']} | `{r['voice_id']}` | {r['voice_name']} |"
        )
    return "\n".join(lines)


def mdx_language_section(languages: list[str], locale: str) -> str:
    if locale == "zh":
        header = """## 语种参数（`input.language`）

可选。对应 MiniMax **`language_boost`**，用于增强指定语种或方言的合成效果。省略或传 **`auto`** 时由模型自动检测。

| `language` | 说明 |
| --- | --- |
| `Chinese` | 普通话 |
| `Chinese,Yue` | 粤语（勿使用 `Cantonese`） |
"""
        tail = "\n".join(f"| `{v}` | — |" for v in languages if v not in ("Chinese", "Chinese,Yue"))
        tip = """
<Tip>
合成粤语文本时，请显式设置 `language` 为 `Chinese,Yue`，并选用粤语音色（如 `Cantonese_*`）。
</Tip>
"""
    else:
        header = """## Language (`input.language`)

Optional. Maps to MiniMax **`language_boost`** to improve synthesis for a target language or dialect. Omit or set **`auto`** for automatic detection.

| `language` | Notes |
| --- | --- |
| `Chinese` | Mandarin Chinese |
| `Chinese,Yue` | Cantonese (do not use `Cantonese`) |
"""
        tail = "\n".join(f"| `{v}` | — |" for v in languages if v not in ("Chinese", "Chinese,Yue"))
        tip = """
<Tip>
For Cantonese text, set `language` to `Chinese,Yue` and pick a Cantonese voice preset (e.g. `Cantonese_*`).
</Tip>
"""
    return header + tail + "\n" + tip + "\n"


def language_openapi_property(languages: list[str], locale: str) -> str:
    enum_lines = ",\n".join(f'              "{v}"' for v in languages)
    enum_block = f"[\n{enum_lines}\n            ]"
    if locale == "zh":
        desc = (
            "合成语种/方言增强（对应 MiniMax `language_boost`）。可选；省略或传 `auto` 时自动检测。"
            "普通话用 `Chinese`，粤语用 `Chinese,Yue`。"
        )
    else:
        desc = (
            "Language or dialect boost (maps to MiniMax `language_boost`). Optional; omit or use `auto` "
            "for auto-detection. Use `Chinese` for Mandarin and `Chinese,Yue` for Cantonese."
        )
    return (
        '          "language": {\n'
        '            "type": "string",\n'
        f'            "description": {json.dumps(desc, ensure_ascii=False)},\n'
        '            "example": "auto",\n'
        f'            "enum": {enum_block}\n'
        "          }"
    )


def fix_model_schema(content: str) -> str:
    model_block = (
        '          "model": {\n'
        '            "type": "string",\n'
        '            "description": "Model ID. Use `speech-2.8-hd` for this endpoint.",\n'
        '            "default": "speech-2.8-hd",\n'
        '            "example": "speech-2.8-hd"\n'
        '          }'
    )
    return re.sub(
        r'"model":\s*\{.*?\n\s*\},\n(\s*)"function"',
        model_block + ',\n\\1"function"',
        content,
        count=1,
        flags=re.DOTALL,
    )


def fix_voice_schema(content: str, desc: str) -> str:
    voice_block = (
        '          "voice": {\n'
        '            "type": "string",\n'
        f'            "description": {json.dumps(desc, ensure_ascii=False)},\n'
        '            "example": "English_Graceful_Lady"\n'
        "          }"
    )
    return re.sub(
        r'"voice":\s*\{.*?\n\s*\}',
        voice_block,
        content,
        count=1,
        flags=re.DOTALL,
    )


def main():
    rows = parse_tsv(TSV.read_text(encoding="utf-8"))
    languages = json.loads(LANG_JSON.read_text(encoding="utf-8"))
    OUT_JSON.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    voice_ids = [r["voice_id"] for r in rows]

    en_mdx = ROOT / "en/api-reference/audio-series/minimax/speech-2.8-hd-generate.mdx"
    zh_mdx = ROOT / "zh/api-reference/audio-series/minimax/speech-2.8-hd-generate.mdx"
    en_json = ROOT / "en/api-reference/audio-series/minimax/speech-2.8-hd-generate.json"
    zh_json = ROOT / "zh/api-reference/audio-series/minimax/speech-2.8-hd-generate.json"

    en_front = """---
title: MiniMax Speech 2.8 HD
description: Create asynchronous text-to-speech tasks with speech-2.8-hd via POST /v1/predictions (function audio).
openapi: en/api-reference/audio-series/minimax/speech-2.8-hd-generate.json POST /v1/predictions
---

## Voice presets (`input.voice`)

Pass the **voice ID** in `input.voice` (maps to MiniMax `voice_id`). The table lists **327** system voices.

"""
    zh_front = """---
title: MiniMax Speech 2.8 HD 语音合成
description: 通过 POST /v1/predictions（function 为 audio）使用 speech-2.8-hd 创建异步文本转语音任务。
openapi: zh/api-reference/audio-series/minimax/speech-2.8-hd-generate.json POST /v1/predictions
---

## 音色参数（`input.voice`）

在 `input.voice` 中传入**音色 ID**（对应 MiniMax `voice_id`）。下表共 **327** 个系统音色。

"""
    en_tail = """

<Info title="Custom voices">
Custom `voice_id` strings (up to 64 characters) are supported when voice cloning is enabled on your account.
</Info>

## Optional parameters

| Field | Type | Description |
| --- | --- | --- |
| `speed` | number | Speed `0.5`–`2.0`, default `1` |
| `volume` | number | Volume `0`–`10`, default `1` |
| `pitch` | integer | Pitch `-12`–`12` semitones, default `0` |
| `emotion` | string | e.g. `happy`, `sad`, `calm`, `neutral`, `fluent` |
| `format` | string | `mp3`, `wav`, `flac`, or `pcm` (default `mp3`) |
| `language` | string | Language boost — see **Language** section (`auto`, `Chinese`, `Chinese,Yue`, …) |
| `english_normalization` | boolean | Normalize English numbers/dates for speech |
"""
    zh_tail = """

<Info title="自定义音色">
开通克隆能力后，也可使用最长 64 字符的自定义 `voice_id`。
</Info>

## 可选参数

| Field | Type | Description |
| --- | --- | --- |
| `speed` | number | 语速 `0.5`–`2.0`，默认 `1` |
| `volume` | number | 音量 `0`–`10`，默认 `1` |
| `pitch` | integer | 音调 `-12`–`12` 半音，默认 `0` |
| `emotion` | string | 如 `happy`、`sad`、`calm`、`neutral`、`fluent` |
| `format` | string | 输出格式：`mp3`、`wav`、`flac`、`pcm`（默认 `mp3`） |
| `language` | string | 语种增强，见上文 **语种参数**（`auto`、`Chinese`、`Chinese,Yue` 等） |
| `english_normalization` | boolean | 英文数字/日期朗读规范化 |
"""

    en_mdx.write_text(
        en_front
        + mdx_table(rows, "Language", "Voice name")
        + "\n\n"
        + mdx_language_section(languages, "en")
        + "\n"
        + en_tail,
        encoding="utf-8",
    )
    zh_mdx.write_text(
        zh_front
        + mdx_table(rows, "语言", "音色名称")
        + "\n\n"
        + mdx_language_section(languages, "zh")
        + "\n"
        + zh_tail,
        encoding="utf-8",
    )

    for path in (en_json, zh_json):
        content = path.read_text(encoding="utf-8")
        desc_en = (
            "MiniMax voice preset ID (maps to `voice_id`). Pass the ID exactly as in the voice table "
            f"on this page ({len(voice_ids)} presets). Example: `English_Graceful_Lady`."
        )
        desc_zh = (
            f"MiniMax 音色预设 ID（对应 `voice_id`）。请按本页音色表原样传入（共 {len(voice_ids)} 个）。"
            "示例：`English_Graceful_Lady`。"
        )
        desc = desc_zh if "/zh/" in str(path) else desc_en
        content = fix_model_schema(content)
        content = fix_voice_schema(content, desc)
        locale = "zh" if "/zh/" in str(path) else "en"
        lang_prop = language_openapi_property(languages, locale)
        content = re.sub(
            r'"language_boost":\s*\{[^}]*\}',
            lang_prop.strip(),
            content,
            count=1,
        )
        path.write_text(content, encoding="utf-8")

    print(f"OK: {len(rows)} voices, {len(languages)} languages")


if __name__ == "__main__":
    main()
