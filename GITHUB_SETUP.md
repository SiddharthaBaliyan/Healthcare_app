# GitHub Setup Instructions

## Push Your Project to Healthcare_app Repository

Follow these steps to deploy your Heart Disease Prediction Pipeline to your GitHub repository.

### Step 1: Initial Git Configuration (First Time Only)

```bash
cd c:\Users\Choud\PROJECTS_BETA\CLASSIFIER1

# Set your Git user configuration
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Or set globally (optional)
# git config --global user.name "Your Name"
# git config --global user.email "your.email@example.com"
```

### Step 2: Initialize Repository Locally

```bash
# Initialize if not already done
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Heart Disease Prediction Pipeline with CI/CD, Testing, and Training

- Complete ML training pipeline with Random Forest classifier
- FastAPI inference server with full documentation
- Beautiful Flask frontend with real-time predictions
- Comprehensive pytest test suite (40+ tests)
- GitHub Actions CI/CD pipeline
- Automated testing on Python 3.10, 3.11, 3.12
- Code quality checks (flake8, black)
- Coverage reporting with Codecov
- Complete project documentation"
```

### Step 3: Create Repository on GitHub

1. Go to [GitHub.com](https://github.com)
2. Click **+** icon → **New repository**
3. Repository name: `Healthcare_app`
4. Description: "Heart Disease Prediction Pipeline with ML Training and FastAPI"
5. Select **Public** or **Private**
6. **Do NOT** initialize with README (you have one)
7. Click **Create repository**

### Step 4: Add Remote and Push

```bash
# Add the GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/Healthcare_app.git

# Rename branch to main (if on master)
git branch -M main

# Push code to GitHub
git push -u origin main
```

### Step 5: Verify GitHub Actions

1. Go to your repository: `https://github.com/YOUR_USERNAME/Healthcare_app`
2. Click **Actions** tab
3. You should see the CI/CD workflow running
4. Wait for all checks to pass (green checkmark)

## What Gets Deployed

### Folder Structure
```
Healthcare_app/
├── .github/workflows/
│   └── ci-cd.yml              # GitHub Actions workflow
├── .gitignore                 # Git ignore rules
├── data/
│   └── train.csv              # Training data
├── training/
│   └── train.py               # Training pipeline
├── inference/
│   └── app.py                 # FastAPI server
├── frontend/
│   ├── app.py                 # Flask frontend
│   ├── static/
│   │   └── style.css          # Styling
│   └── templates/
│       ├── index.html         # Frontend HTML
│       └── script.js          # Frontend JavaScript
├── models/
│   ├── heart_disease_model.pkl
│   ├── scaler.pkl
│   ├── label_encoder.pkl
│   └── feature_columns.pkl
├── tests/
│   ├── conftest.py            # Pytest configuration
│   ├── test_training.py       # Training tests
│   ├── test_inference.py      # API tests
│   └── test_integration.py    # Integration tests
├── logs/                      # Training logs
├── requirements.txt           # Dependencies
├── requirements-test.txt      # Testing dependencies
├── pytest.ini                 # Pytest configuration
├── README.md                  # Project documentation
├── DEPLOYMENT.md              # Deployment guide
├── config.py                  # Configuration
└── run_api.bat / run_frontend.bat   # Run scripts
```

## GitHub Actions Workflow Details

### Triggers
- ✅ Push to `main` branch
- ✅ Push to `develop` branch
- ✅ Pull requests to `main` or `develop`

### Jobs

#### 1. **Test Job**
- Tests Python 3.10, 3.11, 3.12
- Runs pytest suite
- Code quality checks (flake8, black)
- Coverage reporting
- Uploads to Codecov

#### 2. **Build Job**
- Verifies project structure
- Tests API startup
- Validates dependencies

#### 3. **Deploy Job**
- Only runs on `main` branch after successful test/build
- Runs integration tests
- Creates deployment summary
- Archives logs and coverage

## Adding Status Badges to README

Add these badges to your README.md to show CI/CD status:

```markdown
## Status

[![CI/CD Pipeline](https://github.com/YOUR_USERNAME/Healthcare_app/actions/workflows/ci-cd.yml/badge.svg?branch=main)](https://github.com/YOUR_USERNAME/Healthcare_app/actions/workflows/ci-cd.yml)
[![codecov](https://codecov.io/gh/YOUR_USERNAME/Healthcare_app/branch/main/graph/badge.svg)](https://codecov.io/gh/YOUR_USERNAME/Healthcare_app)
```

## Codecov Integration (Optional)

To enable automatic coverage reporting:

1. Go to [Codecov.io](https://codecov.io)
2. Sign in with GitHub
3. Enable your repository
4. Codecov will automatically process coverage reports

## Making Changes After Initial Push

```bash
# Make your changes
# ... edit files ...

# Stage changes
git add .

# Commit
git commit -m "Fix: [description of change]"

# Push to GitHub
git push origin main
```

CI/CD pipeline will automatically run tests!

## Branch Strategy

### Recommended Workflow
```bash
# Create a feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "feat: Add new feature"

# Push feature branch
git push origin feature/new-feature

# Create Pull Request on GitHub
# After review and approval, merge to main
```

## Troubleshooting

### Issue: Permission Denied
```bash
# Generate SSH key (recommended)
ssh-keygen -t ed25519 -C "your.email@example.com"

# Add to GitHub:
# Settings → SSH and GPG keys → New SSH key
# Paste the public key

# Update remote to use SSH
git remote set-url origin git@github.com:YOUR_USERNAME/Healthcare_app.git
```

### Issue: Large Files
GitHub has a 100MB file size limit. If you have large data files:
```bash
# Use Git LFS (Large File Storage)
git lfs install
git lfs track "*.csv"
git add .gitattributes
```

### Issue: Workflow Not Running
1. Check **Settings** → **Actions** → **General**
2. Ensure "Allow all actions" is selected
3. Check `.github/workflows/ci-cd.yml` syntax

## View Test Results

1. Go to **Actions** tab
2. Click on a workflow run
3. Click on the **test** job
4. Expand job logs to see:
   - Pytest output
   - Code coverage report
   - Any failures or warnings

## Next Steps

1. ✅ Push to GitHub
2. ✅ Verify CI/CD pipeline runs
3. ✅ Check test results
4. ✅ Monitor code coverage
5. ✅ Set up branch protection rules (optional)

## Protecting Main Branch (Optional)

```
Settings → Branches → Add rule
- Branch name pattern: main
- Require a pull request before merging
- Require status checks to pass before merging
- Dismiss stale pull request approvals
- Require conversation resolution before merging
```

## Congratulations! 🎉

Your Heart Disease Prediction Pipeline is now:
- ✅ Version controlled with Git
- ✅ Deployed to GitHub
- ✅ Running automated tests
- ✅ Checking code quality
- ✅ Tracking code coverage
- ✅ Integrated with Codecov

For more help, see [DEPLOYMENT.md](DEPLOYMENT.md)
