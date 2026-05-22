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

## Netlify status

Netlify is no longer used for this product. The remaining `netlify.toml` exists only to skip accidental builds if an old Netlify site is still connected to this repository.

## Publish With Vercel

GitHub Pages can host the static page, but it cannot run `/api/sense`. Vercel is another good option if your account can deploy there.

1. Import this GitHub repository into Vercel.
2. Add `OPENAI_API_KEY` in the Vercel project environment variables.
3. Deploy.
4. Share the Vercel URL.

## Publish Static Preview With GitHub Pages

1. Create a new GitHub repository.
2. Push this folder to the repository.
3. Open the repository settings.
4. Go to Pages.
5. Set the source to `Deploy from a branch`.
6. Choose the `main` branch and `/root`.
7. Save and wait for GitHub to generate the public URL.

GitHub Pages is only useful for the UI preview unless `/api/sense` is hosted somewhere else.

## Project Files

- `index.html`: the full static UI
- `api/sense.js`: Vercel serverless model endpoint
- `lib/generate-sense.js`: shared OpenAI generation logic
- `netlify.toml`: legacy Netlify build skip guard
- `package.json`: project metadata and syntax check script
- `README.md`: project overview and publishing notes
