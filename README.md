# FormSaathi frontend

A responsive Next.js App Router frontend prototype for a voice-first Indian government service guide.

## Requirements
- Node.js 20.9 or newer
- npm

## Run locally
```bash
npm install
npm run dev
```
Open http://localhost:3000.

## Included
- Home page, service directory, service detail pages, assistant and about page
- Browser speech recognition where supported
- Speech synthesis for reading responses aloud
- Text-based assistant demo responses (not connected to a real AI service)
- Searchable government-service directory
- Document checklist saved in localStorage
- Responsive layout

## Important demo limitations
The assistant uses sample responses. It is not connected to a government database or an AI API. Check scheme eligibility, required documents, fees and application links on the relevant official government portal before applying. The browser's speech recognition support varies by browser, operating system and language.

## Connect a real AI service
Create a server-side API route (for example `src/app/api/chat/route.ts`) and call your AI provider from that route. Keep API keys on the server in environment variables. Do not expose secrets in client-side code.
