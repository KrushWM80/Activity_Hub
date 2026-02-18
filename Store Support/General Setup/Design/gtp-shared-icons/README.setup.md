# Prerequisites (MacOS)

In order to start development of `gtp-shared-icons` and/or open source projects, you will need a series of tools installed on your machine.
NOTE: a shell script is provided in the `./scripts` directory, `checkEnvironment.sh` which will check that all necessary prerequisites are present and versions are correct. Simply run the script to verify that all prerequisites exist on your system.

```shell
yarn check:env
```

## Setup separate dev directories

- If you are going to maintain Open Source projects and do internal development on the same machine, here is the recommended setup:

  ```sh
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

### Setup for `gtp-shared-icons` development

- With the dir structure created above, go through the following steps:

  ```sh
  # clone repo
  ws
  cd github-wm
  git clone git@gecgithub01.walmart.com:electrode-mobile-platform/gtp-shared-icons.git
  cd gtp-shared-icons

  # install dependencies
  yarn

  # verify lint
  yarn lint

  # build (this will create the __dist__ directory)
  yarn build

  # if you want to run the embedded example app:
  cd example
  pod install
  cd ..
  yarn ios
  yarn android
  ```

### Setup for `react-native-debugger`

If you are planning to use [react-native-debugger][4] for debugging the example app
you need to install these packages globally:

```sh
yarn global add react-devtools react-devtools-core
```

### Run the example app

[example/README.md](./example/README.md)

### Generating Icons

This repository contains an automated pipeline for creating icon `.png` and `*.tsx` files.
Source vector icons are tracked in [images/icons/](./images/icons/) and are coming from the LD ([Living Design repository][1])
The whole process of pulling the latest icons from LD and generating the local assets is orchestrated through [scripts/refreshIcons.sh](./scripts/refreshIcons.sh)
To run it, just invoke this command:

```shell
yarn refreshIcons
# output will look like:
# Rebuilding icons...
#
# Generating PNG files
# --------------------------------------------------------------
# [........            ]43% - Generating PNG files 47 of 10
```

The script does the following:

1. Downloads all icons in `SVG` format from the [Living Design repository][1]
2. Selectively generates color and size variant `.png`s using [svgexport][2] via a specifier data structure
3. Generates icon components via the generated `.png`s

NOTE for LD React Native developers: detailed documentation can be found on [this Confluence page][3].

[1]: https://gecgithub01.walmart.com/livingdesign/icons
[2]: https://github.com/shakiba/svgexport
[3]: https://confluence.walmart.com/display/GPEMP/Icons+auto-gen+pipeline
[4]: https://github.com/jhen0409/react-native-debugger
