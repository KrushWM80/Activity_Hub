---
inject: true
to: example/src/screens/index.ts
append: example/src/screens/index.ts
skip_if: "<%= componentName %>Screen"
---

export {<%= componentName %>Screen} from './<%= componentName %>Screen';