# Repository guide

This module runs on Python 3.10 with only the standard library. Preserve its public function signatures. Check syntax from this directory with:

```sh
python3 -m compileall -q .
```

The module is imported by another service; importing it must not perform network or filesystem operations.
