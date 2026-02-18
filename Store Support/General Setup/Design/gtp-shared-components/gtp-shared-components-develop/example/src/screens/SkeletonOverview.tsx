import * as React from 'react';
import {Skeleton, SkeletonText} from '@walmart/gtp-shared-components';

import {Header, Page, Section} from '../components';

export const SkeletonOverview: React.FC = () => {
  // ---------------
  // Rendering
  // ---------------
  return (
    <Page>
      <Header>Skeleton</Header>
      <Section space={8} color="white">
        <Skeleton />
        <Skeleton variant="rounded" />
      </Section>
      <Section space={8} color="white" horizontal>
        <Skeleton height={50} width={50} />
        <Skeleton height={50} width={50} variant="rounded" />
        <Skeleton height={50} width={100} />
      </Section>

      <Header>SkeletonText</Header>
      <Section space={8} color="white">
        <SkeletonText lines={3} />
      </Section>
    </Page>
  );
};
