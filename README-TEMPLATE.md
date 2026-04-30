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

## Suggested first follow-up tasks after generating a repo

1. Replace the sample Flask code with your real service.
2. Populate `README.md` with project-specific instructions.
3. Set `inputs-global.yaml` and exactly one deployment-target file for each environment.
4. Add lint/type-check tooling if your team standard requires it.
5. Run the first PR through CI before enabling production deployment routes.
