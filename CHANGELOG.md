# Changelog

All notable changes to `pfctl_exporter` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.4.0] - 2023-12-18

### Added

- Parse `pfctl -vs rules` output into `pfctl_rule_*` metrics.

### Changed

- Rename interface metrics from `pfctl_interfaces_*` to `pfctl_interface_**`


## [v0.3.0] - 2023-12-18

### Added

- Parse `pfctl -vvs Interfaces` output into metrics.


## [v0.2.0] - 2023-12-18

### Changed

- Installed executable is now `pfctl-exporter` instead of `pfctl_exporter`


## [v0.1.0] - 2023-12-18

- Initial release. Only `pfctl -vvs info` metrics are parsed for now. Largely untested.
