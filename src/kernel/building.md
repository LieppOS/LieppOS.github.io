# Building the kernel

## Supported path: the LieppOS build engine

The engine (`tools/lieppos-build`) materializes the pinned sources, builds in an out-of-tree root
on an ext4 volume, rebuilds every external module against the same output, enforces strict
modpost, and writes an immutable artifact set with a build receipt.

```bash
cd tools/lieppos-build/scripts
# check every pinned input of the target
./lieppos-kernel --root <engine-root> source verify --target gq5012bf1-mt6878-dev21
# detached, gated build
python3 kernel-workspace/tools/lieppos-build-controller.py --root <engine-root> \
    --target gq5012bf1-mt6878-dev21 --profile c21-parity --tag <tag> --jobs 32
# trusted device tree, then the receipt + artifact set
./lieppos-kernel --root <engine-root> boot dt-declared --target gq5012bf1-mt6878-dev21 --profile c21-parity --dt-policy trusted > dt.json
python3 kernel-workspace/tools/lieppos-receipt.py --engine-root <engine-root> --target gq5012bf1-mt6878-dev21 \
    --profile c21-parity --dt-log dt.json --dest <output-root>
```

Targets: `gq5012bf1-mt6878-dev21` (owner source and config exactly) and
`gq5012bf1-mt6878-dev21-performance` (with the FPSGO/C2PS integration, release `-dev21-perf1`).

## Plain Kbuild (for reading, not the release path)

```bash
make -C kernel/ulefone/gq5012bf1 O=<out> ARCH=arm64 LLVM=1 LLVM_IAS=1 gq5012bf1_defconfig
make -C kernel/ulefone/gq5012bf1 O=<out> ARCH=arm64 LLVM=1 LLVM_IAS=1 MTK_PLATFORM=mt6878 Image
```

`make modules` alone stops in modpost on the two CCU consumers; that is expected and resolved by
the mixed-tree recipe ([Architecture](architecture.md)).

> **Warning — do not run:** `dk12/build-image.sh`, `dk12/make-device-tree.sh` and
> `dk12/build-vendor-targetC.sh` in the historical workspace are **not** build entry points. The
> first two erase kernel source; the third erases a historical vendor module tree. All three are
> guarded to refuse execution.

## Reproducibility

Engine dev21 build (`f7f5ae92572ca86d`) vs the independent C21 build:

| Artifact | Result |
|---|---|
| `.config`, kernel release, `vmlinux.symvers`, mixed-tree export table, `modules.builtin(.modinfo)` | byte-identical |
| `Module.symvers` (19,759 exports) | byte-identical |
| 2,741 objects in `vmlinux.a` | 5 byte-identical; 2,732 match after stripping debug/comment/addrsig; 4 still differ |
| `Image` / `vmlinux` | **not byte-identical**: temporary version banner, initramfs cpio timestamps and vDSO build-ids differ |
| 732 of 740 same-named modules | identical after removing debug info, comment, addrsig and build-id |
| 8 modules | still differ after stripping; complete binary equivalence is **not certified** |

No dev21 byte-for-byte reproducibility claim is made. Historical Phase 11 C18 incremental and
from-scratch builds were byte-identical; that does not automatically certify dev21 or the
performance integration.

## Storage safety

- Btrfs metadata hard floor: **4 GiB**; heavy-build restart threshold: **6 GiB**.
- General free-space floor: **25 GiB**, including projected post-operation use.
- Filesystem error counters must remain zero.
- One owner and one live controller per mutable output directory.
