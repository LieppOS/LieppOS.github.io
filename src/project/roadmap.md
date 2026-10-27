# Roadmap

1. **Publish source** (owner decision): kernel, vendor modules, build engine and manifest, after the license review ([Provenance](../research/provenance.md)). The donor module-signing key in the kernel tree must be replaced first.
2. **Complete kernel history**: fetch the Android Common Kernel ancestry of `6b18f0b` so the published kernel is no longer shallow (no LieppOS commit changes).
3. **First-stage boot contract**: obtain an authorized vendor_boot ramdisk `modules.load` and bootconfig, then build `dtbo.img` from the trusted overlay.
4. **Trusted board description**: display, touch, charger and thermal-camera wiring from authenticated evidence.
5. **Performance**: runtime validation of the FPSGO/C2PS integration (lockdep, KCSAN, hardware), then promotion from HOLD.
6. **Recovery**: switch OrangeFox to the overlay model in a new release.
7. **Full-device ROM** with the source-built kernel (Android 15 first; Android 16 later — never both at once).

## Not on the roadmap

Android 17 is **not** a LieppOS target. The Slot-B Android 17 work was bring-up forensics only; see [Android 17 Slot-B experiment](../android/android17-slot-b.md).

## Open owner decisions

- Publication of the kernel and vendor module sources (license and signing-key review).
- Slot-B capacity: fitting the stock Android 15 userspace would require shrinking Slot-A logical partitions, which is prohibited without explicit owner approval.
- Production AVB signing policy.
