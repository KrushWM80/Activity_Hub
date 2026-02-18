import * as React from 'react';
import {Controller, Header, Page, Section} from '../components';
import {Body, Collapse, Icons} from '@walmart/gtp-shared-components';

export const CollapseOverview: React.FC = () => {
  // ---------------
  // Rendering
  // ---------------
  return (
    <Page>
      <Header>Collapse</Header>
      <Section inset={false} space={false}>
        <Controller setValueProp="onToggle" controlProp="expanded">
          <Collapse dividerTop title="Single Line Collapse" onToggle={() => {}}>
            <Body>Collapse content appears underneath the toggle area.</Body>
          </Collapse>
        </Controller>
        <Controller setValueProp="onToggle" controlProp="expanded">
          <Collapse
            dividerTop
            icon={<Icons.InfoCircleIcon size={24} />}
            title="Collapse with Subtitle and Icon"
            subtitle="Subtitle Text"
            onToggle={() => {}}>
            <Body>Collapse content appears underneath the toggle area.</Body>
          </Collapse>
        </Controller>
        <Controller setValueProp="onToggle" controlProp="expanded">
          <Collapse
            dividerTop
            title="Get beauty finds from $8 and how-to tutorials"
            onToggle={() => {}}>
            <Body>Collapse content appears underneath the toggle area.</Body>
          </Collapse>
        </Controller>
      </Section>
    </Page>
  );
};
