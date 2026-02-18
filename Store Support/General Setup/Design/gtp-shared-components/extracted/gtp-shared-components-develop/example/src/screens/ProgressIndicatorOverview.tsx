import * as React from 'react';
import {StyleSheet, View} from 'react-native';
import {Header, Page, VariantText} from '../components';
import {colors, ProgressIndicator} from '@walmart/gtp-shared-components';

const ProgressIndicatorOverview: React.FC = () => {
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

export {ProgressIndicatorOverview};
