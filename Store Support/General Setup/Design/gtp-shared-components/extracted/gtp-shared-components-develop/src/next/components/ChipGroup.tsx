import * as React from 'react';
import {ScrollView, StyleSheet, View} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/ChipGroup';
import flattenChildren from 'react-keyed-flatten-children';

import type {CommonViewProps} from '../types/ComponentTypes';
import {a11yRole} from '../utils';

import {ChipId} from './Chip';

// ---------------
// Props
// ---------------
export type ChipGroupProps = CommonViewProps & {
  /**
   * List of all chips to render.
   * Example:
   *
   * ```
   * <ChipGroup
   *  onPress={selectedIds =>
   *    console.log('--- selected Chips: ', selectedIds)
   *  }>
   *    <Chip id={0}>All</Chip>
   *    <Chip id={1}>Last 7 Days</Chip>
   *    <Chip id={2}>Last Month</Chip>
   *    <Chip id={3}>Last 6 Months</Chip>
   *    <Chip id={4}>2022</Chip>
   *  </ChipGroup>
   * ```
   */
  children: React.ReactNode;
  /**
   * The callback fired when a chip is pressed
   * @return an array of id's of the chips which are selected (array of one if multiple is false)
   */
  onPress: (selectedIds: Array<ChipId>) => void;
  /**
   * Whether the chip group allows multiple selections.
   * By default, a ChipGroup allows one selection only
   * (radio button-like functionality)
   * @default false
   */
  multiple?: boolean;
};

/**
 * ChipGroup displays multiple related Chip's in a horizontal row
 * to help with arrangement and spacing.
 *
 * ## Usage
 * ```js
 * import {ChipGroup} from '@walmart/gtp-shared-components`;
 *
 * <ChipGroup
 *  onPress={selectedIds =>
 *    console.log('--- selected Chips: ', selectedIds)
 *  }>
 *    <Chip id={0}>All</Chip>
 *    <Chip id={1}>Last 7 Days</Chip>
 *    <Chip id={2}>Last Month</Chip>
 *    <Chip id={3}>Last 6 Months</Chip>
 *    <Chip id={4}>2022</Chip>
 *  </ChipGroup>
 * ```
 */
const ChipGroup: React.FC<ChipGroupProps> = (props: ChipGroupProps) => {
  const {children, onPress: onGroupPress, multiple = false} = props;

  const [selectedIds, setSelectedIds] = React.useState<Array<ChipId>>([]);

  // ---------------
  // Interactions
  // ---------------
  const handleOnPress = (id: ChipId, sel: boolean) => {
    if (sel && multiple) {
      // if the current chip got selected
      // prepend the id to the list
      setSelectedIds([id, ...selectedIds]);
    } else if (sel && !multiple) {
      // if multiple is false, just pick the first one from the list
      // (which was just prepended above)
      setSelectedIds([id]);
    } else if (!sel && multiple) {
      // if the current chip got de-selected
      // extract this id from the list
      setSelectedIds(selectedIds.filter((item) => item !== id));
    } else {
      setSelectedIds([]);
    }
  };

  React.useEffect(() => {
    onGroupPress(selectedIds);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedIds]);

  const kids = flattenChildren(children);

  // ---------------
  // Rendering
  // ---------------
  const gap = token.componentChipGroupContainerGap; // 8
  return (
    <View
      accessibilityRole={a11yRole('combobox')}
      style={ss(gap).outerContainer}>
      <ScrollView
        testID={ChipGroup.displayName}
        bounces={false}
        horizontal
        showsHorizontalScrollIndicator={false}>
        {kids.map((kid, index) => {
          return (
            <View key={index} style={ss(gap).kid}>
              {React.cloneElement(kid as React.ReactElement, {
                id: index,
                onPress: (cid: ChipId) =>
                  handleOnPress(cid, selectedIds.includes(cid) ? false : true),
                selected: selectedIds.includes(index),
                UNSAFE_style: {
                  paddingVertical: selectedIds.includes(index) ? 0 : 1,
                },
              })}
            </View>
          );
        })}
      </ScrollView>
    </View>
  );
};

// ---------------
// StyleSheet
// ---------------
const ss = (gap: number) => {
  return StyleSheet.create({
    outerContainer: {
      justifyContent: 'center',
      alignItems: 'center',
    },
    kid: {
      marginHorizontal: gap / 2,
    },
  });
};

ChipGroup.displayName = 'ChipGroup';
export {ChipGroup};
