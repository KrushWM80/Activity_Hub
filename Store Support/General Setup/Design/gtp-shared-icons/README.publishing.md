## 1) Publishing variants

  [a) Manual publish]( #Manual-publish-process)

  [b) Using hygen script](#Publish-using-Hygen-script)

  # a) Manual publish process
## Publishing and versioning

To publish a new release of the library, run `npm version`, then push the new commit and tag.
Here are the steps in detail:

### Create new version (local)

- checkout branch `main`
- ensure the repo is up-to-date and the working directory is clean
- the local branch is expected to track the source repo
- if you want to see what will be included in the package you can run `npx npm-packlist`. This list is driven by the `files` option in package.json.
- invoke `npm version <VERSION_TYPE>`
  Typical values for `VERSION_TYPE` are `patch` or `minor`. See `npm version --help` for details.
- e.g. if you need to publish a patch (1.5.0 -> 1.5.1)

  ```sh
  npm version patch
  ```

  if you need to publish a minor release (1.5.0 -> 1.6.0)

  ```sh
  npm version minor
  ```

  verify that a new local commit was created and the commit has the correct tag on it

  ```
  git log --oneline --decorate --name-status HEAD^..
  ```

  - push new version to github

  ```sh
  git push --follow-tags
  ```

The actual publication to npme is automated by the [multibranch build job][1]. See [looper.yml][4] file for details on the looper job steps.

### Create release page (github)

- go to [tags][3] -> Releases
- click on the number that has the release you just published
- click Create new release
- fill out the info in there, title can be just the release e.g. 1.5.1 and in the body text add the following e.g.

  ```
  ## What's Changed

  ### Enhancements
  - re-generated icons from Living Design

  **Full Changelog**: https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-icons/compare/v1.5.0...v1.5.1
  ```
Then continue step 2 onwards

# b)Publish using Hygen script

 TO execute the Hygen commands we need to install the following

    brew install hygen
   - [hygen quick start](https://www.hygen.io/docs/quick-start)

    brew install gh
   - [gh quick start](https://cli.github.com/manual/)

     Authenticate your git credentials using gh command
     ```
       gh auth login
         - select Github Enterprise server
         - GHE Hostname:gecgithub01.walmart.com
         - Choose any preferred type ex:HTTPS
         - Authenticate Git with your GitHub credentials (Y)
         - choose any ex:login with a web browser
         - finish the tasks on the web page successfully
     ```
  Then open the terminal and make sure you are in your project folder
  `gtp-shared-icons`,run the following command and provide the details as per the prompts

      npx hygen release new
          -> enter new version number? `enter new version number (ex: 1.0.8)`
          -> enter Previous version number? `enter published version number (ex: 1.0.7)`
          -> whats changed?: `enter info whats changed `
   It will create the draft release, wait for the looper job success, and then publish the release
### 2) Post message in Slack

- go to #ld-support-reactnative and post a message to announce the new release, e.g.

> :tada: Version 1.5.1 of @walmart/gtp-shared-icons has been released :tada:
>
> <ins>Release notes and changelog</ins> <- [make this a Slack link to the new release page https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-icons/releases/tag/v1.5.1]
>
> [add a brief description of changes here]

### Update published docs

- the `looper` job that does the automatic publishing will also create and publish a new
  Styleguidist documentation bundle to production (see `.looper.yml` file, flow `generate-docs`)

### Notes

- optionally, use signed tags: `npm config set sign-git-tag true`
- check previous versions of `gtp-shared-icons` by going to the [tags page][3].

[1]: https://ci.mobile.walmart.com/job/electrode-mobile-platform/job/gtp-shared-icons/
[2]: https://npme.walmart.com/@walmart/gtp-shared-icons/
[3]: https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-icons/tags
[4]: ./.looper.yml
