# Python Application Template

This repository is the **CloudOps Works Python application template** for bootstrapping a new Python service with sample Flask application code, pytest-based tests, GitHub Actions, and CloudOps Works delivery wiring already in place.

Use this template when you want a repository that already includes:

- a minimal Python application scaffold
- sample Flask routes and application factory layout
- pytest-based test examples
- CloudOps Works CI/CD configuration under `.cloudopsworks/`
- GitHub Actions workflows for PR validation, build, scan, release, and deploy
- deployment templates for Kubernetes, Lambda, Elastic Beanstalk, App Engine, Cloud Run, or library-only publishing

---

## What gets generated from this template

### Application scaffold
- `pyproject.toml` — base Python project metadata with placeholder package name and version
- `requirements.txt` — runtime dependency list (Flask by default)
- `main.py` — local application entrypoint
- `app/__init__.py` — Flask application factory
- `app/routes.py` — sample HTTP and JSON routes
- `__tests__/` — pytest examples for the sample routes
- `apifiles/` — API definition placeholders and samples
- `Makefile` — bootstrap and GitVersion-backed version helper targets

### Delivery scaffold
- `.cloudopsworks/cloudopsworks-ci.yaml` — repository governance and deployment routing
- `.cloudopsworks/vars/inputs-global.yaml` — global build/deploy defaults
- `.cloudopsworks/vars/inputs-*.yaml` — deployment-target templates
- `.cloudopsworks/vars/preview/` — preview-environment defaults when enabled
- `.cloudopsworks/vars/apigw/` — API Gateway templates when APIs are published
- `.cloudopsworks/_VERSION` — template version tracked by release automation
- `.cloudopsworks/gitversion_gitflow.yaml` — explicit GitFlow reference configuration
- `.cloudopsworks/gitversion_githubflow.yaml` — explicit GitHub Flow reference configuration
- `.github/workflows/` — reusable CI/CD orchestration

---

## Recommended bootstrap flow

### 1. Create a repository from this template
Create a new repository from `cloudopsworks/python-app-template`, then clone it locally.

### 2. Initialize the Python project metadata
From the root of the generated repository, run:

```bash
make code/init
```

This target updates `pyproject.toml` to:
- set `project.name` to the current directory name
- set the project version to `MajorMinorPatch` derived from GitVersion

### 3. Replace the placeholder Python metadata
`make code/init` does not finish the project definition for you. Review and replace at least:

- `project.name`
- `project.version`
- `project.description`
- `project.requires-python`
- authors, URLs, license, classifiers, and optional dependencies as needed

If you are not using plain `requirements.txt`, extend `pyproject.toml` to reflect your packaging strategy.

### 4. Replace the sample application code
The template includes Flask sample code so the build and tests work immediately.
Replace it with your actual application code:

- update `app/__init__.py` to configure your application
- replace `app/routes.py` sample routes with your real endpoints
- update `main.py` if your runtime entrypoint changes
- remove or replace the sample API files in `apifiles/` if they do not apply

### 5. Update dependencies and tests
Review and adjust:

- `requirements.txt` for runtime dependencies
- test dependencies/tooling in your local environment or CI configuration
- `__tests__/` to match your real application behavior

### 6. Verify the repository locally
Create an environment, install dependencies, then run the sample checks:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt pytest
pytest
make version
```

`make version` writes a `VERSION` file and updates `pyproject.toml` using GitVersion semantics.

To run the sample app locally:

```bash
python main.py
```

The sample Flask app listens on port `8080`.

---

## Template customization guide

### `pyproject.toml`
Review the generated project metadata before the first PR:

- choose the final package or service name
- set the correct Python version support
- add a real description and project metadata
- decide whether to keep a minimal metadata-only file or expand it for packaging, tooling, and optional dependency groups
- align the versioning strategy with your release process

### `requirements.txt`
Use this file for runtime dependencies unless you intentionally standardize on another dependency workflow.

Typical actions:
- replace Flask if the service uses a different framework
- add production dependencies
- keep test-only tools out of runtime requirements unless your process intentionally couples them

### Application structure
The default structure is intentionally simple:

- `main.py` starts the app
- `app/__init__.py` builds the Flask application
- `app/routes.py` defines example routes
- `__tests__/` demonstrates route tests with pytest

You can keep this layout or evolve it into modules such as `config/`, `services/`, `models/`, `schemas/`, or `api/` as the service grows.

### `README.md`
Replace the minimal placeholder with repository-specific documentation:

- what the service does
- how to install dependencies
- how to run it locally
- how to run tests and lint/type checks
- runtime or deployment assumptions
- required environment variables or credentials
- API or operational references

### `.cloudopsworks/cloudopsworks-ci.yaml`
This file controls repository governance and deployment routing.

Update these sections first:

#### `config`
- `branchProtection` — enable/disable branch protection automation
- `gitFlow.enabled` — keep `true` when using GitFlow branch conventions
- `gitFlow.supportBranches` — enable only if you maintain long-lived support branches
- `requiredReviewers`, `reviewers`, `owners`, `contributors` — repository governance

#### `cd.deployments`
This maps branch/tag flows to deployment environments.

Default mapping in this template:
- `develop` -> `dev`
- `release/**` -> `prod`
- internal `test` stage -> `uat`
- prerelease tags -> `demo`
- `hotfix` -> `hotfix`
- optional `support` mappings by version match

Adjust the environment names and routing rules to match your promotion model.

### `.cloudopsworks/vars/inputs-global.yaml`
This is the main global configuration file used by the workflows.

Set these values before the first pipeline run:
- `organization_name`
- `organization_unit`
- `environment_name`
- `repository_owner`
- `cloud`
- `cloud_type`

Common optional sections:
- `python` — Python version, dependency manager mode, pytest/unittest selection, optional Ruff and mypy toggles, image variant, install arguments
- `preview` — PR preview configuration
- `apis` — API Gateway deployment toggle
- `observability` — tracing/monitoring agent configuration
- `snyk`, `semgrep`, `trivy`, `sonarqube`, `dependencyTrack` — security and quality tooling
- `docker_inline`, `docker_args`, `custom_run_command`, `custom_usergroup` — container customization
- `is_library` — artifact-only mode
- `api_files_dir` — custom path for API definitions
- `python_extra_env` — extra environment variables used during image build/runtime bootstrap

---

## Choose a deployment target

Each active environment should use exactly one matching deployment-target file under `.cloudopsworks/vars/`.

### Kubernetes / EKS / AKS / GKE
Use `inputs-KUBERNETES-ENV.yaml`.

Key fields:
- `container_registry`
- `cluster_name`
- `namespace`
- target-cloud credentials/settings
- optional Helm, secret, and external-secret overrides

### AWS Lambda
Use `inputs-LAMBDA-ENV.yaml`.

Key fields:
- `versions_bucket`
- `aws.region`
- `lambda.runtime`
- `lambda.handler`
- IAM, VPC, trigger, schedule, layer, and concurrency configuration

### AWS Elastic Beanstalk
Use `inputs-BEANSTALK-ENV.yaml`.

Key fields:
- `versions_bucket`
- `container_registry`
- `aws.region`
- Beanstalk platform, instance, networking, and port mappings

### Google App Engine
Use `inputs-APPENGINE.yaml`.

Key fields:
- `container_registry`
- `gcp.region`
- `gcp.project_id`
- `appengine.runtime`
- `appengine.type`
- `appengine.entrypoint_shell`

### Google Cloud Run
Use `inputs-CLOUDRUN.yaml`.

Key fields:
- `container_registry`
- `gcp.region`
- `gcp.project_id`
- `cloudrun.type`
- optional scaling, environment variables, secrets, probes, VPC, volume, and trigger configuration

### Library / no-deploy mode
Use `inputs-LIB-ENV.yaml` when the repository should publish artifacts but not deploy runtime infrastructure.

---

## Optional features

### Preview environments
Preview environments are configured from:
- `.cloudopsworks/vars/preview/inputs.yaml`
- `.cloudopsworks/vars/preview/values.yaml`

Enable them in `inputs-global.yaml`:

```yaml
preview:
  enabled: true
```

Use preview environments when pull requests from `feature/**` or `hotfix/**` should deploy isolated review environments.

### API Gateway publication
If the service publishes APIs, configure:
- `.cloudopsworks/vars/apigw/apis-global.yaml`
- `.cloudopsworks/vars/apigw/apis-dev.yaml`
- `.cloudopsworks/vars/apigw/apis-uat.yaml`
- `.cloudopsworks/vars/apigw/apis-prod.yaml`

Enable API deployment in `inputs-global.yaml`:

```yaml
apis:
  enabled: true
```

API definitions are read from `apifiles/` unless `api_files_dir` overrides the path.

### Helm values overrides
For Kubernetes targets, environment-specific Helm overrides live in:
- `.cloudopsworks/vars/helm/values-dev.yaml`
- `.cloudopsworks/vars/helm/values-uat.yaml`
- `.cloudopsworks/vars/helm/values-prod.yaml`

Use them to override ingress, probes, resources, autoscaling, environment variables, and other chart-level behavior without editing the blueprint chart.

### Optional quality tooling
The template can enable additional quality gates through `inputs-global.yaml`, including:

- Ruff
- mypy
- SonarQube
- Snyk
- Semgrep
- Trivy
- Dependency-Track

Turn on only the tools your repository is ready to maintain.

---

## GitHub Actions workflow model

Important workflows in this template:

- `main-build.yml` — build, test, package/containerize, scan, and release/deploy on branch/tag events
- `pr-build.yml` — PR validation and optional preview deployment
- `deploy-container.yml` — push application container artifacts
- `deploy.yml` — standard deployment flow
- `deploy-blue-green.yml` — blue/green deployment flow
- `scan.yml` — SAST/SCA orchestration
- `environment-unlock.yml` / `environment-destroy.yml` — environment operations
- `automerge.yml`, `process-owners.yml`, Jira integration workflows, and slash-command workflows — repository automation
- `pr-close.yaml` — post-merge/tag cleanup actions

---

## Upgrading from the Template

Repositories derived from this template stay in sync with upstream releases using the
`make repos/upgrade*` targets. An agent asked to "upgrade", "update from template",
"sync with template", "apply template changes", or "bump template version" should use
these targets — never fetch or apply template changes manually.

### Available upgrade targets

| Target | When to use |
|---|---|
| `make repos/upgrade` | **Default — patch upgrade.** Pulls the latest patch within the **same minor version**. No breaking changes. Use for routine maintenance. |
| `make repos/upgrade/major` | Pulls the latest release within the **same major version**. May include workflow-level changes. |
| `make repos/upgrade/master` | Pulls from the template's `master` branch tip. Use only when explicitly asked to track the latest unreleased template state. |
| `make repos/upgrade/dev` | Pulls from the template's `develop` branch. Use only for pre-release or preview upgrades. |
| `make repos/available` | Lists the latest available patch and major versions without modifying anything. Run this first to see what is available. |

### Upgrade workflow for agents

1. Run `make repos/available` to see the current and latest available versions.
2. Choose the appropriate target (default: `make repos/upgrade` for a routine patch upgrade).
3. Review the diff — the upgrade overwrites `.github/workflows/` and selected `.cloudopsworks/` metadata; application source files are never touched.
4. Commit the result with: `chore: upgrade from <template-name> <old-version> → <new-version> +semver: patch`
5. Use `/cw-release` to create and merge the hotfix PR (see [Release Workflow — use `cw-release`](#release-workflow--use-cw-release)).

> **Note:** `Makefile`, `.github/`, `.cloudopsworks/labeler.yml`, `.cloudopsworks/Makefile`,
> and `.cloudopsworks/LICENSE` are owned by the template and will be overwritten on every upgrade.
> Do not edit these files manually in derived repositories.

---

## AI-assisted upgrade of `.cloudopsworks/vars` configuration files

This section is a machine-readable protocol for AI agents performing a seamless, non-destructive upgrade of all configuration files under `.cloudopsworks/vars/` when a new template version is released. Follow the steps below in order.

### Upgrade overview

The template version locked into this repository is recorded in `.cloudopsworks/_VERSION`. The canonical upstream source is the GitHub repository `cloudopsworks/python-app-template`, pinned to the tag that matches the content of `_VERSION`.

An upgrade merges new keys, updated comments, and structural changes from the upstream template into local files **without overwriting values the operator has already set**.

---

### Step 1 — determine current and target versions

1. Read `.cloudopsworks/_VERSION` to get the **current locked version** (e.g., `v1.4.15`).
2. The **target version** is either supplied by the operator or is the latest release tag on `cloudopsworks/python-app-template`.
3. Fetch any upstream file from GitHub using the pattern:
   ```
   https://raw.githubusercontent.com/cloudopsworks/python-app-template/<version>/<path>
   ```
   Example:
   ```
   https://raw.githubusercontent.com/cloudopsworks/python-app-template/v1.4.15/.cloudopsworks/vars/inputs-global.yaml
   ```

---

### Step 2 — identify the deployment type for each environment file

Each `inputs-<name>.yaml` file under `.cloudopsworks/vars/` maps to a specific upstream template. Determine the type using the following priority order:

**Priority 1 — `Agents:` header comment**

If the file contains an `# Agents:` line in its header block, read `cloud` and `cloud_type` directly from it:

```yaml
# Agents: cloud=aws ; cloud_type=lambda
```

Multiple valid combinations may be listed separated by `|`:

```yaml
# Agents: cloud=aws|gcp|azure ; cloud_type=kubernetes
```

**Priority 2 — fallback to `inputs-global.yaml`**

If no `# Agents:` line is present, read the active `cloud` and `cloud_type` values from `.cloudopsworks/vars/inputs-global.yaml` and apply the mapping table below.

**`cloud` / `cloud_type` → upstream template file:**

| `cloud`                  | `cloud_type`                   | Upstream template file         |
|--------------------------|--------------------------------|--------------------------------|
| `aws`                    | `eks` or `kubernetes`          | `inputs-KUBERNETES-ENV.yaml`   |
| `azure`                  | `aks` or `kubernetes`          | `inputs-KUBERNETES-ENV.yaml`   |
| `gcp`                    | `gke` or `kubernetes`          | `inputs-KUBERNETES-ENV.yaml`   |
| `aws`                    | `lambda`                       | `inputs-LAMBDA-ENV.yaml`       |
| `aws`                    | `beanstalk`                    | `inputs-BEANSTALK-ENV.yaml`    |
| `gcp`                    | `appengine`                    | `inputs-APPENGINE.yaml`        |
| `gcp`                    | `cloudrun`                     | `inputs-CLOUDRUN.yaml`         |
| `aws` / `gcp` / `azure`  | `none` or library mode         | `inputs-LIB-ENV.yaml`          |

`inputs-global.yaml` always maps to the upstream `inputs-global.yaml` regardless of cloud type.

---

### Step 3 — upgrade deployment target files

The deployment target files identified by the Step 2 mapping table — such as `inputs-KUBERNETES-ENV.yaml`, `inputs-LAMBDA-ENV.yaml`, `inputs-BEANSTALK-ENV.yaml`, `inputs-APPENGINE.yaml`, `inputs-CLOUDRUN.yaml`, `inputs-LIB-ENV.yaml`, and mobile equivalents such as `inputs-ANDROID-ENV.yaml` and `inputs-XCODE-ENV.yaml` — are **scaffolding templates**. They provide placeholder structures and documented examples, not finalized operator configuration.

**Do not merge these files. Overwrite them.**

Upgrade procedure for each deployment target file:

1. **Before overwriting** — inspect the local file and record any operator-configured values (keys that have been uncommented and set to non-placeholder values).
2. **Replace the file** — overwrite the local file entirely with the upstream template version.
3. **Re-apply operator values** — after overwriting, set each previously recorded operator-configured value at its corresponding key in the new file.
4. **Copy in absent files** — if a deployment target file is present in the upstream template but absent locally, copy it in from the upstream template as a new file.

---

### Step 4 — merge `inputs-global.yaml`

`inputs-global.yaml` requires special handling because it contains mandatory operator identity fields alongside a large body of optional commented-out sections.

Merge procedure:

1. **Retain the four mandatory identity fields** verbatim at the top of the file:
   ```yaml
   organization_name: "..."
   organization_unit: "..."
   environment_name: "..."
   repository_owner: "..."
   ```
2. **Retain `cloud` and `cloud_type`** exactly as the operator set them.
3. **For every optional commented-out section** in the upstream template, check the local file:
   - If the operator **has uncommented and configured it** — keep the operator's values; update only surrounding comment text if it changed upstream.
   - If the section **is still fully commented out locally** — replace the entire commented block with the upstream version, capturing any new fields or updated documentation within it.
4. **Append new optional sections** that appear in the upstream template but are entirely absent locally, in fully commented-out form, preserving their upstream position and comments.

---

### Step 5 — upgrade subdirectory files

Apply the merge rules from Step 4 to every file in the following subdirectories, matching each local file to its corresponding upstream file at the same relative path:

- `.cloudopsworks/vars/preview/inputs.yaml`
- `.cloudopsworks/vars/preview/values.yaml`
- `.cloudopsworks/vars/apigw/apis-global.yaml`
- `.cloudopsworks/vars/apigw/apis-dev.yaml`
- `.cloudopsworks/vars/apigw/apis-uat.yaml`
- `.cloudopsworks/vars/apigw/apis-prod.yaml`
- `.cloudopsworks/vars/helm/values-dev.yaml`
- `.cloudopsworks/vars/helm/values-uat.yaml`
- `.cloudopsworks/vars/helm/values-prod.yaml`

---

### Step 6 — update `_VERSION`

After all merges are verified correct, write the target version string (e.g., `v1.4.16`) to `.cloudopsworks/_VERSION`. This is the final step.

---

### Upgrade invariants

An agent performing this upgrade must **never**:

- Overwrite a field the operator has explicitly set to a non-placeholder value.
- Remove a commented-out operator value without first reporting it.
- Change the YAML structure of any active (uncommented) operator section.
- Alter a file's opening description comment (`# This file contains...`) unless the upstream version changed it.
- Modify `.cloudopsworks/cloudopsworks-ci.yaml`, `gitversion_*.yaml`, or any file under `.github/workflows/` as part of a vars upgrade — those follow their own upgrade path.
- Update `_VERSION` before all file merges are complete.

---

### Conflict resolution

When a merge cannot be resolved automatically (for example, the upstream template restructured a section that the operator has customized):

1. Emit a diff showing both the upstream template block and the local operator block side by side.
2. Pause and present the conflict to the operator, asking which version to keep or whether a manual merge is needed.
3. Never silently choose one side.

---

## Suggested first follow-up tasks after generating a repo

1. Replace the sample Flask code with your real service.
2. Populate `README.md` with project-specific instructions.
3. Set `inputs-global.yaml` and exactly one deployment-target file for each environment.
4. Add lint/type-check tooling if your team standard requires it.
5. Run the first PR through CI before enabling production deployment routes.

---

## Release Workflow — use `cw-release`

All releases **must** be performed using the `cw-release` skill from the CloudOps Works skill set. Do **not** create release branches, hotfix branches, version tags, or release PRs manually — the skill owns the full GitFlow-aware release lifecycle for this repository.

### When to invoke `cw-release`

Use it whenever you are asked to:
- Release, ship, or publish a new version (patch, minor, or major)
- Create a hotfix or patch release
- Create a release branch or feature-merge PR
- Tag and publish a version

### How to run it

In Claude Code (CLI, IDE extension, or web):

```
/cw-release
```

### What the skill does

1. Detects the GitVersion flow in use (`gitversion_gitflow.yaml` or `gitversion_githubflow.yaml`).
2. Reads the repo-local release policy from `.cloudopsworks/cloudopsworks-ci.yaml`.
3. Drives the shared tronador `make` / `gh` release path end-to-end.
4. Creates the correct branch, PR, tag, and GitHub Release in the right sequence.

> **Do not** run `git tag`, `gh release create`, or `make release` directly. Always let `cw-release` orchestrate these steps to keep version history and CI consistent.
