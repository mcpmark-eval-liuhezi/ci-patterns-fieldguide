# curl/curl — a matrix of build configurations, not just versions

**Repository:** curl/curl
**Workflow file read:** <https://github.com/curl/curl/blob/master/.github/workflows/linux.yml>

## The pattern

Where most matrices vary an OS and a compiler version, curl's `linux.yml` varies an entire *build configuration*: each `matrix.build` entry is an object carrying a `name`, apt `install_packages`, `install_steps`, CMake `generate:` or autotools `configure:` flags, plus optional `CC`, `LDFLAGS`, and `tflags`. That single mechanism lets the file express dozens of scenarios — AWS-LC, BoringSSL, LibreSSL, mbedTLS, wolfSSL, rustls-ffi — with clang, valgrind, and Fil-C variants, and even ARM64 runners via per-entry `image:` values like `ubuntu-24.04-arm`. Two guardrails wrap the matrix: `fail-fast: false` so one TLS backend failure does not cancel the others, and slow test suites are sharded with `tflags: '--subset=0/2'` and `'--subset=1/2'`. The header is equally instructive — `permissions: {}` (an even stricter statement than `contents: read`), `cache-mode: write`, a per-PR `concurrency:` group with `cancel-in-progress`, and `paths-ignore:` entries that skip the whole workflow for non-code changes. Version-sensitive dependencies are centralized in a top-level `env:` block annotated with renovate directives, so each pinned third-party version is both visible and automatically updatable.
