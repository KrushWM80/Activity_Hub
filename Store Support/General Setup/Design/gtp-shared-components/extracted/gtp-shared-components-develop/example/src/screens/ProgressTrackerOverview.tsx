import * as React from 'react';
import {StyleSheet} from 'react-native';
import {Header, Page, Section, VariantText} from '../components';
import {
  colors,
  ProgressTracker,
  ProgressTrackerItem,
} from '@walmart/gtp-shared-components';

const ProgressTrackerOverview: React.FC = () => {
  return (
    <Page>
      <Header>
        Progress Tracker{'\n  '}
        <VariantText>variant="info"</VariantText>
      </Header>
      <Section>
        <ProgressTracker activeIndex={2} variant="info">
          <ProgressTrackerItem>Label1</ProgressTrackerItem>
          <ProgressTrackerItem>Label2</ProgressTrackerItem>
          <ProgressTrackerItem>Label3</ProgressTrackerItem>
          <ProgressTrackerItem>Label4</ProgressTrackerItem>
        </ProgressTracker>
      </Section>
      <Header>
        Progress Tracker{'\n  '}
        <VariantText>variant="warning"</VariantText>
      </Header>
      <Section>
        <ProgressTracker activeIndex={3} variant="warning">
          <ProgressTrackerItem>Label1</ProgressTrackerItem>
          <ProgressTrackerItem>Label2</ProgressTrackerItem>
          <ProgressTrackerItem UNSAFE_style={styles.itemHeight}>
            Delayed Progress Tracker With All Optional Properties
          </ProgressTrackerItem>
          <ProgressTrackerItem>Label4</ProgressTrackerItem>
          <ProgressTrackerItem>Label5</ProgressTrackerItem>
        </ProgressTracker>
      </Section>
      <Header>
        Progress Tracker{'\n  '}
        <VariantText>variant="error"</VariantText>
      </Header>
      <Section>
        <ProgressTracker activeIndex={1} variant="error">
          <ProgressTrackerItem>Label1</ProgressTrackerItem>
          <ProgressTrackerItem>Label2</ProgressTrackerItem>
          <ProgressTrackerItem>Label3</ProgressTrackerItem>
          <ProgressTrackerItem>Label4</ProgressTrackerItem>
        </ProgressTracker>
      </Section>
      <Header>
        Progress Tracker{'\n  '}
        <VariantText>variant="success"</VariantText>
      </Header>
      <Section>
        <ProgressTracker activeIndex={2} variant="success">
          <ProgressTrackerItem>Label1</ProgressTrackerItem>
          <ProgressTrackerItem>Label2</ProgressTrackerItem>
          <ProgressTrackerItem>Label3</ProgressTrackerItem>
        </ProgressTracker>
      </Section>
    </Page>
  );
};

const styles = StyleSheet.create({
  innerContainer: {
    flex: 1,
    justifyContent: 'space-around',
    flexDirection: 'row',
    padding: 10,
  },
  outerContainer: {
    backgroundColor: colors.gray['5'],
    borderWidth: 1,
    borderBottomLeftRadius: 12,
    borderBottomRightRadius: 12,
    borderColor: colors.gray['10'],
  },
  metricCard: {
    justifyContent: 'flex-start',
    alignItems: 'flex-start',
    padding: 5,
  },
  itemHeight: {
    lineHeight: 16,
  },
});

export {ProgressTrackerOverview};
