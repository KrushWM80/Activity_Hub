import * as React from 'react';
import {StyleProp, StyleSheet, View, ViewStyle} from 'react-native';

import type {CommonViewProps} from '../types/ComponentTypes';

// ---------------
// Props
// ---------------
export type DataTableHeadProps = CommonViewProps & {
  /**
   * The content for the head.
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
 * All Header of the Data Table will be added in DataTableHead
 *
 * ## Usage
 * ```js
 * import {
 *   DataTableHead,
 *   DataTableHeader,
 *   DataTableRow,
 * } from '@walmart/gtp-shared-components';
 *
 * <DataTableHead>
 *     <DataTableRow>
 *       <DataTableHeader>{'ID'}</DataTableHeader>
 *       <DataTableHeader>{'Name'}</DataTableHeader>
 *       <DataTableHeader alignment={'right'}>{'Count'}</DataTableHeader>
 *     </DataTableRow>
 * </DataTableHead>
 * ```
 */
const DataTableHead: React.FC<DataTableHeadProps> = (
  props: DataTableHeadProps,
) => {
  const {children, UNSAFE_style, ...rest} = props;

  // ---------------
  // Rendering
  // ---------------

  return (
    <View
      testID={DataTableHead.displayName}
      style={[styles.header, UNSAFE_style]}
      {...rest}>
      {children}
    </View>
  );
};

// ---------------
// StyleSheet
// ---------------
const styles = StyleSheet.create({
  header: {
    flexDirection: 'row',
  },
});

DataTableHead.displayName = 'DataTableHead';
export {DataTableHead};
