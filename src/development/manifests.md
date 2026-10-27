# Pinned manifests

All LieppOS source projects are pinned by full Git SHA with an explicit upstream branch. Nested imgsensor is a separate project at `vendor/mediatek/kernel_modules/mtkcam/imgsensor/src-v4l2`; the parent tracks no files there and ignores the nested checkout.

| Manifest | Scope |
|---|---|
| `local.xml` | local kernel, external modules, tools, device and recovery candidates |
| `default.xml` | intended publication graph; unavailable remotes are explicitly recorded |
| `lineage-22.2/gq5012bf1.xml` | Android 15 full-device local-manifest snippet, not a complete Android base |
| `gsi/lineage-23.2-gsi-pinned.xml` | existing Android 16 GSI snapshot |
| `gsi/lieppos-gsi-overlay.xml` | separate committed LieppOS GSI vendor pin |

## Tested local checkout (new empty directory only)

```bash
repo init -u file:///path/to/android_manifest_lieppos \
  -b main -m local.xml \
  --repo-url file:///path/to/repo \
  --repo-rev <pinned-tag> \
  --no-repo-verify --no-clone-bundle
repo sync -c -j4 --no-clone-bundle
```

Use only a **new empty directory**. The offline repo-tool revision must be pinned to an existing local tag; signature verification is unavailable in a local-tool test, which is not the same as disabling it for a future public setup.

## What was actually verified

Ten projects synced at their pins and passed Git connectivity checks. The kernel manifest needs an explicit `clone-depth` to preserve the server's shallow boundary; without it the first checkout had a missing-parent error. The missing ACK ancestry was **not fabricated**.

A full-device LineageOS base snapshot is still unavailable: the snippet is not a claim that the entire Android 15 source graph is pinned. No GitHub sync success is claimed for unpublished repositories.
