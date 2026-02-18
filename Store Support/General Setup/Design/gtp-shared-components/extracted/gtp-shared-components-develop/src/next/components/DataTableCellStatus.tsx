import * as React from 'react';
import {
  DimensionValue,
  StyleProp,
  StyleSheet,
  View,
  ViewStyle,
} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/DataTable';

import type {CommonViewProps} from '../types/ComponentTypes';
import {calculateCellWidth} from '../utils';

// ---------------
// Props
// ---------------
export type DataTableCellSelectStatusAlignmentType = 'left' | 'right';
export type DataTableCellSelectStatusProps = CommonViewProps & {
  /**
   * The tag(s) for the cell.
   */
  children: React.ReactNode;
  /**
   * The text alignment of the header's text label.</br>
   * Valid values: left | right
   * @default left
   */
  alignment?: DataTableCellSelectStatusAlignmentType;
  /**
   * The width of the column.
   */
  width?: string | number;
  /**
   * The total number of Columns
   */
  numberOfColumns?: number;
  /**
   * If provided, the <strong>style</strong> to provide to the container.
   * This property is prefixed with <strong>UNSAFE</strong> as its use
   * often results in <strong>unintended side effects</strong>.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
};

/**
 * Use the DataTableCellStatus component in combination with the Tag component to represent status in a cell:
 *
 * ## Usage
 * ```js
 * import {
 *   DataTable,
 *   DataTableBody,
 *   DataTableCell,
 *   DataTableHead,
 *   DataTableHeader,
 *   DataTableCellStatus,
 *   DataTableRow,
 *   Tag,
 * } from '@walmart/gtp-shared-components';
 *
 * const statusHeader = ['Name', 'Status'];
 * const statusData = [
 *   {id: 1, name: 'Freyja Atli', status: 'Healthy'},
 *   {id: 2, name: 'Borghildr Sigurdr', status: 'Upset stomach'},
 *   {id: 3, name: 'Brynhild Idun', status: 'Unamused'},
 * ];
 * const renderTag = (status, id) => {
 *   const color = id === 1 ? 'green' : id === 2 ? 'purple' : 'gray';
 *   return (
 *     <Tag color={color} variant={'tertiary'}>
 *       {status}
 *     </Tag>
 *   );
 * };
 *
 * <DataTable>
 *   <DataTableHead>
 *     <DataTableRow>
 *       {statusHeader.map((header, index) => (
 *         <DataTableHeader>{header}</DataTableHeader>
 *       ))}
 *     </DataTableRow>
 *   </DataTableHead>
 *   <DataTableBody>
 *     {statusData.map((item) => {
 *       const {id, name, status} = item;
 *       return (
 *         <DataTableRow>
 *           <DataTableCell>{name}</DataTableCell>
 *           <DataTableCellStatus>{renderTag(status, id)}</DataTableCellStatus>
 *         </DataTableRow>
 *       );
 *     })}
 *   </DataTableBody>
 * </DataTable>;
 * ```
 */
const DataTableCellStatus: React.FC<DataTableCellSelectStatusProps> = (
  props: DataTableCellSelectStatusProps,
) => {
  const {
    children,
    width,
    numberOfColumns,
    alignment = 'left',
    UNSAFE_style,
  } = props;
  const styles = ss(alignment, width, numberOfColumns);
  // ---------------
  // Rendering
  // ---------------
  return (
    <View
      testID={DataTableCellStatus.displayName}
      style={[styles.container, UNSAFE_style]}>
      {children}
    </View>
  );
};

// ---------------
// StyleSheet
// ---------------
const ss = (
  alignment: DataTableCellSelectStatusAlignmentType,
  cWidth: number | string | undefined,
  numberOfColumns: number | undefined,
) => {
  const padding = token.componentDataTableCellStatusPadding; //"16"

  return StyleSheet.create({
    container: {
      width: calculateCellWidth(cWidth, numberOfColumns) as DimensionValue,
      padding: padding,
      alignItems: alignment === 'left' ? 'flex-start' : 'flex-end',
    },
  });
};

DataTableCellStatus.displayName = 'DataTableCellStatus';
export {DataTableCellStatus};
