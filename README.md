# data-contract-cli

A Python CLI for validating and normalizing CSV files using YAML data contracts.

## Objective

`data-contract-cli` is designed to validate CSV files before they are imported into backend systems, databases, CRMs, ERPs, or internal workflows.

A YAML contract defines the expected columns, data types, validation rules, and transformations. The tool will use this contract to identify invalid rows, normalize valid values, and generate structured output reports.

This project is being developed as part of my backend Python learning roadmap. Its main purpose is to practise robust file processing, validation, error handling, logging, testing, and CLI development.

## Planned features

* Validate CSV columns against a YAML contract
* Validate values row by row
* Normalize valid values
* Separate valid and invalid rows
* Generate a clean CSV file
* Generate a CSV error report
* Generate a JSON execution summary
* Validate YAML contracts
* Support strict and permissive validation modes
* Return explicit exit codes
* Generate a starter contract from a CSV file

## Installation

```bash
git clone https://github.com/alexiskuypers/data-contract-cli.git
cd data-contract-cli
```

The installation process will be documented once the first executable version is available.

## Planned usage

Validate a CSV file:

```bash
data-contract validate input.csv --contract contract.yml
```

Validate a contract:

```bash
data-contract check-contract contract.yml
```

Generate a starter contract:

```bash
data-contract init-contract input.csv --output contract.yml
```

These commands describe the planned CLI interface and are not yet available.

## Project structure

```text
data-contract-cli/
├── examples/
├── src/
│   └── data_contract_cli/
│       └── cli.py
├── tests/
├── README.md
└── pyproject.toml
```

## Status

The project is currently in its initial development stage.

## Next steps

* Define the first validation contract format
* Implement the initial CLI entry point
* Add a minimal CSV example
* Create the first contract validation issue
