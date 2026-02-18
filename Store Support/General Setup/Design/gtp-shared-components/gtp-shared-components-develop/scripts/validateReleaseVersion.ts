/* eslint-disable no-console */
// This script is meant to be run on the looper to validate the new release version.
// It performs the following:
//   - it requires semver package to validate the release.
// ARGUMENTS REQUIRED:
// 1) currentVersion - Current Version (Retrieved from package.json)
// 2) releaseVersion - Valid: major, minor, patch, prepatch, premajor, preminor, prerelease
// Refer Semantic versioning https://semver.org/
// Example - > yarn release:validate 2.1.5 patch"

import * as semver from 'semver';

// Argument 1 - Current Version (Retrieved from package.json)
// Valid: 2.1.5, 2.1.5-rc.0
const currentVersion = process.argv[2];
if (process.argv.length < 5 && !semver.valid(currentVersion)) {
  console.log('ERROR: Invalid Current Version - Please check Package.json');
  process.exit(1);
}

// Argument 2 - Release Version
// Valid: major, minor, patch, prepatch, premajor, preminor, prerelease
// Examples:
// major: 2.1.5 -> 3.0.0
// minor: 2.1.5 -> 2.2.0
// patch: 2.1.5 -> 2.1.6
// prepatch: 2.1.5 -> 2.1.6-rc.0
// premajor: 2.1.5 -> 3.0.0-rc.0
// preminor: 2.1.5 -> 2.2.0-rc.0
// prerelease: 2.1.6-rc.0 -> 2.1.6-rc.1
const releaseVersion = process.argv[3];
console.log('---- Validating new release - ' + releaseVersion + ' ----');
if (
  process.argv.length < 6 &&
  !semver.RELEASE_TYPES.includes(releaseVersion as semver.ReleaseType)
) {
  console.log(
    'ERROR: Invalid Release - Please provide the correct release type like: major, patch, minor, prepatch, preminor, premajor or prerelease',
  );
  process.exit(1);
}

export {};
