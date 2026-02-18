# Publish variants - Use any one variant below to publish gtp-shared-components library based on your convenience

## [a) Using Looper](#a-publish-using-looper) (Preferred)

## [b) Manual publish](#b-manual-publish-process) (If Looper is down then use manual publish)

# STEPS (1*) and (2*) BELOW MUST BE COMPLETED BEFORE STARTING WITH ANY ONE OF THE PUBLISH VARIANT ABOVE

## (1*) Checkout the correct branch

- checkout:
  - branch `main` if you are releasing next gen (rel. 2.\*)
  - branch `main-legacy` if you are releasing legacy (rel. 1.\*)
- ensure the repo is up-to-date and the working directory is clean
- the local branch is expected to track the source repo

```sh
git checkout main
# or
git checkout main-legacy

git pull --all
```

## (2*) Update CHANGELOG

- edit `CHANGELOG.md` and add the corresponding entry for the release if it's not already there, for example:

  ```markdown
  ---

  # Release 1.8.7

  ## Added

  [CEEMP-2623](https://jira.walmart.com/browse/CEEMP-2623) BottomSheet add logic for Android back button
  [CEEMP-2569](https://jira.walmart.com/browse/CEEMP-2569) Legacy Chips support Custom Icons
  ```

  (sections in CHANGELOG can be one of the following: `Breaking`, `Changed`, `Added`, `Fixed` - inspired from various open source changelog's)

- commit changes

```sh
git commit -a -m "(docs) add new release in CHANGELOG"
```

  ---
After Completing above steps (1*) and (2*) use any one of the publish variants below to publish gtp-shared-components library.

# PUBLISH VARIANTS

# a) Publish using Looper

## Step 1: Input Parameters for Looper Build

- To Publish using looper. Navigate to [LOOPER RELEASE HERE][4] link and click on respective release branch (eg: main or main-legacy)
- Click on **Run Publish GTP-Shared-Components** trigger on the left.

     Above Looper Build requires two parameters to initiate the release.

### Input Build Parameter 1 - version

     New Version to release.
     Input Valid Options: major, minor, patch, prepatch, premajor, preminor, prerelease. Refer Semantic versioning <https://semver.org/>

### **NOTE** - If you are unsure which version to choose. Please run yarn release:helper script given below from your release branch (main or main-legacy) which will give you available options. Pull the latest changes from release branch ( main or main-legacy ) before using this script.

   ```sh
   yarn release:helper
   ```
 <img width="768" alt="Screenshot 2023-12-07 at 7 20 40 PM" src="https://gecgithub01.walmart.com/storage/user/77431/files/db441273-a3a5-409e-8966-b659fc735c59">

### Input Build Parameter 2 - teamCode

    Passcode to restrict the library publishing in looper. Please Contact GTP mobile Team.

## Step 2: Start the Looper Build

- After entering 2 parameters and Click Build will start the release.

### Once looper build completes without any issue - Release Build slack message will be posted on the below channel

   [#emp-ci-alerts](https://walmart.slack.com/archives/C015TG6LH7E)

 For regular releases (patch, major or minor) - Go to [#ld-support-reactnative](https://walmart.slack.com/archives/C01LDQF7SRZ) and post this message to announce the new release and add these tags in cc: @Tripti @allspark-core-eng @here

# b) Manual publish process

## Publishing and versioning

To publish a new release of the library, run `npm version`, then push the new commit and tag.
Here are the steps in detail:

### Create new version (local)

- invoke `npm version <VERSION_TYPE>`
  Typical values for `VERSION_TYPE` are `patch` or `minor`. See `npm version --help` for details.
- e.g. if you need to publish a patch (1.8.6 -> 1.8.7)

  ```sh
  npm version patch
  ```

  if you need to publish a minor release (1.8.6 -> 1.9.0)

  ```sh
  npm version minor
  ```

  or you can specify the actual release number as parameter like this:

  ```sh
  npm version 2.0.0-beta.1
  ```

  verify that a new local commit was created and the commit has the correct tag on it
  (use Tower or command line)

  ```sh
  git log --oneline --decorate --name-status HEAD^..
  ```

  - push the new version and tag to github

  ```sh
  git push --follow-tags
  ```

The actual publication to `npme` is automated by the [multibranch build job][1]. See [.looper.yml][3] file for details on the looper job steps.

### Create release page (github)

- go to [tags][2] -> Releases
- click on the number that has the release you just published
- click Create draft release
- fill out the info in there:

  - title can be just the release number e.g. 1.8.7 and
  - in the body text add the following e.g.

    ```
    [CHANGELOG](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/blob/<branch>/CHANGELOG.md#release-187)

    **Code diff with previous release**: https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/compare/v1.8.6...v1.8.7
    ```

  **NOTE**: in the `CHANGELOG` link above replace `<branch>` whith either `main` or `main-legacy` depending on whether you are releasing a 2.\* or a 1.\* version.

### 2) Post message in Slack

- go to #ld-support-reactnative and post a message to announce the new release, e.g.
(replace the `<version-number>` in the template below)

```
  :react-transparent: Version <version-number>  of the Living Design React Native library has been released
  Release notes and changelog   <- [link to  https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/releases/tag/v<verson-number>]

  cc: @Tripti @allspark-core-eng
```

<ins>Release notes and changelog</ins>

### Update published docs

~~- the `looper` job that does the automatic publishing will also create and publish a new
  Styleguidist documentation bundle to production (see `.looper.yml` file, flow `generate-docs`)~~

  This ⬆️ is currently not working, b/c of an unknown Looper error, so we need to run this manually for `next` releases:

- in a terminal run

  ```
  yarn docs
  ```

  and then push the changes with message: `(docs) update docs for rel <rel-number>`

- Looper will send a message to Slack (emp-ci-alerts) when the job is finished
- <span style="color:red">NOTE:</span> if you are publishing a 1.\* release (legacy), last step is update legacy docs on `gtp-sc-legacy-docs`

```shell
git pull --all
./scripts/copyLegacyDocs.sh
```

### Notes

- optionally, use signed tags: `npm config set sign-git-tag true`
- check previous versions of `gtp-shared-components` by going to the [tags page][2].

[1]: https://ci.falcon.walmart.com/job/electrode-mobile-platform/job/gtp-shared-components/
[2]: https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/tags
[3]: ./looper.yml
[4]: https://ci.falcon.walmart.com/job/electrode-mobile-platform/job/gtp-shared-components/
