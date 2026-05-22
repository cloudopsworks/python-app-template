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

### Step 3 — merge environment-specific files

For each `inputs-<name>.yaml`, apply all of the following rules.

#### Keys and values

- **Preserve operator-set values** — any key whose local value differs from the upstream template's placeholder or default must be kept exactly as-is.
- **Add missing keys** — keys present in the upstream template but absent locally must be inserted at the correct structural position using the upstream default value and comment.
- **Flag removed keys** — keys present locally but deleted from the upstream template must be reported to the operator before removal; do not silently delete them.

#### Comments

- **Template comments are authoritative for unchanged sections** — section-level and field-level comments from the upstream template replace their local equivalents when the operator has made no additions to that comment block.
- **Preserve operator-added comments** — any comment not present in the upstream template must be retained verbatim.
- **Update the `Agents:` header line** — if the upstream template added or changed the `# Agents:` metadata line, update it in the local file without altering the first description line (`# This file contains...`).

#### Formatting

- **Match upstream indentation and quoting** — indentation, block vs. flow style, and quoted vs. unquoted strings must match the upstream template for any unchanged or newly added sections.
- **Commented-out blocks** — blocks that are commented out in the upstream template must remain commented out unless the operator has explicitly uncommented them locally.
- **Multiline scalars** — preserve the operator's choice of `|` vs. `>` for any multiline value the operator has set.

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

Apply the same merge rules (Steps 3 and 4) to every file in the following subdirectories, matching each local file to its corresponding upstream file at the same relative path:

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
