import * as React from 'react';
import {
  DimensionValue,
  FlexStyle,
  Pressable,
  StyleProp,
  StyleSheet,
  TextStyle,
  ViewStyle,
} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/DataTable';
import {Icons} from '@walmart/gtp-shared-icons';

import {getFont, Weights} from '../../theme/font';
import {CommonPressableProps} from '../types/ComponentTypes';
import {calculateCellWidth} from '../utils';

import {Body, BodySize} from './Body';

// ---------------
// Props
// ---------------
export type DataTableHeaderAlignmentType = 'left' | 'right';
export type DataTableHeaderSortType = 'ascending' | 'descending' | 'none';
export type DataTableHeaderProps = CommonPressableProps & {
  /**
   * The text label for the header.
   */
  children: string;
  /**
   * The callback fired when the header requests to sort.
   * Return value as DataTableHeaderSortType
   */
  onSort?: (sortType: DataTableHeaderSortType) => void;
  /**
   * The text alignment of the header's text label.</br>
   * Valid values : 'left' | 'right'
   * @default left
   */
  alignment?: DataTableHeaderAlignmentType;
  /**
   * The sort order for the header's column.</br>
   * Valid values : 'ascending' | 'descending' | 'none'
   * @default none
   */
  sort?: DataTableHeaderSortType;
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
 * Each Data Table Header represents the title of a column and allows a user to sort the Data Table.
 *
 * ## Usage
 * ```js
 * import {DataTableHeader} from '@walmart/gtp-shared-components`;
 * <DataTableHeader
 *  numberOfColumns ={1}>
 *   {"Data Table Header"}
 * </DataTableHeader>
 * ```
 */
const DataTableHeader: React.FC<DataTableHeaderProps> = (
  props: DataTableHeaderProps,
) => {
  const {
    children,
    alignment = 'left',
    onSort,
    sort = 'none',
    width,
    numberOfColumns,
    UNSAFE_style,
    ...rest
  } = props;

  const styles = ss(alignment, width, numberOfColumns);
  // ---------------
  // Rendering
  // ---------------

  const headerIcon = () => {
    const margin =
      alignment === 'left'
        ? {
            marginLeft:
              token.componentDataTableHeaderIconAlignmentLeftMarginStart,
          } //"4"
        : {
            marginRight:
              token.componentDataTableHeaderIconAlignmentRightMarginEnd,
          }; // "4"
    if (sort === 'descending') {
      return (
        <Icons.ArrowDownIcon
          color={token.componentDataTableHeaderIconSortDescendingIconColor} //"#000"
          UNSAFE_style={margin}
        />
      );
    } else if (sort === 'ascending') {
      return (
        <Icons.ArrowUpIcon
          color={token.componentDataTableHeaderIconSortAscendingIconColor} //"#000"
          UNSAFE_style={margin}
        />
      );
    }
  };

  const onHeaderPressed = () => {
    const sortType = sort === 'ascending' ? 'descending' : 'ascending';
    if (onSort) {
      onSort(sortType);
    }
  };
  return (
    <Pressable
      style={[styles.container, UNSAFE_style]}
      {...rest}
      testID={DataTableHeader.displayName}
      onPress={onHeaderPressed}>
      <Body
        size={
          token.componentDataTableHeaderTextLabelAliasOptionsSize as BodySize
        } // "medium",
        UNSAFE_style={[styles.cell]}>
        {children}
      </Body>
      {headerIcon()}
    </Pressable>
  );
};

// ---------------
// StyleSheet
// ---------------
const ss = (
  alignment: DataTableHeaderAlignmentType,
  cWidth: string | number | undefined,
  numberOfColumns: number | undefined,
) => {
  const headerTextAlignment =
    alignment === 'right'
      ? token.componentDataTableHeaderAlignmentRightTextAlign //"right"
      : token.componentDataTableHeaderAlignmentLeftTextAlign; //"left"

  return StyleSheet.create({
    container: {
      width: calculateCellWidth(cWidth, numberOfColumns) as DimensionValue,
      flexDirection: 'row',
      alignItems: token.componentDataTableHeaderAlignVertical as Extract<
        FlexStyle,
        'alignItems'
      >, //'center',
      justifyContent: alignment === 'left' ? 'flex-start' : 'flex-end',
      padding: token.componentDataTableHeaderPadding, //16
      backgroundColor: token.componentDataTableHeaderBackgroundColor, //"#f8f8f8"
    },
    cell: {
      lineHeight: 24,
      ...getFont(
        `${token.componentDataTableHeaderTextLabelAliasOptionsWeight}` as Weights, //700
      ),
      textAlign: headerTextAlignment,
    } as TextStyle,
  });
};
DataTableHeader.displayName = 'DataTableHeader';
export {DataTableHeader};
