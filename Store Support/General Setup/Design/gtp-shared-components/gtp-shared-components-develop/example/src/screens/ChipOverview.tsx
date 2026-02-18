import * as React from 'react';
import {StyleSheet, View} from 'react-native';
import {Header, Page} from '../components';

import {
  colors,
  Icons,
  Chip,
  ChipGroup,
  ChipId,
} from '@walmart/gtp-shared-components';

const ChipOverview: React.FC = () => {
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
            <Chip id={4}>2022</Chip>
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
            <Chip id={4}>2022</Chip>
          </ChipGroup>
        </View>
      </>
    );
  };

  const SingleChipDefault: React.FC = () => {
    const [isSingleChipSmallSelected, setIsSingleChipSmallSelected] =
      React.useState<boolean>(false);
    const [isSingleChipLargeSelected, setIsSingleChipLargeSelected] =
      React.useState<boolean>(false);

    const onChipPressSmall = (chipId: ChipId, selected: boolean) => {
      setIsSingleChipSmallSelected(!isSingleChipSmallSelected);
      console.log(`${chipId} ${selected ? 'selected' : 'default'}`);
    };

    const onChipPressLarge = (chipId: ChipId, selected: boolean) => {
      setIsSingleChipLargeSelected(!isSingleChipLargeSelected);
      console.log(`${chipId} ${selected ? 'selected' : 'default'}`);
    };

    return (
      <>
        <Header>Chip</Header>
        <View style={styles.outerContainer}>
          <View style={styles.innerContainer}>
            <Chip
              id={0}
              onPress={onChipPressSmall}
              size="small"
              children="Sam's Choice"
              selected={isSingleChipSmallSelected}
            />
            <Chip id={1} size="small" disabled children="Sam's Choice" />
          </View>
          <View style={styles.innerContainer}>
            <Chip
              id={1}
              onPress={onChipPressLarge}
              size="large"
              children="Sam's Choice"
              selected={isSingleChipLargeSelected}
            />
            <Chip id={1} size="large" disabled children="Sam's Choice" />
          </View>
        </View>
      </>
    );
  };

  const SingleChipWithLeading: React.FC = () => {
    const [isSingleChipSmallSelected, setIsSingleChipSmallSelected] =
      React.useState<boolean>(false);
    const [isSingleChipLargeSelected, setIsSingleChipLargeSelected] =
      React.useState<boolean>(false);

    const onChipPressSmall = (chipId: ChipId, selected: boolean) => {
      setIsSingleChipSmallSelected(!isSingleChipSmallSelected);
      console.log(`${chipId} ${selected ? 'selected' : 'default'}`);
    };

    const onChipPressLarge = (chipId: ChipId, selected: boolean) => {
      setIsSingleChipLargeSelected(!isSingleChipLargeSelected);
      console.log(`${chipId} ${selected ? 'selected' : 'default'}`);
    };

    return (
      <>
        <Header>Chip with leading icon</Header>
        <View style={styles.outerContainer}>
          <View style={styles.innerContainer}>
            <Chip
              id={0}
              onPress={onChipPressSmall}
              size="small"
              children="Time"
              selected={isSingleChipSmallSelected}
              leading={<Icons.ClockIcon />}
            />
            <Chip
              id={1}
              size="small"
              disabled
              children="Time"
              leading={<Icons.ClockIcon />}
            />
          </View>
          <View style={styles.innerContainer}>
            <Chip
              id={1}
              onPress={onChipPressLarge}
              size="large"
              children="Time"
              selected={isSingleChipLargeSelected}
              leading={<Icons.ClockIcon />}
            />
            <Chip
              id={1}
              size="large"
              disabled
              children="Time"
              leading={<Icons.ClockIcon />}
            />
          </View>
        </View>
      </>
    );
  };

  const SingleChipWithTrailing: React.FC = () => {
    const [isSingleChipSmallSelected, setIsSingleChipSmallSelected] =
      React.useState<boolean>(false);
    const [isSingleChipLargeSelected, setIsSingleChipLargeSelected] =
      React.useState<boolean>(false);

    const onChipPressSmall = (chipId: ChipId, selected: boolean) => {
      setIsSingleChipSmallSelected(!isSingleChipSmallSelected);
      console.log(`${chipId} ${selected ? 'selected' : 'default'}`);
    };

    const onChipPressLarge = (chipId: ChipId, selected: boolean) => {
      setIsSingleChipLargeSelected(!isSingleChipLargeSelected);
      console.log(`${chipId} ${selected ? 'selected' : 'default'}`);
    };

    return (
      <>
        <Header>Chip with trailing icon</Header>
        <View style={styles.outerContainer}>
          <View style={styles.innerContainer}>
            <Chip
              id={0}
              onPress={onChipPressSmall}
              size="small"
              children="Associate"
              selected={isSingleChipSmallSelected}
              trailing={<Icons.AssociateIcon />}
            />
            <Chip
              id={0}
              size="small"
              disabled
              children="Associate"
              trailing={<Icons.AssociateIcon />}
            />
          </View>
          <View style={styles.innerContainer}>
            <Chip
              id={1}
              onPress={onChipPressLarge}
              size="large"
              children="Associate"
              selected={isSingleChipLargeSelected}
              trailing={<Icons.AssociateIcon />}
            />
            <Chip
              id={1}
              size="large"
              disabled
              children="Associate"
              trailing={<Icons.AssociateIcon />}
            />
          </View>
        </View>
      </>
    );
  };

  const SingleChipWithLeadingTrailing: React.FC = () => {
    const [isSingleChipSmallSelected, setIsSingleChipSmallSelected] =
      React.useState<boolean>(false);
    const [isSingleChipLargeSelected, setIsSingleChipLargeSelected] =
      React.useState<boolean>(false);

    const onChipPressSmall = (chipId: ChipId, selected: boolean) => {
      setIsSingleChipSmallSelected(!isSingleChipSmallSelected);
      console.log(`${chipId} ${selected ? 'selected' : 'default'}`);
    };

    const onChipPressLarge = (chipId: ChipId, selected: boolean) => {
      setIsSingleChipLargeSelected(!isSingleChipLargeSelected);
      console.log(`${chipId} ${selected ? 'selected' : 'default'}`);
    };

    return (
      <>
        <Header>Chip with leading and trailing icons</Header>
        <View style={styles.outerContainer}>
          <View style={styles.innerContainer}>
            <Chip
              id={0}
              onPress={onChipPressSmall}
              size="small"
              children="Label"
              selected={isSingleChipSmallSelected}
              leading={<Icons.StarIcon />}
              trailing={<Icons.CheckIcon />}
            />
            <Chip
              id={0}
              size="small"
              disabled
              children="Label"
              leading={<Icons.StarIcon />}
              trailing={<Icons.CheckIcon />}
            />
          </View>
          <View style={styles.innerContainer}>
            <Chip
              id={1}
              onPress={onChipPressLarge}
              size="large"
              children="Label"
              selected={isSingleChipLargeSelected}
              leading={<Icons.StarIcon />}
              trailing={<Icons.CheckIcon />}
            />
            <Chip
              id={1}
              size="large"
              disabled
              children="Label"
              leading={<Icons.StarIcon />}
              trailing={<Icons.CheckIcon />}
            />
          </View>
        </View>
      </>
    );
  };

  const SingleChipWithDisableOnPress: React.FC = () => {
    return (
      <>
        <Header>Chip with disabledOnPress</Header>
        <View style={styles.innerContainer}>
          <Chip
            id={0}
            selected
            size="small"
            children="Label"
            disableOnPress
            leading={<Icons.StarIcon />}
            trailing={<Icons.CheckIcon />}
          />
          <Chip
            id={1}
            size="small"
            children="Label"
            disableOnPress
            leading={<Icons.StarIcon />}
            trailing={<Icons.CheckIcon />}
          />
        </View>
      </>
    );
  };

  return (
    <Page>
      <ChipGroupDefault />
      <ChipGroupMulti />
      <SingleChipDefault />
      <SingleChipWithLeading />
      <SingleChipWithTrailing />
      <SingleChipWithLeadingTrailing />
      <SingleChipWithDisableOnPress />
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

export {ChipOverview};
