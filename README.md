# The Corporate Brief — staging

This is the private staging repository for **The Corporate Brief (TCB)**. It contains the source files for a Jekyll site used to generate weekly briefings on markets, macro/policy, geopolitics, deals, IPOs, and companies & tech. Posts are stored in `_posts/` with weekly markdown files.

## Structure

- `index.html` – home page with swipeable cards of recent posts
- `pages/` – category pages (Macro/Policy, Geopolitics, Deals, IPOs, Companies & Tech) plus archive and search pages
- `_layouts/` – Jekyll layouts
- `_includes/` – reusable components (card template)
- `assets/` – CSS and JavaScript files
- `.github/workflows/` – GitHub Actions workflows (build only)
- `_config.yml` – site configuration
- `Gemfile` – Ruby gems used to build the site

## Local development

To build and preview the site locally, install dependencies and run Jekyll:

```bash
bundle install
bundle exec jekyll serve
```

This will serve the site at `http://localhost:4000` with live reload.

## Deployment

GitHub Pages hosting is disabled for this private staging repository. When ready to launch, transfer this repository to a public GitHub Pages repo (e.g., using the final brand name) and enable Pages or point a custom domain. Do **not** enable GitHub Pages on this private staging repository.
