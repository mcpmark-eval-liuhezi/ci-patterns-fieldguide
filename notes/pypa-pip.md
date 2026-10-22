# pypa/pip — path-filtered jobs, disciplined matrices, concurrency cancellation

**Repository:** pypa/pip
**Workflow file read:** <https://github.com/pypa/pip/blob/main/.github/workflows/ci.yml>

## The pattern

pip gates nearly every expensive job behind a `determine-changes` job that runs `dorny/paths-filter`, so a vendoring-only or docs-only pull request skips the test matrix entirely — the output booleans are then consumed by `if:` conditions that also allow the job to run on non-PR events like schedule and manual dispatch. The Unix test matrix pairs `os: [ubuntu-latest, macos-latest]` with six Python versions plus a free-threaded `3.14t` build, and uses `include:` to pin the *oldest patch release* of each minor version on Linux to catch backport regressions. The Windows job takes a different shape on purpose: it is sharded into three `group: [1, 2, 3]` legs because Windows runners are slow, and a comment explains that tests are split by a stable hash of each test's node id. A workflow-level `concurrency:` group cancels superseded runs per PR number, `permissions: contents: read` scopes the token, and every `uses:` is pinned by full commit SHA rather than a floating tag.
