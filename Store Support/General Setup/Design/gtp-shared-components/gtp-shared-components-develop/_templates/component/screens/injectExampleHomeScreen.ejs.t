---
inject: true
to: example/src/screens/HomeScreen.tsx
before: "{target: 'Buttons' as const},"
skip_if: "{target: '<%= componentName %>' as const, title: '<%= componentName %>'}"
---

    {target: '<%= componentName %>' as const, title: '<%= componentName %>'},