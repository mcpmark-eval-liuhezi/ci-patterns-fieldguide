# psf/requests — the classic cross-product matrix with exclusions and pip caching

**Repository:** psf/requests
**Workflow file read:** <https://github.com/psf/requests/blob/main/.github/workflows/run-tests.yml>

## The pattern

This is the cleanest example of the textbook build matrix: `runs-on: ${{ matrix.os }}` crossed with eight `python-version` entries — including a free-threaded `3.14t`, a `3.15-dev` pre-release, and `pypy-3.11` — across `ubuntu-22.04`, `macOS-latest`, and `windows-latest`. Two details make it worth teaching from. First, `fail-fast: false` combined with an explicit `exclude:` entry for `pypy-3.11` on Windows, with the reason documented inline (PyPy cannot build `openssl-sys` with Rust on that platform) — showing how to carve known-broken cells out of a matrix rather than deleting a whole row. Second, `actions/setup-python` is configured with `cache: 'pip'`, the supported one-line way to cache dependencies keyed on the lockfile, alongside a 10-minute `timeout-minutes` on the job. The workflow finishes with two small non-matrix jobs, `no_chardet` and `urllib3`, that deliberately uninstall or downgrade an optional dependency before re-running the tests — a pattern for guarding code paths that only trigger when a dependency is absent or old.
