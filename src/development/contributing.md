# Contributing

- Keep kernel, external modules, Android device configuration, recovery, research and documentation responsibilities separate.
- Preserve Git history. Work on isolated branches; never reset another agent's branch, squash the source import or clean unknown generated evidence.
- Make production changes in their owning source repository. Integration branches carry reviewed native kernel changes; the build engine must not grow a competing production-source copy.
- Pin dependencies and include genuine source-built ABI evidence. Never borrow old `.ko` files, fake CRCs, weaken modpost or infer runtime correctness from symbol closure.
- Keep trusted board facts separate from pending numeric wiring. Every hardware claim needs an authorized evidence citation.
- Document unknowns explicitly and preserve certification counts: strict **440/458**, experimental **6/458**, hardware **0**.
- GitHub publication, signing/deployment changes and **all phone operations** require separate owner authorization.

## Documentation changes

Edit `src/` and update `src/SUMMARY.md` for every new page. Keep the evidence labels described in [Understanding evidence](../evidence.md). Do not add binary evidence or links claiming that planned repositories already exist.

Research belongs in the research repository; this site is a curated explanation of it. Do not copy raw campaign reports or logs into the book.
