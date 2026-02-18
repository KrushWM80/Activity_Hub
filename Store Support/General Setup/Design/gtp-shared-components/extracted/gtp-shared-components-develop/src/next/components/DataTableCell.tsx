import * as React from 'react';
import {
  DimensionValue,
  StyleProp,
  StyleSheet,
  TextStyle,
  View,
  ViewStyle,
} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/DataTable';

import type {CommonViewProps} from '../types/ComponentTypes';
import {calculateCellWidth} from '../utils';

import {Body, BodySize} from './Body';

// ---------------
// Props
// ---------------
export type DataTableCellVariant = 'alphanumeric' | 'numeric';
export type DataTableCellProps = CommonViewProps & {
  /**
   * The text label for the cell.
   * Typically a string label.
   */
  children: React.ReactNode;
  /**
   * The variant for the DataTableCell.</br>
   * Valid variants: alphanumeric | numeric
   * @default alphanumeric
   */
  variant?: DataTableCellVariant;
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
 * Data Table Cells represent one piece of information with a specific type. We provide several Cell types to help represent different kinds of information consistently.
 *
 * ## Usage
 * ```js
 * import {DataTableCell} from '@walmart/gtp-shared-components';
 *
 * <DataTableCell
 *  numberOfColumns ={1} variant="alphanumeric">
 *   {"Data Table Cell"}
 * </DataTableCell>
 * ```
 */
const DataTableCell: React.FC<DataTableCellProps> = (
  props: DataTableCellProps,
) => {
  const {
    children,
    width,
    numberOfColumns,
    variant = 'alphanumeric',
    UNSAFE_style,
    ...rest
  } = props;
  const styles = ss(width, variant, numberOfColumns);
  // ---------------
  // Rendering
  // ---------------

  return (
    <View
      testID={DataTableCell.displayName}
      style={[styles.container, UNSAFE_style]}
      {...rest}>
      {typeof children === 'string' ? (
        <Body
          isMonospace={
            variant === 'numeric' &&
            token.componentDataTableCellVariantNumericAliasOptionsIsMonospace
          }
          size={token.componentDataTableCellAliasOptionsSize as BodySize} //"medium"
          UNSAFE_style={styles.textStyles}>
          {children}
        </Body>
      ) : (
        children
      )}
    </View>
  );
};

// ---------------
// StyleSheet
// ---------------
const ss = (
  cWidth: number | string | undefined,
  variant: DataTableCellVariant,
  numberOfColumns: number | undefined,
) => {
  const textAlignment =
    variant === 'alphanumeric'
      ? token.componentDataTableCellVariantAlphanumericTextAlign // "left"
      : token.componentDataTableCellVariantNumericTextAlign; //"right"

  return StyleSheet.create({
    container: {
      width: calculateCellWidth(cWidth, numberOfColumns) as DimensionValue,
      flexDirection: 'row',
      padding: token.componentDataTableCellPadding, //16
    },
    textStyles: {
      width: '100%',
      textAlign: textAlignment,
    } as TextStyle,
  });
};
DataTableCell.displayName = 'DataTableCell';
export {DataTableCell};
