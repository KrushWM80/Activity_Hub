#!/usr/bin/env bash
set -eo pipefail

PROXIMITY_URL=https://repository.walmart.com/content/repositories/pangaea_releases/com/walmart/android/ld/living-design-tokens
CURRENT_VERSION=$(git describe --tags --abbrev=0 | sed -E 's/^v//')
echo "Most recent git tag: $CURRENT_VERSION"
echo "Checking for existing @livingdesign/tokens@$CURRENT_VERSION in Proximity"
HTTP_CODE=$(curl --head --silent --output /dev/null --write-out %{response_code} "$PROXIMITY_URL/$CURRENT_VERSION/")
echo "HTTP response code: $HTTP_CODE"

if [ "$HTTP_CODE" == 404 ]; then
  echo "Publishing @livingdesign/tokens@$CURRENT_VERSION"
  ./gradlew publishWalmartMultiModulePublicationToPangaea_releasesRepository
fi
