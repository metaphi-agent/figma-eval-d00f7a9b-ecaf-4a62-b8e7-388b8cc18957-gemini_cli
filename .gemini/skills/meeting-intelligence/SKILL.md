---
name: meeting-intelligence
description: Transcribes and analyzes meeting recordings, calls, and interviews. Use when user uploads audio/video files or asks to transcribe, analyze, or extract insights from meetings.
---

# Meeting Intelligence Pipeline

## Tools

| Tool | Function |
|------|----------|
| `Bash` | Run cache check/write scripts |
| `mcp__audio_processing__extract_audio` | Video to audio |
| `mcp__audio_processing__chunk_audio` | Split audio >20min |
| `mcp__google_stt__transcribe_audio` | Audio to transcript (returns GCS URI) |
| `mcp__gemini_large_file__analyze_multiple_files` | Analyze transcripts |

## Workflow

### 0. Check Cache (MANDATORY FIRST STEP)

```bash
python {skill_dir}/scripts/check_manifest.py {project_root}/meeting-intelligence/manifest.json {video_uri}
```

- If `CACHED:[...]` → Parse transcript URIs from JSON array, **skip to step 5**
- If `NOT_CACHED:*` → Continue to step 1

This prevents re-running $0.50+ / 20+ minute transcription on follow-up requests.

### 1. Confirm Language

Ask the user what language is spoken. Map to BCP-47 code from [LANGUAGE_CODES.md](LANGUAGE_CODES.md).

**Common codes:** en-US, en-IN, hi-IN, ta-IN, es-ES, fr-FR, de-DE, ja-JP, cmn-Hans-CN

### 2. Extract Audio (if video)

```
mcp__audio_processing__extract_audio(gcs_uri, output_format="flac")
→ {audio_uri, duration_seconds}
```

### 3. Chunk (if duration > 1200s)

```
mcp__audio_processing__chunk_audio(audio_uri, chunk_minutes=19, overlap_seconds=30)
→ {chunks: [{uri, index, start_seconds, duration_seconds}, ...]}
```

### 4. Transcribe

For each chunk (can run in parallel):

```
mcp__google_stt__transcribe_audio(gcs_uri, language, encoding="FLAC", sample_rate=16000)
→ {transcript_uri, word_count}
```

Collect all `transcript_uri` values for step 5.

### 5. Persist Cache (MANDATORY AFTER TRANSCRIPTION)

```bash
python {skill_dir}/scripts/write_manifest.py \
  {project_root}/meeting-intelligence/manifest.json \
  {video_uri} \
  {audio_uri} \
  {language} \
  {duration_seconds} \
  {total_word_count} \
  {transcript_uri_1} {transcript_uri_2} ...
```

### 6. Generate HTML Transcript Preview

Generate an HTML page with the raw transcript in the original language (e.g., Tamil, Hindi). Processes GCS URIs directly without loading text into agent context:

```bash
python {skill_dir}/scripts/generate_html_preview.py \
  gs://metaphi-ai/previews/{task_id}/transcript.html \
  "{meeting_title}" \
  {language} \
  {duration_minutes} \
  {transcript_uri_1} {transcript_uri_2} ...
```

Output: `SUCCESS:<signed_url>` - Share this signed URL with the user (valid for 7 days).

### 7. Translate with Gemini (if non-English)

For non-English transcripts, generate full English translation (saved to GCS):

```
mcp__gemini_large_file__analyze_multiple_files(
  gcs_uris=[transcript_uri_1, transcript_uri_2, ...],
  prompt="Translate this transcript to English. Preserve all content, speaker turns, and timestamps. Output the complete translated transcript.",
  output_gcs_uri="gs://metaphi-ai/tool-results/{task_id}/translation.txt"
)
→ {output_uri, summary, char_count, word_count}
```

### 8. Analyze with Gemini

```
mcp__gemini_large_file__analyze_multiple_files(
  gcs_uris=[transcript_uri_1, transcript_uri_2, ...],
  prompt="Analyze this meeting transcript and provide:
    - Executive summary (2-3 paragraphs)
    - Key discussion points with context
    - Action items with owners and deadlines
    - Decisions made
    - Important quotes with timestamps",
  output_gcs_uri="gs://metaphi-ai/tool-results/{task_id}/analysis.txt"
)
→ {output_uri, summary, char_count, word_count}
```

### 9. Update Manifest with Outputs

```bash
python {skill_dir}/scripts/update_manifest.py \
  {project_root}/meeting-intelligence/manifest.json \
  --translation_uri {translation_output_uri} \
  --analysis_uri {analysis_output_uri}
```

## Quality Standards

Analysis should be:
- **Specific**: Names, numbers, dates, commitments
- **Actionable**: Clear next steps with owners
- **Evidence-backed**: Cite quotes with timestamps

## Edge Cases

- **Cache hit but different analysis needed**: Use cached transcript_uris, run new Gemini prompt
- **Single chunk**: Still use `analyze_multiple_files` (works with one file)
- **Gemini fails**: Use `analyze_large_file` on each transcript individually
