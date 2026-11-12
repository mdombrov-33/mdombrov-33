# Install this GitHub profile README

1. Upload `README.md`, `assets/`, `scripts/`, and `.github/workflows/` to the root of https://github.com/mdombrov-33/mdombrov-33. Keep `.github` intact (it's a hidden folder).
2. Commit the files to the default branch. Preserve any existing files you want to keep.
3. In your GitHub repo: **Actions → Refresh project cards → Run workflow → Run workflow**. This replaces the placeholder SVGs with live stars, forks, descriptions, and primary languages immediately after the first successful run.
4. The workflow refreshes the cards every day. GitHub may delay scheduled runs. Because generated SVGs are committed to the repo, the profile continues working even if the API or action is temporarily unavailable.
5. If the workflow can't push, go to **Settings → Actions → General → Workflow permissions** and set **Read and write permissions** (if your repo policy allows it), then rerun. The workflow already declares `permissions: contents: write`.

**Project selection is fixed to exactly these repos:** `go-promptguard`, `vault66-crt-effect`, `vex-mcp`. Change `REPOS` in `scripts/update_projects.py` and the corresponding links in README.md if you want to select different projects.

**Dynamic fields:** public repository name, stars, forks, description, primary language (daily updates). Each card links to the real repository.

**Static assets:** hero.gif, hero.png, divider.svg, footer.png.

No third-party project card image API is needed. GitHub's public REST API is accessed by the GitHub Actions workflow using the built-in `GITHUB_TOKEN`. The Spotify and overall GitHub stats widgets remain third-party services as before.

**Note on responsiveness:** GitHub README HTML doesn't support custom layout CSS. Cards are 32% width and may appear small on narrow screens, especially on mobile. For a mobile-friendly alternative, change widths to `48%` and put the third card on its own row.
