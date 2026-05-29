# Alfred Black — Documentation

This repository hosts the public documentation for [Alfred Black](https://github.com/ssdavidai/alfred), an open-source AI butler you can self-host on a single VM.

The site is published with [Mintlify](https://mintlify.com).

## Local preview

```sh
npm install -g mintlify
mintlify dev
```

Then open `http://localhost:3000`.

## Layout

- `docs.json` — site configuration and navigation
- `introduction/`, `quickstart/`, `architecture/`, `surfaces/`, `configuration/`, `integrations/`, `operations/`, `development/`, `reference/`, `troubleshooting/`, `contributing/`, `appendices/` — content trees, one `.mdx` per page
- `scripts/check-links.py` — lightweight local navigation and internal-link check

## Validation

```sh
python3 scripts/check-links.py
```

Run this before opening a PR. It verifies every `docs.json` navigation page exists and that local Markdown/MDX links point to files in this repository.

## Contributing

Open a PR against `main`. Mintlify deploys on merge. See [Contributing](./contributing/pr-conventions.mdx) for conventions.
