# Anant Chaturvedi / XlaMus Portfolio

Multi-page static portfolio for GitHub Pages. The site is intentionally framework-light: HTML, CSS and a small JS enhancement layer keep the output fast and easy to maintain.

## Local preview

```bash
python3 scripts/build_static.py
python3 -m http.server 8000 --directory dist
```

Open `http://localhost:8000`.

## GitHub Pages

The GitHub Actions workflow builds the static site into `dist/` and publishes it with GitHub Pages. During Actions builds the repository name is automatically used as the project-site base path. The public canonical/sitemap URL is inferred from `GITHUB_REPOSITORY`, so no domain is invented in source files.

For a custom domain later, set `SITE_URL` in the workflow (or as an Actions variable) and rebuild. The base path can be overridden with `BASE_PATH` when needed.

## Content model

Project and game cards are generated from small data blocks in the page sources, while shared styling and navigation live in `css/site.css` and `js/site.js`. Add new project cards without changing the visual system.


## Visual assets

The portfolio uses the supplied profile image and XlaMus banner as identity assets. Supplied atmospheric imagery is used selectively at low opacity, while project visuals remain specific to the work they accompany.
