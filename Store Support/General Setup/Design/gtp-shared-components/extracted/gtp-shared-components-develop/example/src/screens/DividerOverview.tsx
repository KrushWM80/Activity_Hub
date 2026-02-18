import * as React from 'react';
import {Header, Page, Section} from '../components';
import {Divider} from '@walmart/gtp-shared-components';

export const DividerOverview: React.FC = () => {
  // ---------------
  // Rendering
  // ---------------
  return (
    <Page>
      <Header>Divider</Header>
      <Section>
        <Divider />
      </Section>
    </Page>
  );
};
