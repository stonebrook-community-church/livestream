# Livestream Volunteer Training

Training material and printable booth reference sheets for the Stonebrook Community Church livestream team.

**Site:** https://stonebrook-community-church.github.io/livestream/

The site is built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/). It is published to GitHub Pages automatically every time a change lands on `main`.

> **This repo and the site are public.** Never add phone numbers, logins, passwords, stream keys or IP addresses. Those go on the private printed booth card.

## Editing a page

You don't need to install anything for small changes.

1. Open the page on the site and click the **Edit this page** (pencil) icon. You can also browse to the file under `docs/` on GitHub.
2. Make your change in GitHub's editor. Pages are written in Markdown.
3. Click **Commit changes** and commit to `main`.
4. The site updates in about a minute. You can watch progress in the **Actions** tab.

If the build fails, the Actions run shows the error and the live site stays as it was.

## Previewing locally

### Dev container (recommended)

You need [VS Code](https://code.visualstudio.com/), the **Dev Containers** extension and Docker.

1. Open this folder in VS Code.
2. Run **Dev Containers: Reopen in Container** from the command palette.
3. Press **Ctrl+Shift+B** to start the preview. It opens at http://localhost:8000/livestream/ and reloads when you save.

To run the same check as CI, use the **MkDocs: build (strict)** task.

### Without a container

You need Python 3.10 or newer.

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve             # preview at http://127.0.0.1:8000/livestream/
mkdocs build --strict    # same check CI runs
```

## Layout

| Path | What's there |
|---|---|
| `docs/onboarding/` | Onboarding guide, read before your first Sunday |
| `docs/reference/` | One-page booth sheets to print and keep at the booth |
| `docs/training/` | Skills Checklist sign-off sheet |
| `docs/admin/` | How to maintain this site, plus the backlog |
| `docs/assets/diagrams/` | SVG mock frames for scenes and presets |
| `docs/assets/photos/` | Real reference photos, which replace the `PHOTO NEEDED` placeholders |
| `docs/stylesheets/extra.css` | Print styles and placeholder styling |
| `overrides/reference.html` | Page template for the one-page printable sheets |
| `mkdocs.yml` | Site config and navigation. Update `nav:` when you add a page |
| `.github/workflows/deploy.yml` | Builds and deploys to GitHub Pages |

## Conventions

Writing style, naming (`Cam 1 P3`, `Scene 7 — Sermon Split`), pictures, callouts and the rules for reference sheets are in [CLAUDE.md](CLAUDE.md). Read it before making bigger changes, whether you edit by hand or with Claude.
