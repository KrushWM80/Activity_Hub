### Deprecated

The legacy version of the library (< 2.0.0) exposed ThemeProvider which allowed a consumer
to override some or all styling on a given component, thus breaking the "visual consistency" aspect
of the LD3 design system.

> A design system is a set of standards to manage design at scale by reducing redundancy while creating a shared language and visual consistency across different pages and channels. (from [Nielsen Norman Group](https://www.nngroup.com/articles/design-systems-101/))

Starting with version 2.0.0, `LivingDesignProvider` is available.
It is an aggregate provider containing only `SnackbarProvider` for now.
It will contain a `ThemeProvider` in the future that will allow you to switch the overall theme to `Mega` (former `Duplo`).
Also, once LD3 officially specs out support for dark mode on mobile device, that theme will be also supported.
