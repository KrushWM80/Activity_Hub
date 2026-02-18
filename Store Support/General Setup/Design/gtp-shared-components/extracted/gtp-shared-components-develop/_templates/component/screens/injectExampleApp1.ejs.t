---
inject: true
to: example/src/App.tsx
before: "} from './screens';"
skip_if: "<%= componentName %>Screen,"
---

  <%= componentName %>Screen,