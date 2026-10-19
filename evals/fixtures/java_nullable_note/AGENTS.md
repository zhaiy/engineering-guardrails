# Repository guide

This is a Java 8 service module. Keep Java 8 source and runtime compatibility and use only the JDK. Production classes live under `src/shop/`. Build from this directory with:

```sh
mkdir -p build
javac -source 8 -target 8 -d build src/shop/*.java
```

Preserve public method signatures and existing response field names unless the request explicitly changes them. Keep the change within this module.
