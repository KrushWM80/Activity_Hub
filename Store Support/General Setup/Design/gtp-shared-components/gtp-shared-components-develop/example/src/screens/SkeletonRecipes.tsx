import * as React from 'react';
import {Skeleton, SkeletonText} from '@walmart/gtp-shared-components';

import {Header, Page, Section, VariantText} from '../components';

export const SkeletonRecipes: React.FC = () => {
  // ---------------
  // Rendering
  // ---------------
  const defaultSkeleton = (
    <>
      <Header>Skeleton (default){'\n  '}</Header>
      <Section space={8} color="white">
        <Skeleton />
      </Section>
    </>
  );

  const variantSkeleton = (
    <>
      <Header>
        Skeleton (with variant){'\n  '}
        <VariantText>{`variant="rounded"`}</VariantText>
      </Header>
      <Section space={8} color="white">
        <Skeleton variant="rounded" />
      </Section>
    </>
  );

  const heightSkeleton = (
    <>
      <Header>
        Skeleton (with height){'\n  '}
        <VariantText>{`height="50"`}</VariantText>
      </Header>
      <Section space={8} color="white">
        <Skeleton height={50} />
        <Skeleton variant="rounded" height={50} />
      </Section>
    </>
  );

  const widthSkeleton = (
    <>
      <Header>
        Skeleton (with width){'\n'}
        <VariantText>{`  width="50" \n`}</VariantText>
      </Header>
      <Section space={8} color="white">
        <Skeleton variant="rounded" height={50} width={50} />
        <Skeleton height={50} width={50} />
      </Section>
    </>
  );

  const exampleSkeleton = (
    <>
      <Header>Skeleton {'\n  '}</Header>
      <Section space={8} color="white">
        <Skeleton />
        <Skeleton variant="rounded" />
      </Section>
      <Section space={8} color="white" horizontal>
        <Skeleton height={50} width={50} />
        <Skeleton height={50} width={50} variant="rounded" />
        <Skeleton height={50} width={100} />
      </Section>
    </>
  );

  const exampleSkeletonText = (
    <>
      <Header>
        SkeletonText{'\n  '}
        <VariantText>{`  lines={3} \n`}</VariantText>
      </Header>
      <Section space={8} color="white">
        <SkeletonText lines={3} />
      </Section>
    </>
  );
  const exampleSkeletonText1 = (
    <>
      <Header>
        SkeletonText{'\n  '}
        <VariantText>{`  lines={5} \n`}</VariantText>
      </Header>
      <Section space={8} color="white">
        <SkeletonText lines={5} />
      </Section>
    </>
  );

  return (
    <Page>
      {defaultSkeleton}
      {variantSkeleton}
      {heightSkeleton}
      {widthSkeleton}
      {exampleSkeleton}
      {exampleSkeletonText}
      {exampleSkeletonText1}
    </Page>
  );
};
