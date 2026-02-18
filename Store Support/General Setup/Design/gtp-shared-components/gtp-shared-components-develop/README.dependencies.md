# Dependencies

This guide describes the dependencies of this repository and their purpose.

[comment]: # 'REPO ONLY START'

- [Dependencies](#dependencies)
  - [Package Dependencies](#package-dependencies)
  - [Peer Dependencies](#peer-dependencies)
  - [React](#react)
  - [React Native](#react-native)
  - [React Native Picker](#react-native-picker)
  - [React Native DateTimePicker](#react-native-datetimepicker)
  - [React Native Device Info](#react-native-device-info)
  - [React Native Drop Shadow](#react-native-drop-shadow)

[comment]: # 'REPO ONLY END'

## Package Dependencies

Package dependencies, or just regular dependencies, are those packages that are needed for the library code to run properly and so are automatically installed as part of the library.

- [@livingdesign/tokens](https://gecgithub01.walmart.com/LivingDesign/tokens)
- [@walmart/gtp-shared-icons](https://gecgithub01.walmart.com/LivingDesign/icons)
- [lodash](https://github.com/lodash/lodash)
- [moment](https://github.com/moment/moment)
- [react-keyed-flatten-children](https://github.com/grrowl/react-keyed-flatten-children)
- [react-native-modal](https://github.com/react-native-community/react-native-modal)

## Peer Dependencies

Peer dependencies are package dependencies that the library depends on but are not automatically installed. These packages are commonly already used by users in their own applications. They are not included as regular dependencies due to the fact that they contain native code and cannot be be autolinked by the app as well as being problematic to have multiple versions of native code. [See here](https://github.com/react-native-community/cli/issues/1347#issuecomment-761657947) and [also here](https://github.com/react-native-community/cli/pull/2054#issuecomment-1675050775) for more information.

### React

[React](https://reactjs.org) is a library for building component-based user interfaces and is required to use React Native

- [react](https://github.com/facebook/react)
- You can use the version of React needed by React Native according to the [Upgrade Helper](https://react-native-community.github.io/upgrade-helper/)

### React Native

[React Native](https://reactnative.dev) is a framework for building native apps using React

- [react-native](https://github.com/facebook/react-native)
- We recommend using supported versions of React Native, according to the official [React Native Releases](https://github.com/reactwg/react-native-releases)

### React Native Picker

A library for creating pickers in React Native. Used in **Dropdown** (deprecated) component.

- [@react-native-picker/picker](https://github.com/react-native-picker/picker) - ^2.4.0 recommended

### React Native DateTimePicker

React Native date & time picker component for iOS & Android. Used in **DateDropdown** component.

- [@react-native-community/datetimepicker](https://github.com/react-native-datetimepicker/datetimepicker) - ^5.1.0 recommended

### React Native Device Info

Device Information for React Native. Used in **Select** component.

- [react-native-device-info](https://github.com/react-native-device-info/react-native-device-info) - ^10.3.0 recommended

### React Native Drop Shadow

A library for creating drop shadows in React Native specifically for Android as drop shadow styles are by default only supported on iOS while Android only uses elevation. Drop shadows are used in a number of components including **Callout, Menu, Popover, and Snackbar**.

- [react-native-drop-shadow](https://github.com/hoanglam10499/react-native-drop-shadow) - ^0.0.7 recommended
