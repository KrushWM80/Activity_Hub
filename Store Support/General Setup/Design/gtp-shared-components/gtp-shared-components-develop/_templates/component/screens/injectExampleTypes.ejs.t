---
inject: true
to: example/src/types.ts
after: "export type NavigationProps = {"
skip_if: "<%= componentName %>: undefined"
---

  <%= componentName %>: undefined;