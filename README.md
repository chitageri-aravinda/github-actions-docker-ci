# github-actions-docker-ci

[![CI](https://github.com/chitageri-aravinda/github-actions-docker-ci/actions/workflows/ci.yml/badge.svg)](https://github.com/chitageri-aravinda/github-actions-docker-ci/actions/workflows/ci.yml)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat&logo=githubactions&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)

A CI pipeline built with **GitHub Actions** that lints, tests, builds, security-scans and publishes a Docker image. The sample app is a small Python HTTP service with no external dependencies, so the focus stays on the pipeline.

## Pipeline

```
push / pull request
        |
   [ test ]  flake8 lint + unit tests
        |
   [ build ] build image -> Trivy scan -> push to GHCR (main only)
```

| Stage | What it does |
|---|---|
| **Lint** | `flake8` checks code style |
| **Test** | `unittest` covers the greeting function and the HTTP endpoints |
| **Build** | Docker Buildx builds the image with GitHub Actions layer caching |
| **Scan** | Trivy fails the build on fixable CRITICAL or HIGH vulnerabilities |
| **Publish** | On pushes to `main`, the image goes to GitHub Container Registry, tagged with the short commit SHA and `latest` |

Pull requests run lint, test, build and scan, but never publish.

## Project layout

```
app/                  # Python service (/ and /health endpoints)
tests/                # Unit tests
Dockerfile            # Non-root image with a health check
.github/workflows/ci.yml
```

## Run locally

```bash
# Tests
python -m unittest discover -s tests -v

# Run the service
python -m app.main
curl localhost:8080/health

# Or with Docker
docker build -t github-actions-docker-ci .
docker run -p 8080:8080 github-actions-docker-ci
```

## Design notes

- **Least-privilege tokens:** the workflow defaults to read-only, and only the build job gets `packages: write`.
- **No stored credentials:** publishing uses the built-in `GITHUB_TOKEN`.
- **Scan before publish:** a vulnerable image never reaches the registry.
- **Non-root container** with a built-in health check.

## Ideas to extend

- Deploy the image to Cloud Run or GKE (using Workload Identity Federation for keyless auth)
- Update an image tag in a GitOps repo so Argo CD rolls it out
- Add Dependabot for action and base-image updates

## License

MIT
