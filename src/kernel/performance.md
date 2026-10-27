# Performance (FPSGO/C2PS)

**VERIFIED OFFLINE — acceptance HOLD.** No runtime scheduling or boot claim is made.

The FPSGO/C2PS performance cohort is maintained in its own repository and integrated into the
kernel on a separate integration branch (`lieppos/dev21-performance-integration`):

1. a **subtree merge** of the performance repository at
   `drivers/misc/mediatek/performance/lieppos14` (its history is the merge's second parent;
   update only by merging a newer commit);
2. **seven reviewed kernel commits**, one per native overlay: native output owners, sugov control
   lease, scheduler uclamp lease, ADPF contract, CPUQoS task lease, ADPF ratio lease, ADPF
   session lease.

## Build result

Release `6.1.115-mt6878-gq5012bf1-dev21-perf1+`: strict modpost passes; **744 modules** = dev21's
741 + `fpsgo.ko`, `mtk_c2ps.ko`, `c2ps_perf_ioctl.ko`.

The historical Codex 12-module selected cohort is present as **9 replacements of existing
filenames plus 3 additions**, not 12 new modules.

New kernel exports: `sched_uclamp_lease_{acquire,apply,is_live,release}`. **No existing kernel CRC
changed.**

## Acceptance: HOLD

An offline build proves neither runtime scheduling safety nor bootability. Promotion requires
lockdep, KCSAN and hardware validation. Research revisions: `integration/c24-codex17`
(`b8463cc1`) and `integration/c25` (`42e32526`).

## FBT lifecycle (C25)

C25 recreated the FBT policy and fixed suspend/resume and UX EAS ownership, with a focused rebuild
and first-stage UFS intake. These are **source-level** corrections; runtime effects are untested.
