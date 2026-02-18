/* eslint-disable no-console */
// This script is meant to be run on the looper to create a release branch if branch doesn't exists.
// It performs the following:
//   - it requires semver package to validate the release version.
// ARGUMENTS REQUIRED:
// 1) releaseVersion - cut a release branch with this version.
// 2) releaseType - patch, major, minor, prerelease, prepatch, premajor or preminor.
// Refer Semantic versioning https://semver.org/
// yarn release:createReleaseBranch -v <release_version> -t <release_type>
// Example - > yarn release:createReleaseBranch -v 2.1.5 -t patch"
// Output -> creates branch release/2.1.5
import {execSync} from 'child_process';
import fs from 'fs';
import {valid} from 'semver';
import yargsParser from 'yargs-parser';

// Output File
const outputFile = 'latestRelease.txt';

// Process the command line arguments excluding the first two entries
const argv = yargsParser(process.argv.slice(2), {
  alias: {
    releaseVersion: ['v'],
    releaseType: ['r'],
  },
  boolean: [],
  string: ['releaseVersion', 'releaseType'],
  configuration: {
    'boolean-negation': false,
  },
});

let releaseBranch =
  argv.releaseType === 'patch' ||
  argv.releaseType === 'minor' ||
  argv.releaseType === 'major'
    ? 'main'
    : 'release/' + argv.releaseVersion?.split('-rc')[0];

// Argument 1 - Release Version
// Valid: 2.1.5, 2.1.5-rc.0
if (!valid(argv.releaseVersion)) {
  console.log('ERROR: Invalid Release Version - Please check Package.json');
  process.exit(1);
}

// Check if branch exists in remote
function checkIfBranchExists(branchName: string): boolean {
  const branchExists: Buffer = execSync(
    `git ls-remote --heads origin ${branchName}`,
  );

  return branchExists.buffer.byteLength > 0;
}

if (!checkIfBranchExists(releaseBranch)) {
  try {
    // create the release branch and push to remote
    console.log('creating new release branch since branch does not exist');
    execSync(
      `git branch ${releaseBranch} && git push -u origin ${releaseBranch}`,
      {stdio: 'ignore'},
    );
  } catch (error) {
    console.log('Error creating release branch' + error);
    process.exit(1);
  }
} else {
  console.log('release branch already exists');
}

fs.rmSync(outputFile, {force: true});

// Store the release branch to latestRelease.txt
fs.writeFileSync(outputFile, releaseBranch);

console.log(releaseBranch);
