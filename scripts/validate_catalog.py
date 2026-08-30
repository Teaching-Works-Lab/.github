#!/usr/bin/env python3
"""Validate the Teaching Works Lab catalog and curated Codex marketplace."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment guidance
    raise SystemExit("PyYAML is required: python -m pip install -r requirements.txt") from exc


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "catalog.yaml"
MARKETPLACE_PATH = ROOT / ".agents" / "plugins" / "marketplace.json"
ALLOWED_RELATIONS = {
    "generated-artifact",
    "generated-by",
    "optional-companion",
    "optional-input",
    "optional-input-to",
}


def load_catalog() -> dict:
    with CATALOG_PATH.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError("catalog.yaml must contain a mapping")
    return data


def load_marketplace() -> dict:
    with MARKETPLACE_PATH.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("marketplace.json must contain an object")
    return data


def public_url(url: str) -> str:
    return url.removesuffix(".git")


def fetch_json(url: str) -> dict:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "teaching-works-lab-catalog-validator",
        },
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


def validate(check_remote: bool) -> list[str]:
    errors: list[str] = []
    catalog = load_catalog()
    marketplace = load_marketplace()

    if catalog.get("schema_version") != 1:
        errors.append("catalog schema_version must be 1")
    if marketplace.get("name") != catalog.get("marketplace", {}).get("name"):
        errors.append("catalog and marketplace names differ")

    items = catalog.get("items")
    plugins = marketplace.get("plugins")
    if not isinstance(items, list) or not items:
        errors.append("catalog items must be a non-empty list")
        return errors
    if not isinstance(plugins, list) or not plugins:
        errors.append("marketplace plugins must be a non-empty list")
        return errors

    ids = [item.get("id") for item in items]
    plugin_names = [item.get("plugin_name") for item in items]
    market_names = [plugin.get("name") for plugin in plugins]
    if len(ids) != len(set(ids)):
        errors.append("catalog item ids must be unique")
    if len(plugin_names) != len(set(plugin_names)):
        errors.append("catalog plugin names must be unique")
    if len(market_names) != len(set(market_names)):
        errors.append("marketplace plugin names must be unique")
    if set(plugin_names) != set(market_names):
        errors.append("catalog plugin names and marketplace entries must match")

    item_by_plugin = {item.get("plugin_name"): item for item in items}
    known_ids = set(ids)

    for item in items:
        item_id = item.get("id", "<missing-id>")
        required = ["type", "repository", "plugin_name", "role", "scope"]
        for field in required:
            if not item.get(field):
                errors.append(f"{item_id}: missing {field}")
        install = item.get("install", {})
        if install.get("policy") != "AVAILABLE":
            errors.append(f"{item_id}: install policy must be AVAILABLE")
        if install.get("auto_installs") != []:
            errors.append(f"{item_id}: auto_installs must remain an empty list")
        triggers = item.get("skills", {}).get("explicit_triggers")
        if not isinstance(triggers, list) or not triggers:
            errors.append(f"{item_id}: explicit_triggers must be a non-empty list")
        for trigger in triggers or []:
            if not isinstance(trigger, str) or not trigger.startswith("$"):
                errors.append(f"{item_id}: invalid explicit trigger {trigger!r}")
        for relation in item.get("relations", []):
            relation_type = relation.get("type")
            target = relation.get("target")
            if relation_type not in ALLOWED_RELATIONS:
                errors.append(f"{item_id}: unsupported relation type {relation_type!r}")
            if target not in known_ids:
                errors.append(f"{item_id}: unknown relation target {target!r}")
            if relation.get("required") is not False:
                errors.append(f"{item_id}: cross-repository relations must remain optional")

    for plugin in plugins:
        name = plugin.get("name", "<missing-name>")
        source = plugin.get("source", {})
        policy = plugin.get("policy", {})
        if source.get("source") != "url":
            errors.append(f"{name}: marketplace source must be url")
        expected_repo = item_by_plugin.get(name, {}).get("repository")
        if public_url(source.get("url", "")) != expected_repo:
            errors.append(f"{name}: marketplace URL does not match catalog repository")
        if source.get("ref") != "main":
            errors.append(f"{name}: marketplace ref must be main")
        if policy.get("installation") != "AVAILABLE":
            errors.append(f"{name}: marketplace installation must be AVAILABLE")
        if policy.get("authentication") != "ON_INSTALL":
            errors.append(f"{name}: marketplace authentication must be ON_INSTALL")
        if plugin.get("category") != "Education":
            errors.append(f"{name}: marketplace category must be Education")

        if check_remote and expected_repo:
            api_base = expected_repo.replace(
                "https://github.com/", "https://api.github.com/repos/"
            )
            try:
                repository = fetch_json(api_base)
                if repository.get("private") is not False:
                    errors.append(f"{name}: repository is not public")
                if repository.get("default_branch") != "main":
                    errors.append(f"{name}: default branch is not main")
                manifest = fetch_json(
                    f"{api_base}/contents/.codex-plugin/plugin.json?ref=main"
                )
                if manifest.get("type") != "file":
                    errors.append(f"{name}: public plugin manifest is missing")
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
                errors.append(f"{name}: remote validation failed: {exc}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check-remote",
        action="store_true",
        help="also verify public GitHub repositories and plugin manifests",
    )
    args = parser.parse_args()

    try:
        errors = validate(check_remote=args.check_remote)
    except (OSError, ValueError, json.JSONDecodeError, yaml.YAMLError) as exc:
        print(f"catalog validation failed: {exc}", file=sys.stderr)
        return 1

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    suffix = " including public GitHub manifests" if args.check_remote else ""
    print(f"Catalog validation passed for 5 plugins{suffix}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
