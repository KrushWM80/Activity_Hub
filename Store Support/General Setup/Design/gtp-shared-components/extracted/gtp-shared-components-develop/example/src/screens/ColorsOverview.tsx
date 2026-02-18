import React from 'react';

import {_ColorPalette} from '@walmart/gtp-shared-components';

import {Header, Page, Section} from '../components';

const ColorsOverview: React.FC = () => {
  return (
    <Page>
      <Header>Colors</Header>
      <Section>
        <_ColorPalette />
      </Section>
    </Page>
  );
};

export {ColorsOverview};
