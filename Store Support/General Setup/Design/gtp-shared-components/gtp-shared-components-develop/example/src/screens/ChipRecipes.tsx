import * as React from 'react';
import {StyleSheet, View} from 'react-native';
import {Header, Page, VariantText} from '../components';

import {
  colors,
  Icons,
  Chip,
  ChipGroup,
  ChipId,
} from '@walmart/gtp-shared-components';

const ChipRecipes: React.FC = () => {
  const ChipGroupDefault: React.FC = () => {
    const onPressChipGroup = (selectedIds: Array<number | string>) => {
      console.log('--- selected Chips (default): ', selectedIds);
    };
    return (
      <>
        <Header>
          ChipGroup (single selection)
          <VariantText>
            {`\n\n<ChipGroup onPress={\n\t\tid=>handler(id)}>\n\t<Chip id={0}>All</Chip>\n\t<Chip id={1}>Last 7 Days</Chip>\n</ChipGroup>`}
          </VariantText>
        </Header>

        <View style={styles.outerContainer}>
          <View style={[styles.innerContainer]}>
            <ChipGroup onPress={selectedIds => onPressChipGroup(selectedIds)}>
              <Chip id={0}>All</Chip>
              <Chip id={1}>Last 7 Days</Chip>
            </ChipGroup>
          </View>
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
        <Header>
          ChipGroup (multiple selection)
          <VariantText>
            {`\n\n<ChipGroup multiple onPress={\n\t\id=>handler(id)}>\n\t<Chip id={0}>All</Chip>\n\t<Chip id={1}>Last 7 Days</Chip>\n</ChipGroup>`}
          </VariantText>
        </Header>
        <View style={styles.outerContainer}>
          <View style={[styles.innerContainer]}>
            <ChipGroup
              multiple
              onPress={selectedIds => onPressChipGroup(selectedIds)}>
              <Chip id={0}>All</Chip>
              <Chip id={1}>Last 7 Days</Chip>
            </ChipGroup>
          </View>
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
        <Header>
          Chip
          <VariantText>
            {`\n\n<Chip id={0}\n\t children="chip_text"\n\t onPress={onChipPressHandler} \n\t size="small" selected=${isSingleChipSmallSelected.toString()} />\n`}
          </VariantText>
        </Header>
        <View style={styles.outerContainer}>
          <View style={styles.innerContainer}>
            <Chip
              id={0}
              onPress={onChipPressSmall}
              size="small"
              children="Small Chip"
              selected={isSingleChipSmallSelected}
            />
            <Chip id={1} size="small" disabled children="Small Chip" />
          </View>
          <View style={styles.innerContainer}>
            <Chip
              id={1}
              onPress={onChipPressLarge}
              size="large"
              children="large chip"
              selected={isSingleChipLargeSelected}
            />
            <Chip id={1} size="large" disabled children="large chip" />
          </View>
        </View>
      </>
    );
  };

  const SingleChipWithLeading: React.FC = () => {
    const [isSingleChipSmallSelected, setIsSingleChipSmallSelected] =
      React.useState<boolean>(false);

    const onChipPressSmall = (chipId: ChipId, selected: boolean) => {
      setIsSingleChipSmallSelected(!isSingleChipSmallSelected);
      console.log(`${chipId} ${selected ? 'selected' : 'default'}`);
    };

    return (
      <>
        <Header>
          Chip with leading icon
          <VariantText>
            {`\n\n<Chip id={0}\n\t children="Time"\n\t onPress={onChipPressHandler} \n\t size="small" \n\t selected=${isSingleChipSmallSelected.toString()} \n\t leading={<Icons.ClockIcon />} />\n`}
          </VariantText>
        </Header>
        <View style={[styles.outerContainer, styles.singleSmallChipContainer]}>
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
              children="Time"
              disabled
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
    const onChipPressSmall = (chipId: ChipId, selected: boolean) => {
      setIsSingleChipSmallSelected(!isSingleChipSmallSelected);
      console.log(`${chipId} ${selected ? 'selected' : 'default'}`);
    };

    return (
      <>
        <Header>
          Chip with trailing icon
          <VariantText>
            {`\n\n<Chip id={0}\n\t children="Associate"\n\t onPress={onChipPressHandler} \n\t size="small" \n\t selected=${isSingleChipSmallSelected.toString()}} \n\t trailing={<Icons.AssociateIcon />} />\n`}
          </VariantText>
        </Header>
        <View style={[styles.outerContainer, styles.singleSmallChipContainer]}>
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
              id={1}
              size="small"
              children="Associate"
              disabled
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
    const onChipPressSmall = (chipId: ChipId, selected: boolean) => {
      setIsSingleChipSmallSelected(!isSingleChipSmallSelected);
      console.log(`${chipId} ${selected ? 'selected' : 'default'}`);
    };

    return (
      <>
        <Header>
          Chip with leading and trailing icons
          <VariantText>
            {`\n\n<Chip id={0}\n\t children="Label"\n\t onPress={onChipPressHandler} \n\t size="small" \n\t selected=${isSingleChipSmallSelected.toString()} \n\t leading={<Icons.StarIcon />} \n\t trailing={<Icons.CheckIcon />} />\n`}
          </VariantText>
        </Header>
        <View style={[styles.outerContainer, styles.singleSmallChipContainer]}>
          <View style={styles.innerContainer}>
            <Chip
              id={0}
              onPress={onChipPressSmall}
              size="small"
              children="Label"
              selected={isSingleChipSmallSelected}
              leading={<Icons.StarIcon />}
              trailing={<Icons.CheckIcon />}
              UNSAFE_style={{padding: 1}}
            />
            <Chip
              id={1}
              onPress={onChipPressSmall}
              size="small"
              children="Label"
              disabled
              leading={<Icons.StarIcon />}
              trailing={<Icons.CheckIcon />}
              UNSAFE_style={{padding: 1}}
            />
          </View>
        </View>
      </>
    );
  };

  const SingleChipWithUnsafeStyleOnPress: React.FC = () => {
    const [isSingleChipSmallSelected, setIsSingleChipSmallSelected] =
      React.useState<boolean>(false);

    const [isSingleChipLargeSelected, setIsSingleChipLargeSelected] =
      React.useState<boolean>(false);

    const onChipPressSmall = () => {
      setIsSingleChipSmallSelected(!isSingleChipSmallSelected);
    };
    const onChipPressLarge = () => {
      setIsSingleChipLargeSelected(!isSingleChipLargeSelected);
    };

    return (
      <>
        <Header>
          Chip with UNSAFE_style
          <VariantText>
            {`\n\n<Chip id={0}\n\t children="small" \n\t size='small' \n\t selected={selected_state} \n\t onPress={onChipPressHandler} \n\t leading={<Icons.StarIcon />} \n\t trailing={<Icons.CheckIcon />} \n\t UNSAFE_style={{ \n\t\t backgroundColor:colors.spark['60'], \n\t\t alignSelf:'center' \n\t }} />\n`}
          </VariantText>
        </Header>
        <View style={[styles.outerContainer]}>
          <View
            style={[styles.innerContainer, styles.singleLargeChipContainer]}>
            <Chip
              id={0}
              size="small"
              children={'small'}
              selected={isSingleChipSmallSelected}
              leading={<Icons.StarIcon />}
              trailing={<Icons.CheckIcon />}
              onPress={onChipPressSmall}
              UNSAFE_style={{
                backgroundColor: colors.spark['60'],
                alignSelf: 'center',
              }}
            />
            <Chip
              id={1}
              size="large"
              children="large"
              selected={isSingleChipLargeSelected}
              leading={<Icons.StarIcon />}
              trailing={<Icons.CheckIcon />}
              onPress={onChipPressLarge}
              UNSAFE_style={{
                backgroundColor: colors.green['50'],
                alignSelf: 'center',
              }}
            />
          </View>
        </View>
      </>
    );
  };

  const SingleChipWithDisableOnPress: React.FC = () => {
    return (
      <>
        <Header>
          Large Chip with disabledOnPress
          <VariantText>
            {`\n\n<Chip id={0}\n\t children="Label"\n\t onPress={onChipPressHandler} \n\t size="large" \n\t selected={true} \n\t disableOnPress \n\t leading={<Icons.StarIcon />} \n\t trailing={<Icons.CheckIcon />} />\n`}
          </VariantText>
        </Header>
        <View style={styles.outerContainer}>
          <View style={styles.innerContainer}>
            <Chip
              id={0}
              selected
              size="large"
              children="Label"
              disableOnPress
              leading={<Icons.StarIcon />}
              trailing={<Icons.CheckIcon />}
            />
          </View>
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
      <SingleChipWithUnsafeStyleOnPress />
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
  singleSmallChipContainer: {
    minHeight: 60,
  },
  singleLargeChipContainer: {
    minHeight: 65,
  },
});

export {ChipRecipes};
