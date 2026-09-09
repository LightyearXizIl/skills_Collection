---
name: cut-motion
description: Use the cut-motion Agent workflow to turn local talking-head footage into tightly edited videos with transcription, rough-cut review, subtitles or motion copy, HyperFrames/GSAP motion graphics, validation, rendering, and revision. Trigger when the user asks to use cut-motion, produce an edited talking-head video through an Agent workflow, or continue an existing cut-motion job.
---

# Cut Motion

Use the bundled upstream runtime as a reproducible video-production workspace. It is a workflow repository adapted into a Codex Skill; the canonical editing rules remain upstream's `AGENTS.md`.

## Start or resume work

1. For any task that will inspect, edit, render, or revise media, read `assets/runtime/AGENTS.md` completely before acting. Then read only the mode-specific documents it directly requires.
2. Never place user media, job state, dependencies, logs, or renders inside this Skill directory.
3. If the user already has a cut-motion checkout or job, work there and preserve its current state.
4. Otherwise create an isolated workspace by running:

   ```bash
   python scripts/prepare_workspace.py /absolute/path/to/new-workspace
   ```

   The helper refuses to overwrite a non-empty destination. After copying, work from the new workspace and treat its `AGENTS.md` as authoritative.
5. A local talking-head video path is the only required input. If it is missing, ask for it and stop. Ask once for any known preferences, but do not block when the user has none.

## Preserve the workflow contract

- Keep the source video immutable and keep each job isolated under `jobs/<job-id>/`.
- Use the nine-state workflow and `scripts/workflow-state.mjs`; never infer approval, completion, or a passed check.
- Default to `review`. Pause only at `rough-cut-review`, and do not treat silence as approval. Use `auto` only when the user explicitly requests it and explain that its validation and repair may take longer.
- Keep ChatCut limited to the editable rough cut. Use FFmpeg/FFprobe for media operations and HyperFrames for released captions, motion graphics, composition, and rendering.
- Inspect ChatCut from the active Agent tool surface; shell detection is not reliable. If unavailable, record and disclose the conservative FFmpeg fallback rather than claiming ChatCut ran.
- Obtain explicit approval before installing dependencies, enabling plugins, starting authentication, or downloading the required font. Follow the bundled preflight instructions exactly.
- On Windows, use WSL2 or an equivalent Unix shell. Invoke shell files with `bash scripts/<name>.sh` when executable-bit behavior is uncertain.
- Report structural media checks separately from editorial or aesthetic approval. A valid file is not proof that the edit looks good.
- Revisions stay in the same job and reopen the earliest affected state. Preserve the last known-good artifacts as required by the upstream protocol.

## Bundled source

The runtime is pinned for reproducibility. Read `references/upstream.md` when checking provenance, license boundaries, or whether the bundled revision is current. Do not silently update or replace it during a video job.
