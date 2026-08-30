# Teaching Works Lab Ecosystem Catalog

This special organization repository provides three small, separate surfaces:

- [`profile/README.md`](profile/README.md): the human-facing organization home page;
- [`catalog.yaml`](catalog.yaml): the machine-readable repository and relationship catalog;
- [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json): the curated Codex plugin marketplace.

## Add the marketplace

```text
codex plugin marketplace add Teaching-Works-Lab/.github
```

List the available Plugins and install only what the current task needs:

```text
codex plugin list
codex plugin add course-teaching-workflows@teaching-works-lab
```

The marketplace does not install every Plugin. All entries use `AVAILABLE`; none use `INSTALLED_BY_DEFAULT`.

## Validate the catalog

```text
python -m pip install PyYAML
python scripts/validate_catalog.py
python scripts/validate_catalog.py --check-remote
```

The validator checks identifier uniqueness, relationship targets, Marketplace parity, Git-backed source URLs, Plugin manifests, and—when requested—public GitHub availability.

GitHub Projects may be used for roadmap tracking, but this repository remains the source of truth for discovery, installation metadata, and cross-repository relationships.
