---
sidebar_position: 1
---

# How to contribute

Contributions are always welcome, no matter how large or small!

## Pre-requisites

You need to have your Mac laptop setup with all the tools necessary.
We provide a script in package.json that will allow you to quickly check your environment for the tools that are needed and their versions.

```bash
> yarn check:env
yarn run v1.22.19
$ ./scripts/checkEnvironment.sh
----------------------------------------------
Checking Xcode ...
✅ OK
----------------------------------------------
Checking Java ...
✅ OK
----------------------------------------------
Checking nvm ...
✅ OK
----------------------------------------------
Checking npx ...
✅ OK
----------------------------------------------
Checking yarn ...
✅ OK
----------------------------------------------
Checking watchman ...
✅ OK
----------------------------------------------
Checking pod ...
✅ OK
----------------------------------------------
Checking shellcheck ...
✅ OK
----------------------------------------------
Checking node ...
✅ OK
----------------------------------------------
Comparing .nvmrc nodejs version with allspark ...
✅ OK
✨  Done in 5.34s.
```

see the [Setup page](./Setup.md) for more details on how to set up your environment.

## Development workflow

To get started with the project, run the following in the root directory to install the required dependencies for each package,
and create the dist directory.

```bash npm2yarn
nvm install # this will make sure that you use the correct node version for this repo
npm install
npm run build
```

> While it's possible to use [`npm`](https://github.com/npm/cli), the tooling is built around [`yarn`](https://classic.yarnpkg.com/), so you'll have an easier time if you use `yarn` for development.

While developing, you can run the `LDRNExample` app to test your changes. Any changes you make in the library's Typescript code will be reflected in the LDNRNExample app without a rebuild.
If you change any native code, then you'll need to rebuild the LDNRNExample app.
Remember to add tests for your change if possible.

```bash npm2yarn
# To start the packager:
cd example
nvm install
npm run start

# To run the LDRNExample app on Android:
npm run android

# To run the LDRNExample app on iOS:
npm run ios
```

NOTE: in order to make sure your changes are updated live in the simulator / emulator, we recommend running `yarn build:watch` from the root directory in a separate terminal.

Before you push the branch to remote, verify the following:

```bash npm2yarn
# Make sure the code passes Typescript and ESLint
npm run build
npm run lint

cd example
npm run typecheck
npm run lint

# Make sure the unit tests are running successfully
npm run test
```

To fix formatting errors, run the following:

```bash npm2yarn
npm run lint --fix
npm run prettier --write ./src

cd example
npm run lint --fix
npm run prettier --write ./src
```

We use

- [TypeScript][4] for type checking,
- [ESLint][2] with [Prettier][3] for linting and formatting the code, and
- [Jest][5] with [testing-library][6] for testing

## Documentation

If you make changes to the Styleguidist documentation, you can test locally by running:

```bash npm2yarn
npm run docs:dev
```

This will build the docs site locally and expose it at `http://localhost:9999`.
You can navigate to this URL in your browser and verify your changes.

## Naming conventions and pull requests

We follow a Jira-driven development lifecycle which translates to the following:

- make sure there is a Jira ticket for the work that you intend to contribute (our Jira project is `CEEMP`)
- we use the following naming conventions:
  - git branch: "[Jira-ticket]-[short-description]" , e.g. "CEEMP-1234-new-component-dialog"
  - git commit message: "[Jira-ticket] [short-description]", e.g. "CEEMP-1234 add styling", "CEEMP-1234 add unit tests"
- when you're sending a pull request:
  - Prefer small pull requests focused on one change.
  - Verify that linters and tests are passing.
  - Review the documentation to make sure it looks good.
  - Follow the pull request template when opening a pull request.
  - For pull requests that change the API or implementation, discuss with GTP.mobile team first (#ld-support-reactnative channel in Slack).

## New component template

If you are contributing a new component, please start with the [provided template][1].
You can also create a new component with the `hygen code generator` which generates all the files and examples required by the component.

Examples below:

```bash
yarn create:component

yarn run v1.22.19
$ npx hygen component new

✔ Whats your component name? - Button
Loaded templates: _templates
       added: src/next/components/Button.tsx
       added: src/next/components/docs/Button.md
       added: src/next/components/__tests__/Button.test.tsx
      inject: src/index.ts
✨  Done in 11.64s.
```

```bash
yarn create:example

yarn run v1.22.19
$ npx hygen component screens

✔ Whats your new screen name to be added in LDRNExample App? eg: Button, Link
Loaded templates: _templates
      added: example/src/screens/ButtonScreen.tsx
      inject: example/src/App.tsx
      inject: example/src/App.tsx
      inject: example/src/screens/HomeScreen.tsx
      inject: example/src/screens/index.ts
      inject: example/src/types.ts
✨  Done in 11.64s.
```

[1]: https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/blob/main/template.tsx
[2]: https://eslint.org
[3]: https://prettier.io/
[4]: https://www.typescriptlang.org/
[5]: https://jestjs.io/
[6]: https://callstack.github.io/react-native-testing-library/
