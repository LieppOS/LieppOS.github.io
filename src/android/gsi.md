# Android 16 GSI

The GSI checkout is LineageOS 23.2 / Android 16 with TrebleDroid, product `tdgsi_arm64_ab`. It is
**not** a GQ5012BF1 full-device checkout and it uses the **stock kernel and vendor contract**.

## Pinned graph

The committed project graph is captured by `gsi/lineage-23.2-gsi-pinned.xml` (1,172 projects);
`gsi/lieppos-gsi-overlay.xml` separately pins `vendor/lieppos`.

Owner changes in scripts, `lieppos.mk`, a personal patch and the local manifest were preserved —
not applied, not reverted. **A committed manifest does not reproduce those dirty changes
automatically.**

## Rules

- Do not add the full-device kernel/module manifest to this checkout.
- Do not run `repo sync` over the preserved dirty state.
- The GSI's `vendor/lieppos` customization is not the device's proprietary vendor tree
  ([Vendor integration](vendor-integration.md)).

See [Manifests](../development/manifests.md) for the separate full-device graph.

> A booting GSI proves that *stock* kernel + vendor support a generic system image. It does **not**
> validate the LieppOS kernel.
