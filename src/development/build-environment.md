# Build environment and output ownership

Kernel source and build outputs are separate. Heavy builds use authorized isolated ext4 output directories, never the original dev21 or Codex output trees.

## Safety gates

| Gate | Value |
|---|---|
| Btrfs metadata hard floor | **4 GiB** |
| Conservative Btrfs heavy-build restart threshold | **6 GiB** |
| General free-space floor | **25 GiB**, including projected post-operation use |
| Filesystem error counters | must remain zero |
| Mutable output directory | one owner, one live controller |

## Output layout

Future immutable outputs live under `$BUILD_ROOT/gq5012bf1/kernel/<line>/<build-id>/`. `$BUILD_ROOT` is a maintainer-local path variable; the concrete host location is deliberately not published.

Each receipt records: source commits, declared overlays, effective config, compiler identity, build invocation, module hashes/classification, DT hashes and offline verification status. Historical output directories are **not** moved.

## Toolchain

Android clang/LLD **17.0.2** (`clang-r487747c`), with recorded binary hashes; pahole 1.32.

## Documentation tooling

mdBook builds this site from `src/`. Editing requires adding a page **and** a `SUMMARY.md` entry. No global package installation is needed for the research work described here.
