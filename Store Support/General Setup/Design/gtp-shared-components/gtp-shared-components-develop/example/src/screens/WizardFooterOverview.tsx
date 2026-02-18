import * as React from 'react';
import {Page} from '../components';
import {WizardFooterPercent} from '../components/WizardFooterPercent';
import {WizardFooterValue} from '../components/WizardFooterValue';
import {WizardFooterEmpty} from '../components/WizardFooterEmpy';

const WizardFooterOverview: React.FC = () => {
  return (
    <Page>
      <WizardFooterPercent />
      <WizardFooterValue />
      <WizardFooterEmpty />
    </Page>
  );
};

export {WizardFooterOverview};
