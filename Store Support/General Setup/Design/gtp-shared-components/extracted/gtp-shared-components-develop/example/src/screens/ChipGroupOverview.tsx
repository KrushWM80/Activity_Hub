import * as React from 'react';
import {StyleSheet, View} from 'react-native';
import {Header, Page} from '../components';

import {colors, Chip, ChipGroup} from '@walmart/gtp-shared-components';

const ChipGroupOverview: React.FC = () => {
  const ChipGroupDefault: React.FC = () => {
    const onPressChipGroup = (selectedIds: Array<number | string>) => {
      console.log('--- selected Chips (default): ', selectedIds);
    };
    return (
      <>
        <Header>ChipGroup (single selection)</Header>
        <View style={styles.outerContainer}>
          <View style={[styles.innerContainer, styles.chipGroup]} />
          <ChipGroup onPress={selectedIds => onPressChipGroup(selectedIds)}>
            <Chip id={0}>All</Chip>
            <Chip id={1}>Last 7 Days</Chip>
            <Chip id={2}>Last Month</Chip>
            <Chip id={3}>Last 6 Months</Chip>
            <Chip id={4}>{new Date().getFullYear().toString()}</Chip>
          </ChipGroup>
        </View>
      </>
    );
  };

  const ChipGroupMulti: React.FC = () => {
    const [count, setCount] = React.useState(0);
    const onPressChipGroup = (selectedIds: Array<number | string>) => {
      setCount(count + 1);

      console.log('--- selected Chips (multi): ', selectedIds);
      console.log('--- count: ', count);
    };
    return (
      <>
        <Header>ChipGroup (multiple selection)</Header>
        <View style={styles.outerContainer}>
          <View style={[styles.innerContainer, styles.chipGroup]} />
          <ChipGroup
            multiple
            onPress={selectedIds => onPressChipGroup(selectedIds)}>
            <Chip id={0}>All</Chip>
            <Chip id={1}>Last 7 Days</Chip>
            <Chip id={2}>Last Month</Chip>
            <Chip id={3}>Last 6 Months</Chip>
            <Chip id={4}>{new Date().getFullYear()}</Chip>
          </ChipGroup>
        </View>
      </>
    );
  };

  return (
    <Page>
      <ChipGroupDefault />
      <ChipGroupMulti />
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
  chipGroup: {
    padding: 0,
  },
});

export {ChipGroupOverview};
