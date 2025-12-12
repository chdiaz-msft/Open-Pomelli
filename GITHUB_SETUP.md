# GitHub Setup Guide

This guide will help you publish the Marketing Agent project to GitHub.

## Prerequisites

- Git installed on your system
- GitHub account created
- Repository created on GitHub (can be done via web interface)

## Step 1: Initialize Git Repository

```bash
cd /Users/anilchandranaidumatcha/Downloads/marketing_agent

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Marketing Agent v2.0.0

- Enhanced Brand DNA Analysis with Vision AI
- Reference-based image generation with auto logo detection
- Smart image format conversion
- Comprehensive documentation and GitHub setup"
```

## Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `marketing-agent` (or your preferred name)
3. Description: "AI Marketing Department in a Box - Inspired by Google's Pomelli"
4. Choose Public or Private
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

## Step 3: Connect and Push to GitHub

```bash
# Add remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/marketing-agent.git

# Verify remote
git remote -v

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 4: Configure Repository Settings

### Enable Features
1. Go to repository Settings
2. Enable:
   - ✅ Issues
   - ✅ Discussions (recommended)
   - ✅ Projects (optional)
   - ✅ Wiki (optional)

### Add Topics
Add relevant topics for discoverability:
- `ai`
- `marketing`
- `automation`
- `brand-analysis`
- `image-generation`
- `python`
- `playwright`
- `vision-ai`

### Set Up Branch Protection (Optional but Recommended)
1. Settings → Branches → Add rule
2. Branch name pattern: `main`
3. Enable:
   - ✅ Require pull request reviews before merging
   - ✅ Require status checks to pass before merging

## Step 5: Add Repository Secrets (for CI/CD)

If you plan to add automated testing:

1. Settings → Secrets and variables → Actions
2. Add secrets:
   - `MUAPIAPP_API_KEY` (for testing)
   - `FAL_KEY` (for testing)

**Note**: Only add these if you're setting up CI/CD. Never commit actual API keys!

## Step 6: Create First Release

1. Go to Releases → Create a new release
2. Tag version: `v2.0.0`
3. Release title: `v2.0.0 - Enhanced Brand Intelligence`
4. Description: Copy from CHANGELOG.md
5. Publish release

## Step 7: Update README Links

After creating the repository, update these placeholders in README.md:

```markdown
- Replace `../../issues` with actual repository URL
- Replace `../../discussions` with actual repository URL
- Update any other placeholder URLs
```

## Step 8: Verify Everything

Check that these files exist and are properly configured:

- ✅ README.md (with badges and proper links)
- ✅ LICENSE (MIT License)
- ✅ .gitignore (excludes api_secrets.py)
- ✅ CONTRIBUTING.md
- ✅ CHANGELOG.md
- ✅ SECURITY.md
- ✅ requirements.txt
- ✅ api_secrets.example.py
- ✅ .github/ISSUE_TEMPLATE/bug_report.yml
- ✅ .github/ISSUE_TEMPLATE/feature_request.yml
- ✅ .github/ISSUE_TEMPLATE/config.yml
- ✅ .github/PULL_REQUEST_TEMPLATE.md

## Step 9: Protect Your API Keys

**CRITICAL**: Verify that `api_secrets.py` is NOT committed:

```bash
# Check git status
git status

# If api_secrets.py appears, it means .gitignore isn't working
# Remove it from git:
git rm --cached api_secrets.py
git commit -m "Remove api_secrets.py from version control"
git push
```

## Step 10: Add Collaborators (Optional)

1. Settings → Collaborators
2. Add team members with appropriate permissions

## Recommended Next Steps

### 1. Set Up GitHub Actions (Optional)
Create `.github/workflows/test.yml` for automated testing

### 2. Add Code Coverage (Optional)
Integrate with Codecov or Coveralls

### 3. Set Up Documentation Site (Optional)
Use GitHub Pages or ReadTheDocs

### 4. Create Project Board (Optional)
Organize issues and features

### 5. Enable Discussions
Great for community Q&A and feature discussions

## Common Issues

### Issue: "Permission denied (publickey)"
**Solution**: Set up SSH keys or use HTTPS with personal access token

### Issue: "api_secrets.py was committed"
**Solution**: 
```bash
git rm --cached api_secrets.py
git commit -m "Remove sensitive file"
git push --force
```
Then rotate your API keys immediately!

### Issue: "Large files rejected"
**Solution**: Use Git LFS for large files or add to .gitignore

## Maintenance

### Regular Tasks
- Update CHANGELOG.md for each release
- Review and respond to issues
- Merge pull requests
- Update dependencies
- Rotate API keys periodically

### Version Bumping
```bash
# Update version in:
# - README.md (Project Status section)
# - CHANGELOG.md (new version entry)

git add .
git commit -m "Bump version to vX.Y.Z"
git tag vX.Y.Z
git push origin main --tags
```

## Resources

- [GitHub Docs](https://docs.github.com)
- [Git Documentation](https://git-scm.com/doc)
- [Semantic Versioning](https://semver.org)
- [Keep a Changelog](https://keepachangelog.com)

---

**You're all set!** 🚀

Your Marketing Agent project is now ready for GitHub. Happy coding!
