# repo-development-tooling Specification

## Purpose
TBD - created by archiving change v1-f013-harden-installer-and-dev-environment. Update Purpose after archive.
## Requirements
### Requirement: Installer distinguishes missing target files from missing workflow markers
The repository installer SHALL treat a missing target `AGENTS.md` file differently from an existing file that has not yet been initialized with the managed workflow markers.

#### Scenario: Installer fails when target AGENTS file is missing
- **WHEN** `install.sh` runs and `${AGENTS_HOME:-$HOME/.agents}/AGENTS.md` does not exist
- **THEN** installation fails
- **AND** the failure message states that the target `AGENTS.md` file is missing

#### Scenario: Installer initializes markers in an existing AGENTS file
- **WHEN** `install.sh` runs and the target `AGENTS.md` exists but lacks the managed workflow markers
- **THEN** installation appends exactly one managed workflow section to that file
- **AND** the install does not fail solely because the markers were previously absent

### Requirement: Managed development environment is explicitly reproducible
The tracked development environment SHALL declare the Python floor and Conda channels required to run the repository's tooling consistently.

#### Scenario: Environment definition states compatible interpreter expectations
- **WHEN** contributors inspect `environment.yml`
- **THEN** it declares a Python version floor compatible with the repository's code
- **AND** it declares the Conda channels needed for repeatable environment resolution

### Requirement: Installer dependencies are documented
The repository documentation SHALL identify the external tool dependencies required by `install.sh`.

#### Scenario: Contributor reviews installation notes
- **WHEN** a contributor follows the documented installation path
- **THEN** the docs name the required sync tool used by `install.sh`
- **AND** the contributor is not expected to infer that dependency from the script alone

