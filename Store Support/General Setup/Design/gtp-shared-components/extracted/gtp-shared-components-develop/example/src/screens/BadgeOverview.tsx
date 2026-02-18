import * as React from 'react';
import {Badge} from '@walmart/gtp-shared-components';
import {Header, Page, Section, BadgeRow} from '../components';

const BadgeOverview: React.FC = () => {
  return (
    <Page>
      <Header>Badge</Header>
      <Section>
        <BadgeRow title="No Text ">
          <Badge color="blue" />
          <Badge color="gray" />
          <Badge color="green" />
          <Badge color="purple" />
          <Badge color="red" />
          <Badge color="spark" />
          <Badge color="white" />
        </BadgeRow>
        <BadgeRow title="With single Text ">
          <Badge color="blue">1</Badge>
          <Badge color="gray">2</Badge>
          <Badge color="green">3</Badge>
          <Badge color="purple">4</Badge>
          <Badge color="red">5</Badge>
          <Badge color="spark">6</Badge>
          <Badge color="white">7</Badge>
        </BadgeRow>
        <BadgeRow title="With double Text ">
          <Badge color="blue">10</Badge>
          <Badge color="gray">20</Badge>
          <Badge color="green">30</Badge>
          <Badge color="purple">40</Badge>
          <Badge color="red">50</Badge>
          <Badge color="spark">60</Badge>
          <Badge color="white">70</Badge>
        </BadgeRow>
        <BadgeRow title="With Numerals">
          <Badge color="blue">1.25 lb</Badge>
        </BadgeRow>
      </Section>
    </Page>
  );
};

export {BadgeOverview};
