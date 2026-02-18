---
sidebar_position: 2
---

# Setup

## Prerequisites (MacOS)

In order to start development of the LivingDesign React Native library and/or open source projects, you will need a series of tools installed on your machine.
NOTE: a script is provided which will check that all necessary prerequisites are present and versions are correct. Simply run the script to verify that all prerequisites exist on your system.

```bash npm2yarn
npm run check:env
```

## Setup separate dev directories (MacOS)

- If you are going to maintain Open Source projects and do internal development on the same machine, here is the recommended setup:

  ```bash
  brew install direnv
  mkdir $HOME/workspace
  alias ws='cd $HOME/workspace'
  alias ws='cd $HOME/workspace' >> $HOME/.zshrc # (or the rc file for whatever shell you are using)
  ws
  mkdir github github-wm

  cd github-wm
  # add file .envrc with the following contents, e.g.
  export GIT_AUTHOR_EMAIL=<your walmart email>
  export GIT_COMMITTER_EMAIL=<your walmart email>
  export NPM_CONFIG_REGISTRY=https://npme.walmart.com/

  cd ../github
  # add file .envrc with the following contents, e.g.
  export GIT_AUTHOR_EMAIL=<your github email>
  export GIT_COMMITTER_EMAIL=<your github email>
  ```

### Setup for development (MacOS)

- With the dir structure created above, go through the following steps:

  ```bash npm2yarn
  # clone repo
  ws
  cd github-wm
  git clone git@gecgithub01.walmart.com:electrode-mobile-platform/gtp-shared-components.git
  cd gtp-shared-components

  # setup node (this will set the default node version from the .nvmrc file)
  nvm install

  # install dependencies
  npm install

  # verify lint
  npm run lint

  # build (this will create the __dist__ directory)
  npm run build

  # if you want to run the embedded example app:
  cd example
  pod install
  cd ..
  npm run ios
  npm run android
  ```

### Setup for `react-native-debugger`

If you are planning to use [react-native-debugger][1] for debugging the example app
you need to install these packages globally:

```bash npm2yarn
npm install -g react-devtools react-devtools-core
```

### Run the example app

[Example-app](./Example-app.md)

[1]: https://github.com/jhen0409/react-native-debugger
