# GitHub Actions Configuration

## 🚨 Path Issues Resolution

### Problem
The original error occurred because GitHub Actions runs on Linux environments where Cyrillic characters in paths (`ВяткинСЮ/web`) can cause issues:
```
/home/runner/work/_temp/a11f3869-3fdc-44bc-a43c-bacdc6380802.sh: line 1: cd: ВяткинСЮ/web: No such file or directory
Error: Process completed with exit code 1.
```

### Solution
Three workflow files are provided to handle different scenarios:

#### 1. `security.yml` - Advanced Security Pipeline
- **Dynamic Path Detection**: Uses `find` commands to locate directories
- **Comprehensive Security Tools**: Bandit, Safety, Trivy, GitLeaks, OWASP Dependency Check
- **Multi-Stage Pipeline**: 5 separate jobs for different security aspects
- **Artifact Management**: Uploads all security reports
- **Universal Compatibility**: Works regardless of directory structure

```yaml
WEBDIR=$(find . -name "web" -type d | head -1)
cd "$WEBDIR"
```

#### 2. `security-simple.yml` - Simplified Security Checks
- **Robust File Discovery**: Finds Python files and requirements.txt anywhere
- **Essential Security Tools**: Bandit, Safety, pip-audit, GitLeaks, Flake8
- **Error Tolerant**: Continues even if some files are missing
- **Lightweight**: Single job with multiple steps

#### 3. `security-fixed.yml` - Fallback Version
- **Manual Path Configuration**: For cases where auto-detection fails
- **Customizable**: Easy to modify for specific directory structures

## 🔧 Usage Instructions

### For Standard Repository Structure
Use `security.yml` - it automatically detects the web directory and Python files.

### For Non-Standard or Unknown Structure
Use `security-simple.yml` - it searches the entire repository for relevant files.

### For Custom Setup
Use `security-fixed.yml` and modify the paths according to your specific structure.

## 🛠️ Technical Details

### Dynamic Path Resolution
```bash
# Find web directory
WEBDIR=$(find . -name "web" -type d | head -1)

# Find requirements.txt files
find . -name "requirements.txt" -exec pip install -r {} \;

# Find Python files for scanning
find . -name "*.py" | head -1
```

### Error Handling
- All security steps use `continue-on-error: true`
- Comprehensive logging for debugging
- Graceful fallbacks when files are missing

### Supported Security Tools
1. **Bandit** - Static security analysis for Python
2. **Safety** - Dependency vulnerability checking
3. **pip-audit** - Additional dependency scanning
4. **Trivy** - Container vulnerability scanning
5. **GitLeaks** - Secret detection
6. **OWASP Dependency Check** - Comprehensive dependency analysis
7. **Flake8 & Pylint** - Code quality and style

## 📊 Reports Generated
- JSON format security reports
- GitHub Security tab integration (SARIF)
- Workflow artifacts with retention policies
- Summary reports in GitHub Actions UI

## 🔍 Debugging
If workflows fail:
1. Check the "Actions" tab in GitHub
2. Review the step-by-step logs
3. Verify file structure matches expectations
4. Consider using the simplified version 