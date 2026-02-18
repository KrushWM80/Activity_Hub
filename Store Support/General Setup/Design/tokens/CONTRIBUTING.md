# How to contribute

## Proposing a change

If you intend to fix, change, or make any non-trivial changes to the implementation, you must [file an issue](https://jira.walmart.com/servicedesk/customer/portal/7425). This lets us reach an agreement on your proposal before you put significant effort into it.

## Architectural decision records

This project tracks uses the [Markdown Architectural Decision Records](https://adr.github.io/madr/) format to track software design choices. See the [docs/adr](./docs/adr/) directory for the complete list of the project's ADRs.

## Contribution prerequisites

- You have [Node](https://nodejs.org/en/) installed at v20.10.0+ ([nvm](https://github.com/nvm-sh/nvm) recommended) and [Yarn](https://yarnpkg.com) at v1.2.0+.
- You are familiar with Git.

## Sending a pull request

**Before submitting a pull request**, please make sure the following is done:

1. Clone [the repository](https://gecgithub01.walmart.com/LivingDesign/tokens) and create your branch from `main`.
2. Run `npm i` in the root repository to install dependencies.
3. If you've fixed a bug or added code that should be tested, add tests!
4. Ensure the project builds (`npm run build`).
5. Ensure the test suite passes (`npm run test`).

## Development workflow

After cloning the repository, run `npm i` to fetch its dependencies. Then, you can run several commands:

- `npm run build`: creates a `build` folder with the build artifacts.
- `npm run clean`: removes the build artifacts.
- `npm run storybook`: runs the [Storybook](https://storybook.js.org) development server.
- `npm run test`: runs the tests on the build artifacts.
- `npm run watch`: automatically build the tokens every time a [token](https://gecgithub01.walmart.com/LivingDesign/tokens/tree/main/properties) file or [configurations](https://gecgithub01.walmart.com/LivingDesign/tokens/tree/main/configuration) are updated. When in `watch` mode, use the `ctrl-c` command in terminal to exit the process.

## Semantic versioning

This library follows [semantic versioning](https://semver.org/). Our commits enforce this versioning by following [conventional changelog](https://github.com/conventional-changelog/commitlint/tree/master/%40commitlint/config-conventional) with custom scope rules defined in [commitlint.config.js](./commitlint.config.js).

## FAQ

### Does this library have continuous deployment?

This project is set up to run continuous linting and tests on [Looper](http://looper.walmart.com), Walmart's CI/CD server, on every pull request. Successful merges to `main` result in automatic version incrementation and changelog generation via [semantic-release](https://semantic-release.gitbook.io/semantic-release/), and automatic package publication to [Artifactory](https://dx.walmart.com/artifactory/documentation/confluence/overview), Walmart's npm registry.

For more information, please see the project's [.looper.yml file](./.looper.yml) for configuration details.
