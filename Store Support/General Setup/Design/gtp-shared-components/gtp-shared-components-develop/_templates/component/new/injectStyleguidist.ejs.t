---
inject: true
to: styleguide.config.js
before: "'src/next/components/Alert.tsx',"
skip_if: "src/next/components/<%= componentName %>.tsx"
---

        'src/next/components/<%= componentName %>.tsx',