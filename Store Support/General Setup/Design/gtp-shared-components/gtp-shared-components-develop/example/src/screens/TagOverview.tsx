import * as React from 'react';
import {Header, Page, Section} from '../components';
import {Tag, Icons} from '@walmart/gtp-shared-components';
import {TagRow} from '../components/TagRow';

const TagOverview: React.FC = () => {
  return (
    <Page>
      <Header>Tag</Header>
      <Section>
        <TagRow title="Primary">
          <Tag variant="primary" color="red">
            Red
          </Tag>
          <Tag variant="primary" color="spark">
            Spark
          </Tag>
          <Tag variant="primary" color="green">
            Green
          </Tag>
          <Tag variant="primary" color="blue">
            Blue
          </Tag>
          <Tag variant="primary" color="purple">
            Purple
          </Tag>
          <Tag variant="primary" color="gray">
            Gray
          </Tag>
        </TagRow>
        <TagRow title="Primary with Icon">
          <Tag variant="primary" color="red" leading={<Icons.TruckIcon />}>
            Red
          </Tag>
          <Tag variant="primary" color="spark" leading={<Icons.TruckIcon />}>
            Spark
          </Tag>
          <Tag variant="primary" color="green" leading={<Icons.TruckIcon />}>
            Green
          </Tag>
          <Tag variant="primary" color="blue" leading={<Icons.TruckIcon />}>
            Blue
          </Tag>
          <Tag variant="primary" color="purple" leading={<Icons.TruckIcon />}>
            Purple
          </Tag>
          <Tag variant="primary" color="gray" leading={<Icons.TruckIcon />}>
            Gray
          </Tag>
        </TagRow>
        <TagRow title="Secondary">
          <Tag variant="secondary" color="red">
            Red
          </Tag>
          <Tag variant="secondary" color="spark">
            Spark
          </Tag>
          <Tag variant="secondary" color="green">
            Green
          </Tag>
          <Tag variant="secondary" color="blue">
            Blue
          </Tag>
          <Tag variant="secondary" color="purple">
            Purple
          </Tag>
          <Tag variant="secondary" color="gray">
            Gray
          </Tag>
        </TagRow>
        <TagRow title="Secondary with Icon">
          <Tag variant="secondary" color="red" leading={<Icons.TagIcon />}>
            Red
          </Tag>
          <Tag variant="secondary" color="spark" leading={<Icons.TagIcon />}>
            Spark
          </Tag>
          <Tag variant="secondary" color="green" leading={<Icons.TagIcon />}>
            Green
          </Tag>
          <Tag variant="secondary" color="blue" leading={<Icons.TagIcon />}>
            Blue
          </Tag>
          <Tag variant="secondary" color="purple" leading={<Icons.TagIcon />}>
            Purple
          </Tag>
          <Tag variant="secondary" color="gray" leading={<Icons.TagIcon />}>
            Gray
          </Tag>
        </TagRow>
        <TagRow title="Tertiary">
          <Tag variant="tertiary" color="red">
            Red
          </Tag>
          <Tag variant="tertiary" color="spark">
            Spark
          </Tag>
          <Tag variant="tertiary" color="green">
            Green
          </Tag>
          <Tag variant="tertiary" color="blue">
            Blue
          </Tag>
          <Tag variant="tertiary" color="purple">
            Purple
          </Tag>
          <Tag variant="tertiary" color="gray">
            Gray
          </Tag>
        </TagRow>
        <TagRow title="Tertiary with Icon">
          <Tag variant="tertiary" color="red" leading={<Icons.ThumbUpIcon />}>
            Red
          </Tag>
          <Tag variant="tertiary" color="spark" leading={<Icons.ThumbUpIcon />}>
            Spark
          </Tag>
          <Tag variant="tertiary" color="green" leading={<Icons.ThumbUpIcon />}>
            Green
          </Tag>
          <Tag variant="tertiary" color="blue" leading={<Icons.ThumbUpIcon />}>
            Blue
          </Tag>
          <Tag
            variant="tertiary"
            color="purple"
            leading={<Icons.ThumbUpIcon />}>
            Purple
          </Tag>
          <Tag variant="tertiary" color="gray" leading={<Icons.ThumbUpIcon />}>
            Gray
          </Tag>
        </TagRow>
      </Section>
    </Page>
  );
};

export {TagOverview};
