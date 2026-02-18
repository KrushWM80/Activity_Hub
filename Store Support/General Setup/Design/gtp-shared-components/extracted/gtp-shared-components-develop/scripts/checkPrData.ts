/* eslint-disable no-console */
import fetch from 'node-fetch';
import yargsParser from 'yargs-parser';

// This script is meant to be run on the looper to check the PR Title and Commit messages are in correct format.
// It performs the following:
//   - it will get all pull request meta data using github api and validate if Pull request title and commit messages follow the rules.
//   - Refer jira driven development rules - https://confluence.walmart.com/display/GPEMP/Jira+Driven+Development
// Run - yarn check:prData -t <git_token> -i <pullRequest_title> -p <pullRequest_number>

// Credentials
const owner = 'electrode-mobile-platform';
const repo = 'gtp-shared-components';

// Process the command line arguments excluding the first two entries
const argv = yargsParser(process.argv.slice(2), {
  alias: {
    token: ['t'],
    pullrequestTitle: ['i'],
    pullRequestNumber: ['p'],
  },
  boolean: [],
  string: ['token', 'pullrequestTitle', 'pullRequestNumber'],
  configuration: {
    'parse-numbers': false,
    'boolean-negation': false,
  },
});

// PR titles should start with any one of the below formats
// refer - https://confluence.walmart.com/display/GPEMP/Jira+Driven+Development
// Valid Titles below:
// CEEMP-1234 Fix Tab Component styling
// [CEEMP-1234,CEEMP-3345,CEEMP-2245] Feature Request - add AX component FilterGroup
// (docs) update introduction in docusaurus
// (fix) fix looper node to support ubuntu
// (refactor) update Bottomsheet component to support new RN Modal
// (chore) add script to run codemods
const prTitleOptions = [
  /^CEEMP-\d{4}\s.{0,40}/,
  /^\(docs\)\s.{0,40}/,
  /^\(fix\)\s.{0,40}/,
  /^\(chore\)\s.{0,40}/,
  /^\(refactor\)\s.{0,40}/,
  /^\[(CEEMP-\d{4},)*CEEMP-\d{4}\]\s.{0,40}$/,
];

// PR Commit Messages should start with any one of the below formats
// refer - https://confluence.walmart.com/display/GPEMP/Jira+Driven+Development
// Valid Messages below:
// CEEMP-1234 Fix Tab Component styling
// (docs) update introduction in docusaurus
// (fix) fix looper node to support ubuntu
// (refactor) update Bottomsheet component to support new RN Modal
// (chore) add script to run codemods
const prCommitOptions = [
  /^CEEMP-\d{4}\s.{0,29}/,
  /^\(docs\)\s.{0,29}/,
  /^\(fix\)\s.{0,29}/,
  /^\(chore\)\s.{0,29}/,
  /^\(refactor\)\s.{0,29}/,
];

// Check PR title options
async function checkPrCommits() {
  let pullsUrl = `https://gecgithub01.walmart.com/api/v3/repos/${owner}/${repo}/pulls/${argv.pullRequestNumber}/commits`;

  await fetch(pullsUrl, {
    headers: {
      Accept: 'application/vnd.github+json',
      Authorization: `Bearer ${argv.token}`,
      'X-GitHub-Api-Version': '2022-11-28',
    },
  })
    .then((response) => response.json())
    .then((data) => {
      for (const commit of data) {
        const message = commit.commit.message;
        if (prCommitOptions.some((pattern) => pattern.test(message))) {
          console.log('----------------------------');
          console.log('✅ Pull request follows correct commit message format');
        } else {
          console.log('----------------------------');
          console.log('❌ PR Commit message below has incorrect format');
          console.log(message);
          console.log('\n');
          console.log(
            'P.S - Length of PR Commit Message should not exceed 50 characters',
          );
          console.log('PLEASE FOLLOW ANY ONE OF THE VALID EXAMPLES BELOW');
          console.log('\n');
          console.log('1) CEEMP-1234 Fix Tab Component styling');
          console.log('2) (docs) update introduction in docusaurus');
          console.log('3) (fix) fix looper node to support ubuntu');
          console.log(
            '4) (refactor) update Bottomsheet component to support new RN Modal',
          );
          console.log('5) (chore) add script to run codemods');
          process.exit(1);
        }
      }
    })
    .catch((error) => console.error(error));
}

function checkPRTitle(title: string) {
  return prTitleOptions.some((pattern) => pattern.test(title));
}

// Validate PR Title
if (checkPRTitle(argv.pullrequestTitle)) {
  console.log('----------------------------');
  console.log('✅ Pull request follows correct Title format');
} else {
  console.log('----------------------------');
  console.log('❌ PR Title has incorrect format');
  console.log('P.S - Length of PR title should not exceed 100 characters');
  console.log('PLEASE FOLLOW ANY ONE OF THE VALID EXAMPLES BELOW');
  console.log('\n');
  console.log('1) CEEMP-1234 Fix Tab Component styling');
  console.log(
    '2) [CEEMP-1234,CEEMP-3345,CEEMP-2245] Feature Request - add AX component FilterGroup',
  );
  console.log('3) (docs) update introduction in docusaurus');
  console.log('4) (fix) fix looper node to support ubuntu');
  console.log(
    '5) (refactor) update Bottomsheet component to support new RN Modal',
  );
  console.log('6) (chore) add script to run codemods');
  process.exit(1);
}

// Validate PR commit message
checkPrCommits();
