# Deployment Guide for GitHub Actions CI/CD

## Overview

This project uses GitHub Actions to automatically test, build, and deploy the Heart Disease Prediction application. The CI/CD pipeline runs on every push and pull request.

## Pipeline Stages

### 1. **Test Stage** 
- Runs on Python 3.10, 3.11, and 3.12
- Executes pytest test suite with coverage reporting
- Performs code quality checks with flake8 and black
- Uploads coverage reports to Codecov

### 2. **Build Stage**
- Verifies project structure
- Tests API startup
- Checks all dependencies are available

### 3. **Deploy Stage**
- Only runs on `main` branch after successful test/build
- Creates deployment summary
- Runs integration tests
- Archives artifacts

## GitHub Actions Workflow Files

### Location: `.github/workflows/ci-cd.yml`

This file defines:
- **Trigger events**: Push to main/develop, Pull requests
- **Test matrix**: Python 3.10, 3.11, 3.12
- **Jobs**: test, build, deploy

## Setting Up GitHub Repository

### Prerequisites
1. GitHub account with repository access
2. Repository initialized with Git

### Step 1: Initialize Git Locally

```bash
cd c:\Users\Choud\PROJECTS_BETA\CLASSIFIER1
git init
git add .
git commit -m "Initial commit: Heart Disease Prediction Pipeline with CI/CD"
```

### Step 2: Add Remote Repository

```bash
git remote add origin https://github.com/yourusername/Healthcare_app.git
git branch -M main
git push -u origin main
```

### Step 3: Enable GitHub Actions

1. Go to your GitHub repository
2. Navigate to **Settings** → **Actions**
3. Click **General**
4. Under "Actions permissions", select **Allow all actions and reusable workflows**
5. Click **Save**

## Running Tests Locally

### Run All Tests
```bash
pytest tests/ -v
```

### Run with Coverage
```bash
pytest tests/ --cov=inference --cov=training --cov-report=html
```

### Run Specific Test Category
```bash
pytest tests/test_inference.py -v  # API tests
pytest tests/test_training.py -v   # Training tests
pytest tests/test_integration.py -v # Integration tests
```

### Run Tests in Parallel
```bash
pytest tests/ -v -n auto
```

## GitHub Actions Features

### 1. Automated Testing
- Runs on every push
- Tests Python 3.10, 3.11, 3.12 compatibility
- Generates coverage reports

### 2. Code Quality Checks
- **flake8**: Python linting
- **black**: Code formatting
- **Coverage**: Code coverage reporting

### 3. Build Verification
- Checks project structure
- Verifies API can start
- Tests dependencies

### 4. Deployment Artifacts
- Stores logs
- Archives coverage HTML reports
- 30-day retention period

### 5. Codecov Integration
- Automatic coverage reporting
- Comments on pull requests
- Tracks coverage trends

## Customizing the Workflow

### Edit Workflow File
Edit `.github/workflows/ci-cd.yml` to:

```yaml
# Change Python versions
matrix:
  python-version: ['3.9', '3.10', '3.11']

# Add environment variables
env:
  API_PORT: 8000
  FRONTEND_PORT: 5000

# Modify triggers
on:
  push:
    branches: [ main, develop, staging ]
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight
```

## Monitoring Builds

### View Build Status
1. Go to **Actions** tab in your GitHub repository
2. Click on a workflow run to see details
3. Expand job logs to troubleshoot

### Status Badges
Add to README.md:
```markdown
[![CI/CD Pipeline](https://github.com/yourusername/Healthcare_app/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/yourusername/Healthcare_app/actions/workflows/ci-cd.yml)

[![codecov](https://codecov.io/gh/yourusername/Healthcare_app/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/Healthcare_app)
```

## Secrets and Environment Variables

### Setting Secrets in GitHub
1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add secrets needed for deployment

Example secrets:
```yaml
DOCKERHUB_USERNAME
DOCKERHUB_TOKEN
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
```

## Common Issues and Solutions

### Issue: Tests Fail on GitHub but Pass Locally
**Solution**: 
- Check Python version differences
- Verify all dependencies in requirements.txt
- Check file path issues (use `/` not `\`)

### Issue: API Startup Times Out
**Solution**:
- Increase timeout in workflow
- Check for blocking operations
- Verify port 8000 is available

### Issue: Coverage Reports Not Uploading
**Solution**:
- Ensure pytest-cov is installed
- Check Codecov token is set
- Verify coverage.xml is generated

## Best Practices

1. **Branch Strategy**
   - Create feature branches for development
   - Use pull requests for code review
   - Merge to main only after CI passes

2. **Commit Messages**
   - Use descriptive commit messages
   - Reference issues: `Fixes #123`
   - Use conventional commits: `feat:`, `fix:`, `test:`

3. **Testing**
   - Write tests for new features
   - Maintain >80% code coverage
   - Test edge cases and error handling

4. **Documentation**
   - Update README with changes
   - Document API endpoints
   - Include setup instructions

## Performance Optimization

### Caching Dependencies
The workflow automatically caches pip dependencies to speed up builds.

### Matrix Strategy
Tests run in parallel across Python versions to save time.

### Conditional Steps
Deployment only runs on main branch after successful tests.

## Contact & Support

For issues or questions:
1. Check existing GitHub Issues
2. Create a new issue with details
3. Include workflow logs if available

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/advanced/testing-dependencies/)
- [Codecov Integration](https://codecov.io/docs)
