/* eslint-disable no-console */
// This script is meant to give available release options for gtp-shared-components library.

// NOTE : THIS SCRIPT IS ONLY USED AS HELPER FOR RELEASE AND IT WILL NOT INITIATE THE RELEASE
// RELEASE CAN ONLY BE DONE USING LOOPER BUILD TRIGGER.
//
// It performs the following:
//   - it requires semver package to get the next patch, major, minor, prerelease, prepatch, premajor, preminor from current release version.
// Refer Semantic versioning https://semver.org/
import * as semver from 'semver';

import {version} from '../package.json';

const patch = semver.inc(version, 'patch');
const major = semver.inc(version, 'major');
const minor = semver.inc(version, 'minor');
const prepatch = semver.inc(version, 'prepatch', 'rc');
const preminor = semver.inc(version, 'preminor', 'rc');
const premajor = semver.inc(version, 'premajor', 'rc');
const prerelease = semver.inc(version, 'prerelease', 'rc');

console.log(
  '------------------------------ RELEASE HELPER ------------------------------',
);
console.log('Current @walmart/gtp-shared-components version - ' + version);
console.log('Available Release Options below from Current Version: ' + version);

console.log('Next patch will be (' + patch + ')');
console.log('Next major will be (' + major + ')');
console.log('Next minor will be (' + minor + ')');
console.log('Next prepatch will be (' + prepatch + ')');
console.log('Next preminor will be (' + preminor + ')');
console.log('Next premajor will be (' + premajor + ')');

if (semver.prerelease(version)) {
  console.log('Next prerelease will be (' + prerelease + ')');
}
