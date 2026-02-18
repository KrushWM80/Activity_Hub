import * as React from 'react';
import {StyleSheet, View} from 'react-native';
import {Header, Page, Section, VariantText} from '../components';
import {
  colors,
  CircularProgressIndicator,
  ProgressTracker,
  Rating,
  Scrollbar,
  Variants,
  ProgressIndicator,
  ProgressTrackerItem,
  Metric,
  Icons,
  SpotIcon,
  Link,
  Button,
  Card,
  Nudge,
  Spinner,
} from '@walmart/gtp-shared-components';
import {displayPopupAlert} from './screensFixtures';

const IndicatorOverview: React.FC = () => {
  return (
    <Page>
      <Header>
        ProgressIndicator{'\n  '}
        <VariantText>variant="error"</VariantText>
      </Header>
      <View style={styles.outerContainer}>
        <View style={styles.innerContainer}>
          <ProgressIndicator
            label={'Blocked by conveyor downtime'}
            value={25}
            valueLabel="25% loaded"
            variant="error"
          />
        </View>
      </View>
      <Header>
        ProgressIndicator{'\n  '}
        <VariantText>variant="info"</VariantText>
      </Header>
      <View style={styles.outerContainer}>
        <View style={styles.innerContainer}>
          <ProgressIndicator
            label={'Location'}
            value={50}
            valueLabel="50%"
            variant="info"
          />
        </View>
        <View style={styles.innerContainer}>
          <ProgressIndicator
            label={'Add $35 of items to your cart for free shipping'}
            value={75}
            valueLabel="$9 remaining"
            variant="info"
          />
        </View>
      </View>
      <Header>
        ProgressIndicator{'\n  '}
        <VariantText>variant="success"</VariantText>
      </Header>
      <View style={styles.outerContainer}>
        <View style={styles.innerContainer}>
          <ProgressIndicator
            label={'Account setup is complete'}
            value={100}
            valueLabel="10 0f 10"
            variant="success"
          />
        </View>
      </View>
      <Header>
        ProgressIndicator{'\n  '}
        <VariantText>variant="warning"</VariantText>
      </Header>
      <View style={styles.outerContainer}>
        <View style={styles.innerContainer}>
          <ProgressIndicator
            label={'Your membership will expire soon'}
            value={75}
            valueLabel="3 days left"
            variant="warning"
          />
        </View>
      </View>
      <Header>
        ProgressIndicator{'\n  '}
        <VariantText> without label's</VariantText>
      </Header>
      <View style={styles.outerContainer}>
        <View style={styles.innerContainer}>
          <ProgressIndicator value={85} variant="warning" />
        </View>
        <View style={styles.innerContainer}>
          <ProgressIndicator value={75} variant="error" />
        </View>
        <View style={styles.innerContainer}>
          <ProgressIndicator value={65} variant="success" />
        </View>
        <View style={styles.innerContainer}>
          <ProgressIndicator value={55} variant="info" />
        </View>
      </View>
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
      <Header>Scrollbar</Header>
      <Section space={false}>
        <Scrollbar segments={3} selected={1} />
        <Scrollbar segments={3} selected={2} />
        <Scrollbar segments={3} selected={3} />
      </Section>
      <Header>Circular Progress Indicator</Header>
      <Section horizontal color={colors.gray['5']}>
        <CircularProgressIndicator value={25} />
        <CircularProgressIndicator value={33} />
        <CircularProgressIndicator value={75} />
        <CircularProgressIndicator value={100} />
      </Section>
      <Header>
        Rating{'\n  '}
        <VariantText>{'size="small"'}</VariantText>
      </Header>
      <Section color={colors.gray['5']}>
        <Rating value={5} size="small" />
        <Rating value={4} size="small" />
        <Rating value={3} size="small" />
        <Rating value={2} size="small" />
        <Rating value={1} size="small" />
        <Rating size="small" />
      </Section>
      <Header>
        Rating{'\n  '}
        <VariantText>{'size="large"'}</VariantText>
      </Header>
      <Section color={colors.gray['5']}>
        <Rating value={4.5} size="large" />
        <Rating value={3.5} size="large" />
        <Rating value={2.5} size="large" />
        <Rating value={1.5} size="large" />
        <Rating value={0.5} size="large" />
        <Rating size="large" />
      </Section>
      <Header>Spinners</Header>
      <Section space={false}>
        <Spinner />
        <Spinner size="small" />
      </Section>
      <Section space={false} color={colors.blue['100']}>
        <Spinner color="white" />
        <Spinner size="small" color="white" />
      </Section>
      <Header>
        Metric{'\n  '}
        <VariantText>{'variant="neutral"'}</VariantText>
      </Header>
      <Section>
        <Card UNSAFE_style={styles.metricCard}>
          <Metric
            title="Real-Time WOSH and overtime"
            textLabel="3 hours more then last month"
            timescope="MTD"
            value="24"
            unit="hours"
            variant="neutral"
          />
        </Card>
      </Section>
      <Header>
        Metric{'\n  '}
        <VariantText>{'variant="positiveUp"'}</VariantText>
      </Header>
      <Section>
        <Card UNSAFE_style={styles.metricCard}>
          <Metric
            title="Sales"
            textLabel="50K (3.21%) more from last month"
            timescope="Today"
            value="$500"
            unit="M"
            variant="positiveUp"
          />
        </Card>
      </Section>
      <Header>
        Metric{'\n  '}
        <VariantText>{'variant="positiveDown"'}</VariantText>
      </Header>
      <Section>
        <Card UNSAFE_style={styles.metricCard}>
          <Metric
            title="Oil average"
            textLabel="4% faster YoY"
            timescope="YTD"
            value="16"
            unit="minutes"
            variant="positiveDown"
          />
        </Card>
      </Section>
      <Header>
        Metric{'\n  '}
        <VariantText>{'variant="negativeUp"'}</VariantText>
      </Header>
      <Section>
        <Card UNSAFE_style={styles.metricCard}>
          <Metric
            title="Tire average"
            textLabel="6% slower than last month"
            timescope="MTD"
            value="27"
            unit="minutes"
            variant="negativeUp"
          />
        </Card>
      </Section>
      <Header>
        Metric{'\n  '}
        <VariantText>{'variant="negativeDown"'}</VariantText>
      </Header>
      <Section>
        <Card UNSAFE_style={styles.metricCard}>
          <Metric
            title="Sales"
            textLabel="3k (3.7%) less than last month"
            timescope="MTD"
            value="$1.23"
            unit="M"
            variant="negativeDown"
          />
        </Card>
      </Section>
      <Header>Nudge</Header>
      <Section>
        <Nudge
          title={'The years start coming'}
          onClose={() => displayPopupAlert('Close', 'Close button pressed')}
          leading={
            <SpotIcon color="white">
              <Icons.StarIcon size={24} />
            </SpotIcon>
          }
          actions={
            <Link
              color="default"
              onPress={() => displayPopupAlert('Link', 'Link pressed')}>
              Look away
            </Link>
          }>
          And they don't stop coming. Fed to the rules and I hit the ground
          running. Didn't make sense not to:
        </Nudge>
      </Section>
      <Header>
        Nudge{'\n  '}
        <VariantText>{'Without Actions'}</VariantText>
      </Header>
      <Section>
        <Nudge title="And they don't stop coming. Fed to the rules and I hit the ground running. Didn't make sense not to">
          And they don't stop coming. Fed to the rules and I hit the ground
          running. Didn't make sense not to:
        </Nudge>
        <Nudge
          title={'The years start coming'}
          onClose={() => displayPopupAlert('Close', 'Close button pressed')}
          leading={<Icons.EyeIcon size={24} />}>
          And they don't stop coming. Fed to the rules and I hit the ground
          running. Didn't make sense not to:
        </Nudge>
      </Section>
      <Header>
        Nudge{'\n  '}
        <VariantText>{'Without Close'}</VariantText>
      </Header>
      <Section>
        <Nudge
          title={'The years start coming'}
          leading={<Icons.EyeIcon size={24} />}
          actions={
            <>
              <Button
                variant="primary"
                onPress={() =>
                  displayPopupAlert('Action', 'Primary Button pressed')
                }>
                Look away
              </Button>
              <Button
                variant="tertiary"
                onPress={() =>
                  displayPopupAlert('Action', 'Tertiary button pressed')
                }>
                Look away
              </Button>
            </>
          }>
          And they don't stop coming. Fed to the rules and I hit the ground
          running. Didn't make sense not to:
        </Nudge>
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

export {IndicatorOverview};
