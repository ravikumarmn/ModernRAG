# ModernRAG Frontend

This directory contains the frontend code for the ModernRAG project website, which is deployed to GitHub Pages.

## Structure

- `index.html` - Main landing page
- `documentation.html` - Documentation page
- `styles.css` - CSS styles
- `script.js` - JavaScript functionality
- `assets/` - Directory containing images and other assets
- `_config.yml` - GitHub Pages configuration
- `deploy-gh-pages.yml` - GitHub Actions workflow file (to be moved to `.github/workflows/`)

## Local Development

To run the website locally:

```bash
# Navigate to the frontend directory
cd frontend

# Start a local server
python -m http.server 8000
```

Then open your browser to `http://localhost:8000`

## Deployment

The website is automatically deployed to GitHub Pages using GitHub Actions whenever changes are pushed to the main branch. The workflow is defined in the `deploy-gh-pages.yml` file.

## GitHub Pages Setup

To set up GitHub Pages for this project:

1. Go to your GitHub repository settings
2. Navigate to the "Pages" section
3. Select the "GitHub Actions" as the source
4. The site will be deployed automatically when you push to the main branch

## Notes for Developers

- Update the GitHub username in all files (replace `yourusername` with your actual GitHub username)
- The workflow file (`deploy-gh-pages.yml`) should be moved to the `.github/workflows/` directory
- Make sure to update the documentation as the project evolves
