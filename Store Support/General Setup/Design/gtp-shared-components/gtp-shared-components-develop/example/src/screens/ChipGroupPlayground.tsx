import * as React from 'react';
import {StyleSheet, Text, View, TextStyle} from 'react-native';
import {
  Checkbox,
  colors,
  getFont,
  Chip,
  ChipGroup,
} from '@walmart/gtp-shared-components';

import {Page} from '../components';

const Spacer = () => <View style={ss.spacer} />;

const ChipGroupPlayground: React.FC = () => {
  type Traits = {
    multiple?: boolean;
    optionalChip1: boolean;
    optionalChip2: boolean;
    optionalChip3: boolean;
    optionalChip4: boolean;
  };

  const [traits, setTraits] = React.useState<Traits>({
    multiple: false,
    optionalChip1: false,
    optionalChip2: false,
    optionalChip3: false,
    optionalChip4: false,
  });

  const [count, setCount] = React.useState(0);
  const onPressChipGroup = (selectedIds: Array<number | string>) => {
    setCount(count + 1);

    console.log('--- selected Chips (multi): ', selectedIds);
    console.log('--- count: ', count);
  };

  const [refreshUI, setRefreshUI] = React.useState(false);
  const refreshUIHandler = () => {
    setRefreshUI(true);
    setTimeout(() => {
      setRefreshUI(false);
    }, 1);
  };

  return (
    <View style={ss.container}>
      <View style={ss.buttonContainer}>
        {!refreshUI && (
          <ChipGroup
            multiple={traits.multiple}
            onPress={selectedIds => onPressChipGroup(selectedIds)}>
            <Chip id={0}>All</Chip>
            <Chip id={1}>Last 7 Days</Chip>
            <Chip id={2}>Last Month</Chip>
            {traits.optionalChip1 && <Chip id={3}>Last 6 Months</Chip>}
            {traits.optionalChip2 && (
              <Chip id={4}>{new Date().getFullYear().toString()}</Chip>
            )}
            {traits.optionalChip3 && <Chip id={5}>Tomorrow</Chip>}
            {traits.optionalChip4 && <Chip id={6}>Yesterday</Chip>}
          </ChipGroup>
        )}
      </View>

      <Page>
        <View style={ss.header}>
          <Text style={ss.headerText}>Chip traits</Text>
        </View>
        <View style={ss.innerContainer}>
          <Spacer />

          <Spacer />
          <Checkbox
            label="multiple"
            checked={!!traits.multiple}
            onPress={() => {
              refreshUIHandler();
              onPressChipGroup([]);
              setCount(0);
              setTraits({
                ...traits,
                multiple: !traits.multiple,
              });
            }}
          />

          <Spacer />
          <Text style={ss.radioHeaderText}>children</Text>
          <Text style={ss.secondaryHdr}>(Example chips)</Text>
          <Checkbox
            label={'Last 6 Months'}
            checked={traits.optionalChip1}
            onPress={() => {
              setTraits({
                ...traits,
                optionalChip1: !traits.optionalChip1,
              });
            }}
          />
          <Checkbox
            label={new Date().getFullYear().toString()}
            checked={traits.optionalChip2}
            onPress={() => {
              setTraits({
                ...traits,
                optionalChip2: !traits.optionalChip2,
              });
            }}
          />
          <Checkbox
            label={'Tomorrow'}
            checked={traits.optionalChip3}
            onPress={() => {
              setTraits({
                ...traits,
                optionalChip3: !traits.optionalChip3,
              });
            }}
          />

          <Checkbox
            label={'Yesterday'}
            checked={traits.optionalChip4}
            onPress={() => {
              setTraits({
                ...traits,
                optionalChip4: !traits.optionalChip4,
              });
            }}
          />
          <Spacer />
        </View>
      </Page>
    </View>
  );
};

const ss = StyleSheet.create({
  container: {
    flex: 1,
  },
  buttonContainer: {
    height: 80,
    marginHorizontal: 16,
    borderRadius: 12,
    paddingVertical: 10,
    borderColor: colors.blue['90'],
    paddingHorizontal: 8,
    borderWidth: 0.5,
    alignItems: 'center',
    justifyContent: 'center',
  },
  spacer: {
    height: 8,
  },
  innerContainer: {
    borderBottomLeftRadius: 12,
    borderBottomRightRadius: 12,
    borderColor: colors.blue['90'],
    borderTopColor: colors.blue['90'],
    borderBottomColor: colors.blue['90'],
    borderLeftColor: colors.blue['90'],
    borderRightColor: colors.blue['90'],
    paddingHorizontal: 8,
    paddingBottom: 8,
    borderWidth: 1,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderTopWidth: 1,
    borderLeftWidth: 1,
    borderRightWidth: 1,
    borderTopLeftRadius: 12,
    borderTopRightRadius: 12,
    borderTopColor: colors.blue['90'],
    borderLeftColor: colors.blue['90'],
    borderRightColor: colors.blue['90'],
    paddingRight: 16,
    paddingVertical: 8,
    marginTop: 8,
  },
  headerText: {
    fontSize: 20,
    fontWeight: '500',
    color: colors.blue['90'],
    textAlign: 'left',
    paddingVertical: 4,
    marginLeft: 12,
  },
  radioHeaderText: {
    ...getFont('500'),
    lineHeight: 28,
    fontSize: 20,
    color: colors.blue['90'],
  } as TextStyle,
  secondaryHdr: {
    ...getFont('bold'),
    fontSize: 12,
    color: colors.black,
  } as TextStyle,
});

export {ChipGroupPlayground};
