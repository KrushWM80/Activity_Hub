import * as React from 'react';
import {Header, Page, Section} from '../components';
import {
  colors,
  CircularProgressIndicator,
} from '@walmart/gtp-shared-components';

const CircularProgressIndicatorOverview: React.FC = () => {
  return (
    <Page>
      <Header>Circular Progress Indicator default</Header>
      <Section horizontal color={colors.gray['5']}>
        <CircularProgressIndicator value={25} />
        <CircularProgressIndicator value={33} />
        <CircularProgressIndicator value={75} />
        <CircularProgressIndicator value={100} />
      </Section>
      <Header>Circular Progress Indicator with label and color</Header>
      <Section horizontal color={colors.gray['5']}>
        <CircularProgressIndicator value={25} label="loading" color="blue" />
        <CircularProgressIndicator value={33} label="loading" color="blue" />
        <CircularProgressIndicator value={75} label="error" color="red" />
        <CircularProgressIndicator value={100} label="Done" color="green" />
      </Section>
    </Page>
  );
};

export {CircularProgressIndicatorOverview};
