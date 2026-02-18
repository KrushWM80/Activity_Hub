import * as React from 'react';
import {StyleSheet, View} from 'react-native';
import {Header, Page, VariantText} from '../components';

import {colors, Chip, ChipGroup, Button} from '@walmart/gtp-shared-components';

const ChipGroupRecipes: React.FC = () => {
  type chipGroupCodeProps = {
    singleSelectionCodeVisible: boolean;
    multipleSelectionCodeVisible: boolean;
  };
  const [chipGroupCode, setChipGroup] = React.useState<chipGroupCodeProps>({
    singleSelectionCodeVisible: false,
    multipleSelectionCodeVisible: false,
  });

  /**
   *
   * @param buttonLabel
   * @param listName
   * @returns button ui to Show or hides sample code
   */
  const displayCodeButton = (buttonLabel: string, chipGroupName: string) => {
    const chipGroupNameVal: boolean =
      chipGroupCode[chipGroupName as keyof chipGroupCodeProps];
    return (
      <Button
        UNSAFE_style={styles.displayCodeBtn}
        variant="tertiary"
        onPress={() => {
          setChipGroup({...chipGroupCode, [chipGroupName]: !chipGroupNameVal});
        }}>
        {buttonLabel}
      </Button>
    );
  };

  const ChipGroupDefault: React.FC = () => {
    const buttonLabel = chipGroupCode.singleSelectionCodeVisible
      ? 'Hide code'
      : 'Show Code';
    const codeSample = `\n\n<ChipGroup onPress={selectedIds => chipHandler(selectedIds)}>
    <Chip id={0}>All</Chip>
    <Chip id={1}>Last 7 Days</Chip>
    <Chip id={2}>Last Month</Chip>
    <Chip id={3}>Last 6 Months</Chip>
    <Chip id={4}>${new Date().getFullYear().toString()}</Chip>
  </ChipGroup>`;

    const onPressChipGroup = (selectedIds: Array<number | string>) => {
      console.log('--- selected Chips (default): ', selectedIds);
    };

    return (
      <>
        <View>
          <Header>
            ChipGroup (single selection)
            {chipGroupCode.singleSelectionCodeVisible && (
              <VariantText>{codeSample}</VariantText>
            )}
          </Header>
          {displayCodeButton(buttonLabel, 'singleSelectionCodeVisible')}
        </View>
        <View style={styles.outerContainer}>
          <View style={[styles.innerContainer]}>
            <ChipGroup onPress={selectedIds => onPressChipGroup(selectedIds)}>
              <Chip id={0}>All</Chip>
              <Chip id={1}>Last 7 Days</Chip>
              <Chip id={2}>Last Month</Chip>
              <Chip id={3}>Last 6 Months</Chip>
              <Chip id={4}>{new Date().getFullYear().toString()}</Chip>
            </ChipGroup>
          </View>
        </View>
      </>
    );
  };

  const ChipGroupMulti: React.FC = () => {
    const buttonLabel = chipGroupCode.multipleSelectionCodeVisible
      ? 'Hide code'
      : 'Show Code';
    const codeSample = `\n\n<ChipGroup
    multiple
    onPress={selectedIds => chipGroupHandler(selectedIds)}>
    <Chip id={0}>All</Chip>
    <Chip id={1}>Last 7 Days</Chip>
    <Chip id={2}>Last Month</Chip>
    <Chip id={3}>Last 6 Months</Chip>
    <Chip id={4}>${new Date().getFullYear().toString()}</Chip>
  </ChipGroup>`;

    const [count, setCount] = React.useState(0);
    const onPressChipGroup = (selectedIds: Array<number | string>) => {
      setCount(count + 1);

      console.log('--- selected Chips (multi): ', selectedIds);
      console.log('--- count: ', count);
    };
    return (
      <>
        <View>
          <Header>
            ChipGroup (multiple selection)
            {chipGroupCode.multipleSelectionCodeVisible && (
              <VariantText>{codeSample}</VariantText>
            )}
          </Header>
          {displayCodeButton(buttonLabel, 'multipleSelectionCodeVisible')}
        </View>
        <View style={styles.outerContainer}>
          <View style={[styles.innerContainer]}>
            <ChipGroup
              multiple
              onPress={selectedIds => onPressChipGroup(selectedIds)}>
              <Chip id={0}>All</Chip>
              <Chip id={1}>Last 7 Days</Chip>
              <Chip id={2}>Last Month</Chip>
              <Chip id={3}>Last 6 Months</Chip>
              <Chip id={4}>{new Date().getFullYear().toString()}</Chip>
            </ChipGroup>
          </View>
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
  displayCodeBtn: {position: 'absolute', bottom: 0, right: 2},
});

export {ChipGroupRecipes};
