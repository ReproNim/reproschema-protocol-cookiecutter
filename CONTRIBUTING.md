# Contributing to reproschema-protocol-cookiecutter

Thank you for your interest in contributing to the ReproSchema Protocol Cookiecutter! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR-USERNAME/reproschema-protocol-cookiecutter.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes (see Testing section)
6. Commit your changes using conventional commits
7. Push to your fork and submit a pull request

## Development Setup

### Prerequisites

- Python 3.8+
- Node.js 20+ (for testing GitHub Pages deployment)
- Git

### Installing Dependencies

```bash
pip install -r requirements.txt
```

### Pre-commit Hooks

We use pre-commit hooks to ensure code quality:

```bash
pre-commit install
```

## Testing

### Running Tests Locally

```bash
# Test the cookiecutter template generation
python test_cookiecutter.py

# Or use the micromamba environment
./run_in_env.sh python test_cookiecutter.py
```

### Testing Your Changes

1. Generate a test protocol:
   ```bash
   cookiecutter . --no-input -o test-output
   ```

2. Validate the generated schemas:
   ```bash
   cd test-output/my-reproschema-protocol
   reproschema validate my_reproschema_protocol/my_reproschema_protocol_schema
   ```

## Code Style

- Python code follows PEP 8
- Use meaningful variable and function names
- Add docstrings to functions
- Keep functions focused and small

## Commit Messages

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `chore:` Maintenance tasks
- `test:` Test additions or modifications

Example:
```
feat: add support for custom activity types

- Allow users to define custom activity schemas
- Update documentation with examples
- Add tests for custom activities
```

## Pull Request Process

1. Ensure all tests pass
2. Update documentation if needed
3. Update CHANGELOG.md with your changes under "Unreleased"
4. Fill out the PR template completely
5. Request review from maintainers

## Release Process

Releases are managed by maintainers using a hybrid approach: manual release workflow with automated changelog generation.

### Creating a Release

1. Go to Actions → Release workflow
2. Click "Run workflow"
3. Enter the new version (e.g., 1.0.1)
4. Select release type (patch/minor/major)
5. The workflow will:
   - Update version in pyproject.toml and cookiecutter.json
   - **Automatically generate and update CHANGELOG.md using git-cliff**
   - Create a git tag
   - Generate comprehensive release notes from conventional commits
   - Create a GitHub release

### Automated Changelog

The project uses [git-cliff](https://git-cliff.org/) to automatically generate changelog entries from conventional commits. This eliminates manual changelog maintenance and ensures consistency.

- Changelog is generated from commit messages following the Conventional Commits specification
- The `.cliff.toml` configuration file defines how commits are grouped and formatted
- CHANGELOG.md is automatically updated during the release process
- No manual post-release changelog updates needed!

### Version Guidelines

- **Major** (X.0.0): Breaking changes to template structure or output
- **Minor** (1.X.0): New features, activities, or capabilities
- **Patch** (1.0.X): Bug fixes, documentation updates

### Why This Approach?

We use a hybrid approach (manual release + automated changelog) because:
- Cookiecutter templates have different release needs than packages
- Manual releases provide intentional version control
- Automated changelog prevents human error and ensures consistency
- Simpler than full release automation tools while addressing key pain points

## Schema Updates

When updating ReproSchema versions or structures:

1. Use `update_schema_version.py` to update all schemas consistently
2. Test that all schemas validate with the new version
3. Update documentation to reflect changes

## Adding New Activities

To add a new activity type:

1. Create the activity folder in `{{cookiecutter.protocol_name}}/activities/`
2. Add the activity schema and item schemas
3. Update `hooks/pre_gen_project.py` to include the new activity option
4. Add tests for the new activity
5. Update documentation

## Questions?

Feel free to:
- Open an issue for bugs or feature requests
- Start a discussion for questions
- Join the ReproNim community channels

Thank you for contributing!