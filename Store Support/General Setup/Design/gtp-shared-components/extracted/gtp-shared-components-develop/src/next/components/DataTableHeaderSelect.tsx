import * as React from 'react';
import {
  DimensionValue,
  GestureResponderEvent,
  StyleProp,
  StyleSheet,
  TextStyle,
  View,
  ViewProps,
  ViewStyle,
} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/DataTable';

import {getFont, Weights} from '../../theme/font';
import {calculateCellWidth} from '../utils';

import {Body, BodySize} from './Body';
import {Checkbox, CheckboxProps} from './Checkbox';
import {DataTableHeaderAlignmentType} from './DataTableHeader';

// ---------------
// Props
// ---------------
export type DataTableHeaderSelectProps = ViewProps & {
  /**
   * The accessibility label for the data table header select.
   * @default 'Toggle all rows'
   */
  a11yCheckboxLabel?: string;
  /**
   * The props spread to the data table header select's input element.
   */
  checkboxProps?: CheckboxProps;
  /**
   * If the data table header select is checked.
   * @default false
   */
  checked?: boolean;
  /**
   * If the data table header select is disabled.
   * @default false
   */
  disabled?: boolean;
  /**
   * If the data table header select is indeterminate.
   * @default false
   */
  indeterminate?: boolean;
  /**
   * The name for the data table header select.
   */
  name?: string;
  /**
   * The callback fired when the data table header select requests to change.
   */
  onChange: (event: GestureResponderEvent) => void;
  /**
   * The text alignment of the header's text label.</br>
   * Valid values: left | right
   * @default left
   */
  alignment?: DataTableHeaderAlignmentType;
  /**
   * The width of the column.
   */
  width?: string | number;
  /**
   * The total number of Columns
   */
  numberOfColumns: number;
  /**
   * If provided, the <strong>style</strong> to provide to the container.
   * This property is prefixed with <strong>UNSAFE</strong> as its use
   * often results in <strong>unintended side effects</strong>.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
};

/**
 * Column selection is implemented with the DataTableHeaderSelect and DataTableCellSelect components.
 *
 * ## Usage
 * ```js
 * import {DataTableHeaderSelect} from '@walmart/gtp-shared-components`;
 *
 * const [simpleCellChecked, setSimpleCellChecked] = React.useState(false);
 *
 * <DataTableHeaderSelect
 *  name={'Options'}
 *  numberOfColumns ={1}
 *  alignment={'right'}
 *  onChange={()=>setSimpleCellChecked(!simpleCellChecked)}
 *  checked={simpleCellChecked}
 * />
 * ```
 */
const DataTableHeaderSelect: React.FC<DataTableHeaderSelectProps> = (
  props: DataTableHeaderSelectProps,
) => {
  const {
    a11yCheckboxLabel,
    checkboxProps,
    checked = false,
    disabled = false,
    indeterminate = false,
    name,
    onChange,
    UNSAFE_style,
    numberOfColumns,
    alignment = 'left',
    width,
    ...rest
  } = props;
  const styles = ss(numberOfColumns, width, alignment);
  // ---------------
  // Rendering
  // ---------------

  return (
    <View style={[styles.container, UNSAFE_style]} {...rest}>
      {name && (
        <Body
          size={
            token.componentDataTableHeaderTextLabelAliasOptionsSize as BodySize
          } // "medium",
          UNSAFE_style={[styles.cell]}>
          {name}
        </Body>
      )}
      <Checkbox
        {...checkboxProps}
        onPress={onChange}
        accessibilityLabel={a11yCheckboxLabel}
        checked={checked}
        disabled={disabled}
        indeterminate={indeterminate}
        UNSAFE_style={styles.CheckboxStyle}
      />
    </View>
  );
};

// ---------------
// StyleSheet
// ---------------
const ss = (
  numberOfColumns: number | undefined,
  cWidth: string | number | undefined,
  alignment: DataTableHeaderAlignmentType,
) => {
  const headerTextAlignment =
    alignment === 'right'
      ? token.componentDataTableHeaderAlignmentRightTextAlign
      : token.componentDataTableHeaderAlignmentLeftTextAlign;

  return StyleSheet.create({
    container: {
      width: calculateCellWidth(cWidth, numberOfColumns) as DimensionValue,
      flexDirection: 'row',
      justifyContent: alignment === 'right' ? 'flex-end' : 'flex-start',
      padding: token.componentDataTableHeaderSelectContainerPadding, //16
      backgroundColor:
        token.componentDataTableHeaderSelectContainerBackgroundColor, //"#f8f8f8"
    },
    cell: {
      width: '80%',
      ...getFont(
        `${token.componentDataTableHeaderTextLabelAliasOptionsWeight}` as Weights, //700
      ),
      marginRight: 5,
      textAlign: headerTextAlignment,
    } as TextStyle,
    CheckboxStyle: {
      marginRight: 5,
    },
  });
};

DataTableHeaderSelect.displayName = 'DataTableHeaderSelect';
export {DataTableHeaderSelect};
