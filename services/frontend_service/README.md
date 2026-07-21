# AI Chat — Landing Screen

A pixel-close React implementation of the dark AI-chat home screen: slim icon sidebar, gradient greeting, suggested prompt cards with a working "Refresh Prompts" cycle, and a message composer with a search-scope dropdown, attachment actions, live character count, and a send button.

## Stack

- React 18 + Vite
- lucide-react for icons
- Plain CSS (one stylesheet per component, design tokens in `src/styles/global.css`)

## Getting started

```bash
npm install
npm run dev
```

Then open the URL Vite prints (usually http://localhost:5173).

Production build:

```bash
npm run build
npm run preview
```

## Structure

```
index.html                  Entry HTML (loads Inter from Google Fonts)
src/
  main.jsx                  React bootstrap
  App.jsx                   Layout shell + shared input state
  styles/global.css         Color tokens, resets, app shell
  components/
    Sidebar.jsx / .css      Left rail: logo, new chat, nav, settings, avatar
    Greeting.jsx / .css     Gradient headline + subtitle
    PromptGrid.jsx / .css   4-card grid + Refresh Prompts (cycles prompt sets)
    PromptCard.jsx / .css   Single suggestion card (click fills the composer)
    ChatInput.jsx / .css    Textarea, "All Web" dropdown, actions, 0/1000, send
```

## Behavior notes

- Clicking a prompt card copies its text into the composer.
- "Refresh Prompts" swaps in an alternate set of suggestions with a spin animation.
- The "All Web" pill opens a scope menu (All Web / Academic / News / Social).
- Character count caps at 1000; Enter sends, Shift+Enter adds a newline.
- `handleSend` in `ChatInput.jsx` currently logs to the console — wire your API call there.
- Responsive down to mobile; respects `prefers-reduced-motion`.
