/* eslint-disable no-console */
// This script is meant to be run on the looper to retrieve all the releases in the Shared Component library on github w.r.t Github API.
// Refer - https://docs.github.com/en/rest/releases/releases?apiVersion=2022-11-28#list-releases
// It needs to be run from looper for release automation.
// It performs the following:
//  - requires Github Token from looper to get list of releases.
//  - requires new release version.
//  - Output -> store previously released version before the new version in latestRelease.txt
// Run - yarn release:getAll <git_token> <Current_release_version>

import fs from 'fs';
import fetch from 'node-fetch';
import * as semver from 'semver';

// Credentials
const owner = 'electrode-mobile-platform';
const repo = 'gtp-shared-components';

// Output File
const outputFile = 'latestRelease.txt';

// Argument 1 - Github API Token (Stored in Looper w.r.t credentials)
const github_token = process.argv[2];
if (process.argv.length < 3) {
  console.log('ERROR: Please Input Github Api Token');
  process.exit(1);
}

// Argument 2 - New Version to be released
// Valid examples - v2.1.5, v2.1.5.rc-0, v2.2.0
const new_release = process.argv[3];
if (process.argv.length < 4) {
  console.log('ERROR: Please Input New Release version');
  process.exit(1);
}

// Fetch releases from Github API.
async function fetchReleases(page: number, perPage: number): Promise<any[]> {
  const url = `https://gecgithub01.walmart.com/api/v3/repos/${owner}/${repo}/releases?page=${page}&per_page=${perPage}`;
  const response = await fetch(url, {
    headers: {
      Accept: 'application/vnd.github+json',
      Authorization: `Bearer ${github_token}`,
      'X-GitHub-Api-Version': '2022-11-28',
    },
  });

  if (response.status !== 200) {
    console.log('Github Api Request Failed - ' + response.statusText);
    process.exit(1);
  }

  const releases = await response.json();
  return releases;
}

// Paginate the releases retrieved and concat the responses.
async function paginateReleases(): Promise<any[]> {
  const perPage = 30;
  let currentPage = 1;
  let releases: any[] = [];
  let hasNextPage = true;

  while (hasNextPage) {
    const currentReleases = await fetchReleases(currentPage, perPage);

    if (currentReleases.length > 0) {
      releases = releases.concat(currentReleases);
      currentPage += 1;
    } else {
      hasNextPage = false;
    }
  }

  return releases;
}

(async () => {
  const allReleases = await paginateReleases();
  const releaseList: [ReleaseList] = JSON.parse(
    JSON.stringify(allReleases, null, 2),
  );

  const foundReleases: string[] = [];

  // Logic Implemented - Ease of release for 1.x.x and 2.x.x from respective branches main and main-legacy.
  // Traverse all the Github releases and ignore all prerelease
  // List all the versions previously released which are lesser than new released version (1.x.x or 2.x.x) and push to foundReleases.
  // Example:
  // If new version to be released is 1.15.0 -> 1.14.0, 1.13.1, 1.13.0, 1.12.0 (Latest Release here - 1.14.0)
  // If new version to be released is 2.5.0 -> 2.4.0, 2.3.2, 2.3.1, 2.3.0, 2.2.0 (Latest Release here - 2.4.0)
  // This is done to ignore the prerelease version in package.json. Example - 2.5.0-rc.0
  var releaseVersions = releaseList
    .map((rel) => {
      if (!rel.prerelease) {
        return rel.tag_name;
      }
      return '';
    })
    .filter((rel) => rel !== '');

  // Sort the released versions in descending to find the last released version
  releaseVersions.sort(semver.rcompare);

  for (var release of releaseVersions) {
    if (semver.gt(new_release, release)) {
      foundReleases.push(release);
    }
  }

  console.log(foundReleases);

  fs.rmSync(outputFile, {force: true});

  // Store the latest released version to latestRelease.txt
  fs.writeFileSync(outputFile, foundReleases[0]);
})();

// ---------------------------------------------------------------------------------
// GITUHB API RELEASED RESPONSE DATA MODEL - GENERATED FROM SAMPLE SCHEMA IN GITHUB.
// ---------------------------------------------------------------------------------
export interface ReleaseList {
  url: string;
  html_url: string;
  assets_url: string;
  upload_url: string;
  tarball_url: string;
  zipball_url: string;
  id: number;
  node_id: string;
  tag_name: string;
  target_commitish: string;
  name: string;
  body: string;
  draft: boolean;
  prerelease: boolean;
  created_at: Date;
  published_at: Date;
  author: Author;
  assets: Asset[];
}

export interface Asset {
  url: string;
  browser_download_url: string;
  id: number;
  node_id: string;
  name: string;
  label: string;
  state: string;
  content_type: string;
  size: number;
  download_count: number;
  created_at: Date;
  updated_at: Date;
  uploader: Author;
}

export interface Author {
  login: string;
  id: number;
  node_id: string;
  avatar_url: string;
  gravatar_id: string;
  url: string;
  html_url: string;
  followers_url: string;
  following_url: string;
  gists_url: string;
  starred_url: string;
  subscriptions_url: string;
  organizations_url: string;
  repos_url: string;
  events_url: string;
  received_events_url: string;
  type: string;
  site_admin: boolean;
}
