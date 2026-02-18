/* eslint-disable no-console */
// This script is meant to generate release notes for changelog from previous released version in gtp-shared-components library.

// NOTE : THIS SCRIPT IS ONLY USED AS HELPER FOR RELEASE AND IT WILL NOT INITIATE THE RELEASE
// RELEASE CAN ONLY BE DONE USING LOOPER BUILD TRIGGER.
//
// It performs the following:
//   - it will get all the pull requests info until the previously released version by default or the version provided in optional argument and generate release notes for changelog.
// Run - yarn release:generateRelNotes <git_token> <release_branch>(OPTIONAL) <last_release_version>(OPTIONAL)
// yarn release:generateRelNotes -t <GIT_TOKEN_HERE>
// yarn release:generateRelNotes -t <GIT_TOKEN_HERE> -b release -v v2.0.10

import fetch from 'node-fetch';
import yargsParser from 'yargs-parser';

// Credentials
const owner = 'electrode-mobile-platform';
const repo = 'gtp-shared-components';

// Process the command line arguments excluding the first two entries
const argv = yargsParser(process.argv.slice(2), {
  alias: {
    token: ['t'],
    releaseBranch: ['b'],
    releaseVersion: ['v'],
  },
  default: {
    releaseBranch: 'main',
  },
  boolean: [],
  string: ['token', 'releaseBranch', 'releaseVersion'],
  configuration: {
    'parse-numbers': false,
    'boolean-negation': false,
  },
});

// all changelog updates to be printed
let changelogUpdates: ChangelogInfo[] = [];

/**
 * Checks if a pull request with the given pull number has been merged.
 *
 * @param pull_number - The number of the pull request to check.
 * @returns A boolean indicating whether the pull request has been merged or not.
 */
async function isMerged(pull_number: number) {
  const response = await fetch(
    `https://gecgithub01.walmart.com/api/v3/repos/${owner}/${repo}/pulls/${pull_number}/merge`,
    {
      headers: {
        Accept: 'application/vnd.github+json',
        Authorization: `Bearer ${argv.token}`,
        'X-GitHub-Api-Version': '2022-11-28',
      },
    },
  );

  const status = await response.status;
  return status === 204;
}

/**
 * Checks if an entry with the given ticket number exists in the changelogUpdates array.
 * If an entry exists, it updates the ticket description and adds the PR info to the existing entry.
 *
 * @param ticketNumber - The ticket number to check for in the changelogUpdates array.
 * @param prInfo - The PR info to add to the existing entry.
 * @param ticketDesc - The ticket description to update in the existing entry.
 * @returns True if an entry with the given ticket number exists and is updated, false otherwise.
 */
function checkAndUpdateEntry(
  ticketNumber: string,
  prInfo: PRInfo,
  ticketDesc: string,
) {
  for (let i = 0; i < changelogUpdates.length; i++) {
    if (changelogUpdates[i].ticketNumber === ticketNumber) {
      changelogUpdates[i].ticketDesc =
        changelogUpdates[i].ticketDesc + '.' + ticketDesc;
      changelogUpdates[i].ticketPRInfo.push(prInfo);
      return true;
    }
  }
  return false;
}

/**
 * Prints the changelog entries.
 *
 * This function iterates over the `changelogUpdates` array and prints the changelog entries to the console.
 * Each entry consists of a ticket number (if available), ticket description, and associated pull request information.
 * The function constructs a formatted string for each entry and logs it to the console.
 *
 * Example output:
 * - [CEEMP-1234](https://jira.walmart.com/browse/CEEMP-1234) Ticket description [#5678](https://gecgithub01.walmart.com/owner/repo/pull/5678)
 * - (chore|refactor|fix|docs) Ticket description
 * @returns {void} This function does not return anything.
 */
function printChangelogEntries() {
  for (let entry of changelogUpdates) {
    if (entry.ticketNumber) {
      const jiraTicketNumber = entry.ticketNumber;
      const ticketDesc = entry.ticketDesc;
      let _changelogEntry =
        '- [' +
        jiraTicketNumber +
        '](https://jira.walmart.com/browse/' +
        jiraTicketNumber +
        ')' +
        ticketDesc;

      for (let prInfo of entry.ticketPRInfo) {
        _changelogEntry =
          _changelogEntry +
          ' ' +
          '[#' +
          prInfo.prNumber +
          '](' +
          prInfo.prUrl +
          ')';
      }

      console.log(_changelogEntry);
    } else {
      let _changelogEntry = '- ' + entry.ticketDesc;

      for (let prInfo of entry.ticketPRInfo) {
        _changelogEntry =
          _changelogEntry +
          ' ' +
          '[#' +
          prInfo.prNumber +
          '](' +
          prInfo.prUrl +
          ')';
      }

      console.log(_changelogEntry);
    }
  }
}

/**
 * Generates release notes for the changelog.
 *
 * This function retrieves the necessary data from the GitHub API to generate release notes for the changelog.
 * It fetches information about releases, merged and closed pull requests.
 * It then filters and sorts the pull requests based on the last release version and generates the changelog entries accordingly.
 * The generated changelog entries are printed to the console.
 *
 * @returns {Promise<void>} A promise that resolves once the release notes are generated and printed.
 */
async function generateNotesForChangelog() {
  const releasesUrl = `https://gecgithub01.walmart.com/api/v3/repos/${owner}/${repo}/releases`;
  let pullsUrl = `https://gecgithub01.walmart.com/api/v3/repos/${owner}/${repo}/pulls?state=closed`;

  const releasesResponse = await fetch(releasesUrl, {
    headers: {
      Accept: 'application/vnd.github+json',
      Authorization: `Bearer ${argv.token}`,
      'X-GitHub-Api-Version': '2022-11-28',
    },
  });

  let releases = await releasesResponse.json();

  if (argv.releaseVersion) {
    releases = releases.filter((release: any) => {
      return release.tag_name === argv.releaseVersion ? release : '';
    });
  }

  if (!releases || releases.length === 0) {
    console.error('No releases found');
    return;
  }

  const lastReleaseVersion = releases[0].tag_name;
  const lastReleaseDate = new Date(releases[0].published_at);

  if (argv.releaseBranch === 'release') {
    pullsUrl = `https://gecgithub01.walmart.com/api/v3/repos/${owner}/${repo}/pulls?state=closed&base=release/${
      lastReleaseVersion.replace('v', '').split('-rc')[0]
    }`;
  }

  console.log('----------------------------------------');
  console.log(`Last release version: ${lastReleaseVersion}`);
  console.log(`Last release date: ${lastReleaseDate}`);

  const releaseBranch =
    argv.releaseBranch === 'release'
      ? 'release/' + lastReleaseVersion.replace('v', '').split('-rc')[0]
      : 'main';
  console.log(`Release changelog data from Branch: ${releaseBranch}`);

  // Get all Pull requests until the last release version by default or provided version in argument.
  const pullsResponse = await fetch(pullsUrl, {
    headers: {
      Accept: 'application/vnd.github+json',
      Authorization: `Bearer ${argv.token}`,
      'X-GitHub-Api-Version': '2022-11-28',
    },
  });

  const pulls = await pullsResponse.json();

  let prsUntilLastRelease = pulls.filter((pull: any) => {
    const prDate = new Date(pull.closed_at);
    return prDate > lastReleaseDate;
  });

  let mergedPrs: number[] = [];
  for (let pr of prsUntilLastRelease) {
    let _isMerged = await isMerged(pr.number);
    if (_isMerged) {
      mergedPrs.push(pr.number);
    }
  }
  // Store only PRs which are merged into main branch
  prsUntilLastRelease = prsUntilLastRelease.filter((pull: any) => {
    return mergedPrs.includes(pull.number);
  });

  console.log(
    `PRs created after last release above: ${prsUntilLastRelease.length}`,
  );
  console.log('----------------------------------------');
  console.log('GENERATED CHANGELOG NOTES BELOW FOR NEW VERSION \n');

  // Sort the PRs based on last recently merged.
  prsUntilLastRelease = prsUntilLastRelease.sort(
    (
      a: {merged_at: string | number | Date},
      b: {merged_at: string | number | Date},
    ) => {
      return new Date(b.merged_at).getTime() - new Date(a.merged_at).getTime();
    },
  );

  prsUntilLastRelease.forEach((pr: any) => {
    const prTitle = pr.title;
    const prInfo: PRInfo = {prNumber: pr.number, prUrl: pr.html_url};

    // PR Title Cases
    // case 1 -> CEEMP-1234 Pr description.
    if (prTitle.startsWith('CEEMP')) {
      const _prTitleInfo: string[] = prTitle.split(/(CEEMP-\d{4})/);
      const _jiraTicketNumber = _prTitleInfo[1] as string;
      const _ticketDesc = _prTitleInfo[2] as string;

      if (!checkAndUpdateEntry(_jiraTicketNumber, prInfo, _ticketDesc)) {
        let changelogInfo: ChangelogInfo = {
          ticketNumber: _jiraTicketNumber,
          ticketDesc: _ticketDesc,
          ticketPRInfo: [prInfo],
        };
        changelogUpdates.push(changelogInfo);
      }
    } else if (prTitle.startsWith('[CEEMP')) {
      // case 2 -> [CEEMP-1234,CEEMP-4777,CEEMP-3408] Pr description.
      let _jiraTicketNumbers = '';
      let _ticketDesc = '';
      const _prTitleInfo = prTitle.match(/\[(.*?)\]\s*(.*)/);
      if (_prTitleInfo) {
        _jiraTicketNumbers = _prTitleInfo[1];
        _ticketDesc = _prTitleInfo[2];
      }

      const ticketNumbers = _jiraTicketNumbers.split(',');

      for (let ticketNumber of ticketNumbers) {
        let changelogInfo: ChangelogInfo = {
          ticketNumber: ticketNumber,
          ticketDesc: _ticketDesc,
          ticketPRInfo: [prInfo],
        };
        changelogUpdates.push(changelogInfo);
      }
    } else {
      // case 3 -> (chore|refactor|fix|docs) Pr description.
      let changelogInfo: ChangelogInfo = {
        ticketDesc: prTitle,
        ticketPRInfo: [prInfo],
      };
      changelogUpdates.push(changelogInfo);
    }
  });
  printChangelogEntries();
}

generateNotesForChangelog();

interface ChangelogInfo {
  ticketNumber?: string;
  ticketPRInfo: [PRInfo];
  ticketDesc: string;
}

interface PRInfo {
  prUrl: string;
  prNumber: string;
}
