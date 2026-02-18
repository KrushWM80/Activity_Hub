---
inject: true
to: src/index.ts
before: "export {Button} from './next/components/Button';"
skip_if: "./next/components/<%= componentName %>"
---

export {<%= componentName %>} from './next/components/<%= componentName %>';