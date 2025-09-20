# Ka-ching! Frontend

Arcade-styled Cornell-themed UI for the Ka-ching productivity game. Built with React + Vite + TypeScript.

## Run locally

```bash
cd frontend
npm install
npm run dev
```

If npm isn’t found, install Node.js LTS and restart the shell.

## Environment

Create a `.env` file in `frontend/`:

```
VITE_BACKEND_URL=http://localhost:5000   # Flask mongoapi (calendar upload/events)
VITE_CORE_URL=http://localhost:8000      # Core gamification API (tasks/xp/levels)
VITE_MCP_URL=http://localhost:7000       # MCP AI orchestrator (Gemini → YouTube/Podcasts)
```

## Integration points

- Tycoon ranking: `src/services/api.ts` → `api.tycoon.rankTask` (invoked from `src/pages/Dashboard.tsx` when tasks are added).
- Core gamification: `api.tasks.create|complete`, `api.users.getXp` used for XP/level/streak bar.
- Calendar (Flask mongoapi): `api.calendar.upload` (POST /upload), `api.calendar.fetch` (GET /events/:user_id).
- MCP media search: `api.media.search` (returns podcast/video list for roadmap building).

## Style & UX

- Cornell palette on dark: red titles, white mono body.
- Neovim-inspired header with blinking "insert coin" prompt.
- Arcade fonts: Press Start 2P, VT323, Roboto Mono.
- Ka-ching sound on task completion: `public/sfx/kaching.mp3` via `src/sfx/useSfx.ts`.

