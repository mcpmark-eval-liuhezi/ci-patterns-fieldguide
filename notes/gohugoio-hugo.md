# gohugoio/hugo — adapting an OS matrix to hostile runner environments

**Repository:** gohugoio/hugo
**Workflow file read:** <https://github.com/gohugoio/hugo/blob/master/.github/workflows/test.yml>

## The pattern

On the surface this is a plain `matrix` of `os: [ubuntu-latest, windows-latest]`, but the valuable part is everything the workflow does to make that matrix survive the runners. On Ubuntu it runs `jlumbroso/free-disk-space` to clear tool caches, Docker images, and large packages before Hugo's build; on Windows it moves `GOCACHE`, `GOMODCACHE`, `GOTMPDIR`, `TMP`, and `TEMP` off the cramped `C:` drive by writing them to `$GITHUB_ENV`, and disables `actions/setup-go`'s build cache entirely with a comment noting that restoring it on Windows is slow and eats disk. Per-OS tool installation is handled with `if:`-guarded steps that install pandoc via `apt`, `brew`, or `choco`, and the dart-sass binary is downloaded with a pinned `sha256` checksum per platform before being added to `PATH` — supply-chain hygiene applied to a downloaded tool, not just to `uses:` references. The matrix uses `go-version: [1.27.x]` so patch releases float while the minor is fixed, and the test step itself branches by OS because Hugo disables `-race` on Windows, with the reason cited as issue #11052. It is the best available example of how a two-line matrix quietly implies a dozen platform-conditional workarounds.
