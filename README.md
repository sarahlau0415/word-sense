# Word Sense

Word Sense is a small static prototype for exploring how English words work in real usage, especially for Chinese adult English learners.

The page focuses on:

- a word search input
- optional source and original sentence fields
- sense-specific explanations
- examples across workplace, daily conversation, and social media contexts

This is currently a serverless-ready prototype. The front end calls `/api/sense`, a small backend function that uses the OpenAI Responses API to generate Word Sense explanations. The built-in examples include `shot`, `pristine`, `sweet`, and `agency` as a fallback/demo path.

## Preview Locally

Open `index.html` directly in a browser to preview the static UI.

Model generation requires a deployed serverless environment with `OPENAI_API_KEY` set. The local `file://` preview cannot call `/api/sense`.

## Environment Variables

Set these in Vercel:

- `OPENAI_API_KEY`: required
- `OPENAI_MODEL`: optional, defaults to `gpt-5.2`

## Check Syntax

```bash
npm run check
```

## Publish With Netlify

Use Netlify when you want friends to enter any word and receive generated results.

1. Import this GitHub repository into Netlify.
2. Leave the build command empty.
3. Set the publish directory to `.` if Netlify asks.
4. Add `OPENAI_API_KEY` in the Netlify project environment variables.
5. Deploy.
6. Share the Netlify URL.

The file `netlify.toml` routes `/api/sense` to the Netlify function automatically.

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
- `netlify/functions/sense.js`: Netlify serverless model endpoint
- `lib/generate-sense.js`: shared OpenAI generation logic
- `netlify.toml`: Netlify routing and publish settings
- `package.json`: project metadata and syntax check script
- `README.md`: project overview and publishing notes
