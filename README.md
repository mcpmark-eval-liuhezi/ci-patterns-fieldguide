# CI Patterns Field Guide

A browsable reference of how mature open-source projects configure their GitHub Actions
continuous integration. Every example here was chosen by **reading the actual workflow
files**, not by reputation or star count.

## What this is

This repository collects annotated notes on real-world CI configurations maintained by
other people. Each selected repository demonstrates at least one teachable pattern:

- **Build matrices** across operating systems and language versions
- **Path filtering and change detection** so unrelated commits skip expensive jobs
- **Concurrency and cancellation** so superseded runs do not burn minutes
- **Artifact and digest hand-off** between build and publish jobs
- **Least-privilege permissions** pinned at the workflow level
- **Dependency caching** and disk-space management on constrained runners

## How the examples were chosen

1. **Live research, not memory.** Candidates were found through GitHub code search over
   `.github/workflows/*.yml` files, then each candidate's workflow file was fetched and
   read in full. No repository was selected on the strength of its name or popularity
   alone — several well-known projects were cut after reading their workflows.
2. **One teachable pattern per entry.** A candidate qualified only if a specific,
   quotable technique could be pointed at inside the file — a `matrix:` block, a
   `dorny/paths-filter` job, a `concurrency:` group, a digest-export step, or similar.
   Generic "runs the tests on push" pipelines were rejected.
3. **Maintained by others.** Only repositories owned by third parties were considered.
4. **Coverage across ecosystems.** Python, C, JavaScript/TypeScript, and Go projects are
   all represented, so the patterns are not tied to one toolchain.
5. **Trimmed to the strongest.** From the wider candidate set, the clearest and most
   instructive examples were kept. Every candidate that was cut is recorded, with a
   one-line reason, in the issue tracker — see
   ["Expand coverage beyond the first batch"](../../issues/1).

## Repository layout

- `.github/workflows/ci.yml` — this repository's own CI, triggered on every push. It
  lints the field-guide notes so the repo practices what it preaches.
- `notes/` — one markdown file per selected repository (added via the field-guide pull
  request), each naming the repo as `owner/name`, linking the exact workflow file that
  was read, and summarizing the pattern.

## Using this guide

Read `notes/*.md` top to bottom, then follow each workflow link and read the original
file. The notes deliberately stay short — three to five sentences each — because the
point of the guide is to send you to the real code.
