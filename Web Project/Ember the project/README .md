# Ember — AI fire-safety assistant (prototype)

A front-end-only prototype of a fire-safety companion app. It opens with an
"AI waking up" moment (typewriter greeting + pulsing orb), then shows a
sensor status rail, a risk map, quick actions, and a small chat panel you
can type into.

The chat replies are canned/keyword-matched in `src/App.jsx` (see
`answerFrom`) — there's no real model behind it yet. Swap that function for
a fetch to your own backend or the Anthropic API when you're ready to wire
it up for real.

## Run it in VS Code

1. Open this folder in VS Code (`File → Open Folder…`).
2. Open a terminal in VS Code (`` Ctrl/Cmd + ` ``) and install dependencies:
   ```
   npm install
   ```
3. Start the dev server:
   ```
   npm run dev
   ```
4. Open the URL it prints (usually `http://localhost:5173`) in your browser.

Vite will hot-reload as you edit files in `src/`.

## Project structure

```
fire-helper-ai/
├── index.html          entry HTML, loads the fonts
├── package.json
├── vite.config.js
└── src/
    ├── main.jsx         React root
    ├── App.jsx          all components + logic
    └── index.css        design tokens + styles
```

## Where to take this next

- Wire `answerFrom()` up to a real model or backend.
- Replace the mock sensor/risk data with a live feed.
- Add real geolocation for the risk map instead of the placeholder rings.
