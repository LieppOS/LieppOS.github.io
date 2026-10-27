# Understanding evidence

Every claim on this site carries an evidence label. The labels are **not**
interchangeable success states: a compile result, a descriptor check, a source
comparison and a hardware observation are different kinds of knowledge, and
they are never promoted into one another.

## The labels

| Label | Meaning | What it does **not** prove |
|---|---|---|
| **VERIFIED ON DEVICE** | Observed on the physical GQ5012BF1, almost always on **stock** firmware. | That the same behaviour occurs under a LieppOS-built kernel. |
| **VERIFIED OFFLINE** | Established from authenticated images or captures, or from a reproducible local build and verification run. | Hardware behaviour, bootloader acceptance, or that Android starts. |
| **SOURCE-LEVEL VERIFIED** | Established by reading source, a device tree, a configuration symbol or a manifest. | That the code ever executes, or that the value is right for this board. |
| **STRONG INFERENCE** | Several independent observations converge, but no direct measurement exists. | Fact. A strong inference can still be wrong. |
| **EXPERIMENTAL** | Exercised outside any supported configuration and kept as forensic evidence. | Support, roadmap status, or fitness for use. |
| **MANUFACTURER CLAIM** | Stated by Ulefone or MediaTek product or marketing material. | Electrical or software reality. |
| **UNKNOWN** | Not established. Recorded explicitly so that the gap stays visible. | — |
| **PLANNED** | Intended work that does not exist yet. | Availability. A planned repository is not a published one. |

Where a page cites an earlier convention, **SOURCE-LEVEL** is shorthand for
**SOURCE-LEVEL VERIFIED**, and "manufacturer marketing name" is shorthand for
**MANUFACTURER CLAIM**. Neither shorthand weakens the rule that the claim has
only the strength its label describes.

## Three rules that are easy to break

1. **A successful kernel compilation is not proof that a driver works on the
   phone.** Building shows that source and configuration agree; it says nothing
   about a probe, a clock, a regulator or a panel.
2. **A successful AVB verification with a development key is not proof of
   bootloader acceptance.** Descriptor integrity and lock-state enforcement are
   separate mechanisms. See [AVB and trust](android/avb.md).
3. **A successful module dependency closure is not proof that Android boots.**
   Link closure, first-stage placement and runtime behaviour are three
   different checks. See [DLKM partitions](android/dlkm.md).

## What a runtime claim needs

A valid build result needs a committed source graph, declared non-Git inputs, an
effective configuration, compiler identity, generated headers, strict modpost
and a complete module manifest. A **runtime** claim additionally needs
independently authorized observation on the hardware itself.

| Claim | Sufficient evidence |
|---|---|
| "It builds" | source lock + configuration + toolchain + strict modpost + module manifest |
| "It is ABI-closed" | `Module.symvers`, CRCs and a dependency graph per partition |
| "The descriptor is valid" | authenticated image + recomputed hashtree + root binding |
| "It boots" | hardware observation only |
| "The driver works" | hardware observation only |

## Current standing

As of the C28 baseline documented here:

- **Hardware validation of any custom image: 0.** The LieppOS kernel has never
  been booted on this device.
- Strict stock-module certification: **440 / 458**. Experimental: **6 / 458**.
- The C28 boot package is `OFFLINE_PREFLIGHT_FAILED` and is **not deployable**.

Nothing on this site describes a flash-ready artifact. See
[Current status](project/status.md) and
[Known limitations](devices/ulefone-armor-29-pro-thermal/known-limitations.md).

## Where the raw evidence lives

The [research repository](https://github.com/LieppOS/LieppOS-ulefone-gq5012bf1-research)
holds raw captures, logs and per-campaign reports. This book is a curated
explanation of that evidence, not a replacement for it. See
[Methodology](research/methodology.md) and
[Evidence index](research/evidence-index.md).
