# mastodon/mastodon — distributed multi-platform container builds with digest hand-off

**Repository:** mastodon/mastodon
**Workflow file read:** <https://github.com/mastodon/mastodon/blob/main/.github/workflows/build-container-image.yml>

## The pattern

This is the reference implementation of Docker's "distribute build across multiple runners" strategy for multi-architecture images. A `build-image` job runs one matrix leg per platform (`linux/amd64`, `linux/arm64`) on the matching native runner — `ubuntu-24.04-arm` is selected with `startsWith(matrix.platform, 'linux/arm') && 'ubuntu-24.04-arm' || 'ubuntu-24.04'` — builds with `docker/build-push-action`, and pushes *by digest only*, without any tag. Each leg then exports its digest as an empty marker file and uploads it with `actions/upload-artifact` (`if-no-files-found: error`, `retention-days: 1`), and a downstream `merge-images` job downloads the digest artifacts, recreates the tags with `docker/metadata-action`, and stitches everything into a single manifest list with `docker buildx imagetools create`. Layer caching is scoped so the two platforms never collide: `cache-from`/`cache-to` use `type=gha` with a `scope:` derived from `hashFiles(inputs.file_to_build)` plus the platform pair. The whole file is a reusable workflow triggered by `workflow_call:` with typed inputs (`boolean`, `string`) for `cache`, `push_to_images`, and `file_to_build`, which lets Mastodon's release and nightly workflows share one implementation.
