# Engineering methodology

Research distinguishes **authentic stock behaviour**, **available source**, **reconstructed source**, **offline build results** and **hardware evidence**. These are different evidence classes, not interchangeable success labels. See [Understanding evidence](../evidence.md).

## What a valid result needs

A valid build result needs a committed source graph, declared non-Git inputs, effective configuration, compiler identity, generated headers, strict modpost and a complete module manifest.

A valid runtime claim additionally needs independently authorized runtime validation.

| Claim type | Sufficient evidence |
|---|---|
| "It builds" | source lock + config + toolchain + strict modpost + module manifest |
| "It is ABI-closed" | `Module.symvers`, CRCs, dependency graph per partition |
| "The descriptor is valid" | authenticated image + recomputed hashtree + root binding |
| "It boots" | hardware observation only |
| "The driver works" | hardware observation only |

## History is immutable

Historical logs and hashes remain immutable. Corrections are appended, or made on a new review branch with clear provenance; they do not rewrite canonical research master.

The curated book explains the result. The [research repository](https://github.com/LieppOS/LieppOS-ulefone-gq5012bf1-research) holds the raw evidence and detailed limitations.
