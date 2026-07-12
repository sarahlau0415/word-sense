# Word Sense

Word Sense is a small static prototype for exploring how English words work in real usage, especially for Chinese adult English learners.

The page focuses on:

- a word search input
- optional source and original sentence fields
- sense-specific explanations
- examples across workplace, daily conversation, and social media contexts

The current public Word Sense site runs on a VPS at `wordsense.sarahliu.fun`. The old Netlify serverless prototype is no longer used.

## Preview Locally

Open `index.html` directly in a browser to preview the static UI.

Model generation is handled by the VPS-backed Word Sense server, not by Netlify Functions.

## Environment Variables

Set these on the VPS/service environment:

- `OPENAI_API_KEY`: required
- `OPENAI_BASE_URL`: optional OpenAI-compatible endpoint
- `OPENAI_MODEL`: optional

## Check Syntax

```bash
npm run check
```

## Validate The Product

The folder `validation/` contains the operating project for testing Word Sense across usage, growth, and business viability. Start with:

- `validation/product-diagnosis.md`
- `validation/hypotheses.md`
- `validation/test-plan.md`
- `validation/content-quality-rubric.md`

The backend prompt in `lib/generate-sense.js` is aligned with the six-dimension Word Sense v2 structure: 字面、感觉、来历、用法、跟中文比、悟道时刻.

## Publish To Production

Production runs from the VPS-backed Word Sense server at `wordsense.sarahliu.fun`.

For a full issue release—not only a code deploy—follow `word-sense-workflow/05-issue-release-workflow.md`. It covers required `surface` metadata, homepage/current-archive identity, cache versioning, visual screenshots, and public no-cache verification.

Before release:

1. Merge the prepared release branch into `main`.
2. Push `main` to GitHub.
3. Pull the latest `main` on the VPS.
4. Restart the Word Sense server process.
5. Check `/index.html`, `/word-sense-review.html`, and a generated `/word-sense-entry.html?word=...` page.

## Latest Fixes

- 2026-05-31: Mobile visitors no longer see the redesign notice by default; the origin index slip now scales long headwords so they stay inside the paper label.

## Legacy Hosting Notes

Netlify is no longer used for this product. The remaining `netlify.toml` exists only to skip accidental builds if an old Netlify site is still connected to this repository.

GitHub Pages can host a static UI preview, but it cannot run the VPS job API. Vercel-related files are retained only as legacy prototype code.

## Project Files

- `index.html`: the index wall and search entry point
- `word-sense-entry.html`: the standalone word dossier reading page
- `api/sense.js`: legacy Vercel serverless prototype endpoint
- `lib/generate-sense.js`: shared OpenAI generation logic
- `netlify.toml`: legacy Netlify build skip guard
- `package.json`: project metadata and syntax check script
- `README.md`: project overview and publishing notes
