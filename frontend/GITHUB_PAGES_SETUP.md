# Setting Up GitHub Pages for ModernRAG

This document provides step-by-step instructions for setting up GitHub Pages for the ModernRAG project.

## Prerequisites

1. A GitHub account
2. The ModernRAG repository pushed to GitHub
3. Admin access to the repository

## Step 1: Enable GitHub Pages

1. Go to your GitHub repository (https://github.com/yourusername/ModernRAG)
2. Click on "Settings" tab
3. Scroll down to the "Pages" section in the left sidebar
4. Under "Source", select "GitHub Actions" from the dropdown menu
5. Click "Save"

## Step 2: Set Up GitHub Actions Workflow

1. Create a `.github/workflows` directory in your repository if it doesn't exist already
2. Move the `deploy-gh-pages.yml` file from the `frontend` directory to the `.github/workflows` directory:

```bash
mkdir -p .github/workflows
mv frontend/deploy-gh-pages.yml .github/workflows/
```

3. Commit and push these changes:

```bash
git add .github/workflows/deploy-gh-pages.yml
git commit -m "Add GitHub Pages deployment workflow"
git push
```

## Step 3: Update Repository Settings (Optional)

1. Go to your GitHub repository settings
2. Under "Pages" section, you can configure:
   - Custom domain (if you have one)
   - Enforce HTTPS
   - Branch protection rules

## Step 4: Customize Your Site

1. Update the `frontend/_config.yml` file with your information:
   - Replace `yourusername` with your actual GitHub username
   - Update the title and description as needed
   - Set the correct baseurl and url values

2. Update the links in the HTML files:
   - In `frontend/index.html` and `frontend/documentation.html`, replace all instances of `yourusername` with your actual GitHub username

## Step 5: Trigger the First Deployment

1. Push a change to the main branch to trigger the GitHub Actions workflow:

```bash
git commit --allow-empty -m "Trigger GitHub Pages deployment"
git push
```

2. Go to the "Actions" tab in your GitHub repository to monitor the workflow
3. Once the workflow completes successfully, your site will be available at `https://yourusername.github.io/ModernRAG`

## Step 6: Add a Status Badge to Your README (Optional)

Add the following markdown to your README.md file:

```markdown
[![Deploy to GitHub Pages](https://github.com/yourusername/ModernRAG/actions/workflows/deploy-gh-pages.yml/badge.svg)](https://github.com/yourusername/ModernRAG/actions/workflows/deploy-gh-pages.yml)
```

Replace `yourusername` with your actual GitHub username.

## Troubleshooting

If you encounter issues with the GitHub Pages deployment:

1. Check the GitHub Actions logs for errors
2. Ensure all file paths in the workflow file are correct
3. Verify that the repository permissions are set correctly
4. Make sure the `frontend` directory contains all necessary files

## Additional Resources

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Custom Domain Setup](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)
