import * as React from 'react';
import {StyleProp, StyleSheet, View, ViewStyle} from 'react-native';

import flattenChildren from 'react-keyed-flatten-children';

import type {CommonViewProps} from '../types/ComponentTypes';

// ---------------
// Props
// ---------------

export type DataTableBodyProps = CommonViewProps & {
  /**
   * The content for the data table body.
   */
  children: React.ReactNode;
  /**
   * If provided, the <strong>style</strong> to provide to the container.
   * This property is prefixed with <strong>UNSAFE</strong> as its use
   * often results in <strong>unintended side effects</strong>.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
};

/**
 * All Data Cells of the Data Table will be added in DataTableBody
 *
 * ## Usage
 * ```js
 * import {DataTableBody, DataTableCell, DataTableRow} from '@walmart/gtp-shared-components';
 *
 * <DataTableBody>
 *   <DataTableRow>
 *     <DataTableCell>{'1'}</DataTableCell>
 *     <DataTableCell>{'Apple'}</DataTableCell>
 *     <DataTableCell variant="numeric">{'20'}</DataTableCell>
 *   </DataTableRow>
 * </DataTableBody>
 * ```
 */
const DataTableBody: React.FC<DataTableBodyProps> = (
  props: DataTableBodyProps,
) => {
  const {children, UNSAFE_style, ...rest} = props;
  const kids = flattenChildren(children);
  // ---------------
  // Rendering
  // ---------------
  return (
    <>
      {kids.map((child, index) => (
        <View
          testID={DataTableBody.displayName}
          {...rest}
          key={index}
          style={styles.dataTableBody}>
          {child}
        </View>
      ))}
    </>
  );
};

// ---------------
// StyleSheet
// ---------------
const styles = StyleSheet.create({
  dataTableBody: {
    flexDirection: 'row',
  },
});

DataTableBody.displayName = 'DataTableBody';
export {DataTableBody};
