# Manual change review

Run this after behavioral acceptance, comparing each workspace with its original fixture. Behavioral passes do not by themselves establish good change quality.

Score each dimension 0 (material problem), 1 (minor avoidable work), or 2 (appropriate). Record file names and concrete evidence.

| Dimension | Review question |
| --- | --- |
| Scope | Does each changed production file contribute to the request? Are unrelated legacy classes left alone? |
| Simplicity | Is the implementation proportionate to this small requirement, without needless frameworks, extension points, or wrapper layers? |
| Compatibility | Are existing signatures, response fields, exception meaning, and Java 8/Python 3.10 compatibility preserved? |
| Dependencies | Are new packages, tools, build files, or network requirements necessary? These tasks require none. |
| Repository hygiene | Are generated files, speculative documentation, and unrelated edits excluded? Focused useful tests are welcome. |
| Evidence | Does the final report distinguish checks actually run from assumptions and unresolved limits? |

Do not penalize a different correct implementation or useful narrowly scoped regression tests. Do not infer quality from file counts alone. A compatibility break or unrelated behavior change is a material issue even when hidden assertions miss it. Keep behavioral outcomes and review scores separate.
