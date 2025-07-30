# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- GitHub Pages deployment workflow for generated protocols
- Comprehensive testing infrastructure with CI/CD
- Improved error handling in post-generation hooks
- Support for deploying specific versions/commits to GitHub Pages

### Changed
- Updated all schemas to use stable ReproSchema version 1.0.0
- Standardized schema filenames to lowercase convention
- Fixed context paths from `/contexts/generic` to `/contexts/reproschema`

### Fixed
- Schema version inconsistencies
- Hardcoded activity references in protocol template
- Path mismatches in generated schemas

## [1.0.0] - 2024-06-12

### Added
- Initial release of reproschema-protocol-cookiecutter
- Support for generating ReproSchema protocols
- Customizable number of activities (1-5)
- Pre-configured activity types:
  - Basic activities with various input types
  - Voice recording activities
  - Selection activities
- Integration with reproschema-ui
- Cruft support for template updates
- Basic documentation and examples

[Unreleased]: https://github.com/ReproNim/reproschema-protocol-cookiecutter/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/ReproNim/reproschema-protocol-cookiecutter/releases/tag/v1.0.0