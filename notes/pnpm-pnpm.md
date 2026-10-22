# pnpm/pnpm — reusable workflows, artifact hand-off, and merge-queue handling

**Repository:** pnpm/pnpm
**Workflow file read:** <https://github.com/pnpm/pnpm/blob/main/.github/workflows/ci.yml>

## The pattern

pnpm's `TS CI` workflow separates a fast `compile-and-lint` job from the test matrix and passes work between them as an artifact: the compile job tars up its compiled `lib/` directories and `.tsbuildinfo` files, uploads them with `actions/upload-artifact`, and the test jobs download and reuse them instead of recompiling — with a tight `retention-days: 1`, since the artifact only needs to outlive the run. The most quotable lesson is the decision *not* to use a matrix for the `pnpr` binary builds: the file carries a comment explaining that `needs:` can only gate on a whole job, never an individual matrix leg, so a single matrix build would make the Linux tests wait for the slower Windows build — instead each OS calls its own reusable workflow via `uses:`, letting each platform's tests gate only on their own build. The trigger block is also unusual and well-reasoned: `push` is restricted to `main` because a same-repo branch would otherwise fire both a `push` and `pull_request` run for one commit and report two results for the same required check. A `merge_group` trigger forces the full suite in the merge queue, because a skipped job never reports its check context and would leave the queue waiting forever, and the concurrency group keys on the event name so PRs cancel superseded runs without killing push runs.
