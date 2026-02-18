import * as React from 'react';
import {Header, Page, Section} from '../components';
import {colors, Variants} from '@walmart/gtp-shared-components';

const VariantsOverview: React.FC = () => {
  return (
    <Page>
      <Header>Variants - color</Header>
      <Section>
        <Variants variants={[colors.blue['100'], colors.red['100']]} />
        <Variants
          variants={[
            colors.blue['100'],
            colors.green['100'],
            colors.red['100'],
            colors.spark['100'],
            colors.purple['100'],
          ]}
        />
      </Section>
      <Header>Variants - non-color</Header>
      <Section>
        <Variants
          variants={[
            colors.blue['100'],
            colors.green['100'],
            colors.red['100'],
            colors.spark['100'],
            colors.purple['100'],
          ]}
          colors={false}
        />
      </Section>
    </Page>
  );
};

export {VariantsOverview};
