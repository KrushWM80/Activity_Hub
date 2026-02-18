---
inject: true
to: example/src/App.tsx
after: "const screens ="
skip_if: "component: <%= componentName %>Screen"
---

  {
    name: '<%= componentName %>',
    component: <%= componentName %>Screen,
  },