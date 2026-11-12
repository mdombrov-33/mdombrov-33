#!/usr/bin/env python3
"""Render three dynamic SVG repository cards, using GitHub's public REST API.

Works with stdlib only. Run from repo root. In GitHub Actions, GITHUB_TOKEN
raises API limits; errors abort without overwriting the existing cards.
"""
import html
import json
import os
import pathlib
import urllib.error
import urllib.request

OWNER = 'mdombrov-33'
REPOS = ['go-promptguard', 'vault66-crt-effect', 'vex-mcp']
OUT = pathlib.Path('assets')


def fetch(repo):
    url = f'https://api.github.com/repos/{OWNER}/{repo}'
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'mdombrov33-readme-project-cards', 'X-GitHub-Api-Version': '2022-11-28'}
    if os.environ.get('GITHUB_TOKEN'):
        headers['Authorization'] = f'Bearer {os.environ["GITHUB_TOKEN"]}'
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=20) as response:
        info = json.load(response)
    if info.get('full_name', '').lower() != f'{OWNER}/{repo}'.lower():
        raise ValueError(f'Unexpected repository returned for {repo}')
    return info


def shorten(text, n=78):
    text = ' '.join((text or 'No description provided').split())
    return text if len(text) <= n else text[:n - 1].rsplit(' ', 1)[0] + '…'


def lines(text, wrap_at=35):
    words = text.split()
    result = []
    row = ''
    for w in words:
        if len(row) + len(w) + 1 > wrap_at and row:
            result.append(row)
            row = w
        else:
            row = (row + ' ' + w).strip()
    if row: result.append(row)
    return result[:2]


def generate(repo, data):
    name = html.escape(repo)
    description = shorten(data.get('description'), 76)
    copy = lines(description, 38)
    labels = ''.join(f'<text x="31" y="{109+i*24}" font-size="17" fill="#D6C8E7">{html.escape(line)}</text>' for i, line in enumerate(copy))
    stars = data.get('stargazers_count')
    forks = data.get('forks_count')
    language = data.get('language') or 'Other'
    starstr = f'{stars:,}' if isinstance(stars, int) else '—'
    forkstr = f'{forks:,}' if isinstance(forks, int) else '—'
    # Visually restrained glitch texture; kept below text for readability.
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="220" viewBox="0 0 400 220" role="img" aria-label="{name} repository card">
<defs>
 <linearGradient id="bg" x1="0" x2="1" y1="0" y2="1"><stop stop-color="#180B25"/><stop offset="0.58" stop-color="#0D0616"/><stop offset="1" stop-color="#210D2B"/></linearGradient>
 <linearGradient id="accent" x1="0" x2="1"><stop stop-color="#7024AC"/><stop offset="0.6" stop-color="#BD73E6"/><stop offset="1" stop-color="#6820B2"/></linearGradient>
 <linearGradient id="mist" x1="0" x2="1"><stop stop-color="#7323A7" stop-opacity="0"/><stop offset="0.6" stop-color="#A855F7" stop-opacity=".22"/><stop offset="1" stop-color="#9C27B0" stop-opacity=".03"/></linearGradient>
 <clipPath id="clip"><rect width="398" height="218" x="1" y="1" rx="12"/></clipPath>
</defs>
<rect x="1" y="1" width="398" height="218" rx="12" fill="url(#bg)" stroke="#4F2964" stroke-width="1.5"/>
<g clip-path="url(#clip)">
 <path d="M40 -8 Q144 62 237 -12 T440 42 L440 0 Z" fill="url(#mist)"/>
 <path d="M210 0 Q288 60 405 18" fill="none" stroke="#9F57BE" stroke-width="1.3" opacity=".24"/>
 <path d="M230 -3 Q312 74 410 27" fill="none" stroke="#C084FC" stroke-width="1" opacity=".15"/>
 <path d="M-1 23 h55 M318 35 h91 M291 40 h96 M6 173 h22 M307 172 h97 M348 177 h62" stroke="url(#accent)" opacity=".32" stroke-width="2"/>
 <path d="M16 7 h40 M332 15 h68 M355 20 h47 M0 191 h46" stroke="#D59BFF" opacity=".18"/>
</g>
<g font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Arial,sans-serif">
 <g transform="translate(26,27)" fill="none" stroke="#C087FA" stroke-width="1.9"><path d="M8 21 Q-1 17 2 7 Q10 -1 20 5 Q29 -2 37 6 Q40 17 31 21 L30 31 L23 30 L23 24 L17 24 L17 30 L11 31 L10 21 Z"/></g>
 <text x="76" y="55" font-size="24" font-weight="700" fill="#F3DAFF">{name}</text>
 {labels}
 <line x1="26" y1="164" x2="374" y2="164" stroke="#4A255E" stroke-width="1"/>
 <text x="27" y="191" font-size="17" fill="#DCC0F5">★ {starstr}</text>
 <text x="124" y="191" font-size="17" fill="#DCC0F5">⑂ {forkstr}</text>
 <circle cx="{260}" cy="185" r="6" fill="#AF65EA"/>
 <text x="273" y="191" font-size="16" fill="#D8BCEF">{html.escape(language)}</text>
</g>
</svg>'''


def main():
    # Fetch all metadata before writing anything to avoid half-updated output.
    data = {repo: fetch(repo) for repo in REPOS}
    OUT.mkdir(parents=True, exist_ok=True)
    for repo in REPOS:
        p = OUT / f'project-{repo}.svg'
        p.write_text(generate(repo, data[repo]), encoding='utf-8')
        print(f'{p}: stars={data[repo].get("stargazers_count")}, forks={data[repo].get("forks_count")}')

if __name__ == '__main__':
    main()
