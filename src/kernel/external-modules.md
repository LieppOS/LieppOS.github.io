# External modules

33 modules come from five vendor repositories built out of tree (`M=`) against the kernel output:

| Repository | Modules |
|---|---|
| Mali (`mali`) | 4 (`mali_kbase_mt6878_r44`, memory group manager, protected allocator, DMA-buf test exporter) |
| camera (`mtkcam`) | camsys (4), CCU `mtk_ccuv`, DPE, cam_cal |
| imgsensor (nested in `mtkcam`) | 2 |
| connectivity | conninfra, connfem, WLAN adaptor + core, BT, GPS (3), FM |
| MET | 11 (`met` + API modules) |

## Rules

- Each tree is pinned by commit **and** tree id.
- Provider symbol tables come only from modules built in the same run.
- Duplicate exports and undefined symbols fail the build.
- The Mali recipe follows the owner's `build-mali-r44.sh` exactly.
- Test and helper modules (`cam-ut`, `kheaders`, the DMA-buf test exporter) are reported separately
  and never autoloaded.

## Firmware

Mali firmware (`mali_csffw.bin`) and connectivity firmware are **stock binaries** and are not in
source. They are never redistributed by LieppOS.

See [DLKM partitions](../android/dlkm.md) for how these modules are packaged and signed.
