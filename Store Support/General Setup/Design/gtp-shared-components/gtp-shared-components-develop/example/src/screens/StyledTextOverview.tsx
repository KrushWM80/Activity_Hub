import * as React from 'react';
import {Icons, StyledText} from '@walmart/gtp-shared-components';
import {Header, Page, Section} from '../components';

const StyledTextOverview: React.FC = () => {
  return (
    <Page>
      <Header>StyledText</Header>
      <Section>
        <StyledText size="small" color="blue" leading={<Icons.CheckIcon />}>
          Blue small StyledText with Check Icon
        </StyledText>
        <StyledText size="small" color="green" leading={<Icons.CheckIcon />}>
          Green small StyledText with Check Icon
        </StyledText>
        <StyledText size="small" color="gray" leading={<Icons.CheckIcon />}>
          Gray small StyledText with Check Icon
        </StyledText>
        <StyledText size="large" color="blue" leading={<Icons.CheckIcon />}>
          Blue large StyledText with Check Icon
        </StyledText>
        <StyledText size="large" color="green" leading={<Icons.CheckIcon />}>
          Green large StyledText with Check Icon
        </StyledText>
        <StyledText size="large" color="gray" leading={<Icons.CheckIcon />}>
          Gray large StyledText with Check Icon
        </StyledText>
      </Section>
    </Page>
  );
};

export {StyledTextOverview};
