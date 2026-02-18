import * as React from 'react';
import {StyleProp, StyleSheet, View, ViewStyle} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/DataTable';
import flattenChildren from 'react-keyed-flatten-children';

import type {CommonViewProps} from '../types/ComponentTypes';

// ---------------
// Props
// ---------------
export type DataTableRowProps = CommonViewProps & {
  /**
   * The content for the row.
   */
  children: React.ReactNode;
  /**
   * If the row is selected.
   * @default false
   */
  selected?: boolean;
  /**
   * If provided, the <strong>style</strong> to provide to the container.
   * This property is prefixed with <strong>UNSAFE</strong> as its use
   * often results in <strong>unintended side effects</strong>.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
};

/**
 * Each Data Table row represents one object, showing details about that object in each cell.
 *
 * ## Usage
 * ```js
 * import {DataTableRow,DataTableHeader} from '@walmart/gtp-shared-components';
 *
 * <DataTableRow>
 *   <DataTableHeader alignment={'left'}>
 *       {"header Left"}
 *   </DataTableHeader>
 *   <DataTableHeader alignment={'right'}>
 *       {"header Right"}
 *   </DataTableHeader>
 * </DataTableRow>
 * ```
 */
const DataTableRow: React.FC<DataTableRowProps> = (
  props: DataTableRowProps,
) => {
  const {children, selected = false, UNSAFE_style, ...rest} = props;

  // ---------------
  // Rendering
  // ---------------

  const renderChildren = () => {
    const kids = flattenChildren(children);
    return kids.map((child) =>
      React.cloneElement(child as React.ReactElement, {
        numberOfColumns: kids.length,
      }),
    );
  };
  return (
    <View
      style={[styles(selected).content, UNSAFE_style]}
      {...rest}
      testID={DataTableRow.displayName}>
      {renderChildren()}
    </View>
  );
};

// ---------------
// StyleSheet
// ---------------
const styles = (selected: boolean) => {
  const backgroundColor = selected
    ? token.componentDataTableRowStateSelectedBackgroundColorDefault //"#f2f8fd"
    : token.componentDataTableRowBackgroundColorDefault; //"#fff"
  return StyleSheet.create({
    container: {
      borderStyle: 'solid',
      borderBottomWidth: StyleSheet.hairlineWidth,
      minHeight: 48,
      paddingHorizontal: 16,
    },
    content: {
      flex: 1,
      flexDirection: 'row',
      backgroundColor: backgroundColor,
      borderBottomColor: token.componentDataTableRowBorderBottomColor, //#e3e4e5
      borderBottomWidth: token.componentDataTableRowBorderWidthBottom,
    },
  });
};

DataTableRow.displayName = 'DataTableRow';
export {DataTableRow};
