# Livestream Volunteer Training Site

MkDocs Material site for church livestream volunteers. Deployed to GitHub Pages by `.github/workflows/deploy.yml` on every push to `main`. The site is **public**.

Readers are volunteers with **no video experience**. One person runs the whole Sunday livestream alone.

## Commands

The easiest setup is the dev container (`.devcontainer/`). In VS Code, run "Dev Containers: Reopen in Container", then run the default build task (Ctrl+Shift+B) to serve the site. Without the container:

```bash
pip install -r requirements.txt
mkdocs serve            # preview at http://127.0.0.1:8000/livestream/
mkdocs build --strict   # same check CI runs; warnings fail the build
```

When you add, rename or remove a page, update `nav:` in `mkdocs.yml`.

## Hard rules

- **No personal or sensitive info, ever.** That means no phone numbers, names with contact details, logins, passwords, stream keys or IP addresses. Contacts live on the private printed booth card. Write "call the on-call tech lead".
- **Use the exact same names everywhere.** These strings must match the Stream Deck and SuperJoy labels:
  - Presets: `Cam 1 P3`, `Cam 2 P5` (Cam 1 = center, Cam 2 = left side when facing the stage). P1 is always the safe wide shot.
  - Scenes: `Scene 7 — Sermon Split` (em dash). The scene list: 1 Countdown, 2 Cam 1 + Lyrics, 3 Cam 2 + Lyrics, 4 Cam 1 Clean, 5 Cam 2 Clean, 6 Full Slide, 7 Sermon Split, 8 Break, 9 End Slate.
- The docs describe the **target** setup. Don't invent values that aren't known yet, such as exposure settings or resolution. Write `TBD` instead.

## Pictures

- Every scene and preset gets a picture: a 16:9 SVG mock frame in `docs/assets/diagrams/` that shows the composition, with a caption.
- Under each diagram, add a placeholder for the real frame:
  ```html
  <div class="photo-placeholder">PHOTO NEEDED: cam1-p3.jpg</div>
  ```
  Real photos go in `docs/assets/photos/` with that exact filename. They replace the placeholder, not the SVG.

## Callouts

Use Material admonitions:
- `!!! danger` for the off-air camera rule ("only move the camera that isn't live") and the no-slides-during-Sunday-school rule.
- `!!! tip` for good habits.

## Reference sheets (`docs/reference/`, `docs/training/skills-checklist.md`)

These are printed and kept at the booth. Each one **must fit on one Letter page**.

```yaml
---
template: reference.html
hide:
  - navigation
  - toc
---
```

`template: reference.html` (in `overrides/`) wraps the page in `.reference-sheet`. That gives it larger type and turns off printed link URLs. Keep these pages short: a table or checklist, no long explanations. Link to the onboarding guide for the "why".

## Print

`docs/stylesheets/extra.css` handles print. It hides the header, nav, footer and search, and avoids page breaks inside tables, figures and admonitions. It prints link URLs on guide pages only. Check a page with the browser's print preview after a big change.

## Writing style

- Talk to the reader as "you". Use short sentences.
- Use numbered steps for procedures.
- Define each video term the first time a page uses it, or link to `onboarding/video-basics.md`.
