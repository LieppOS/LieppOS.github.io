# Getting started

1. Read [Current status](../project/status.md), [Provenance](../research/provenance.md) and the [Build environment](build-environment.md).
2. Choose **either** the Android 16 GSI **or** the Android 15 full-device workflow; never combine their manifests.
3. Use a new authorized workspace. Do not overwrite historical outputs or synchronize over dirty owner work.
4. Validate the source lock and local source graph before compiling.
5. Read the build receipt and acceptance boundaries before interpreting a successful build.

The local manifest repository is `android_manifest_lieppos`; until publication is authorized, use its `local.xml` against the preserved local candidates. [Manifests](manifests.md) lists the tested commands.

## Destructive scripts — do not run

`dk12/build-image.sh`, `make-device-tree.sh` and `build-vendor-targetC.sh` are destructive reconstruction scripts, **not** build entry points. Their guards deliberately refuse execution. Use the LieppOS build engine instead.

> Building is not booting. Nothing here produces a deployable image.
