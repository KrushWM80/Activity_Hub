import * as React from 'react';
import {
  DimensionValue,
  GestureResponderEvent,
  Platform,
  StyleProp,
  StyleSheet,
  TextStyle,
  View,
  ViewProps,
  ViewStyle,
} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/DataTable';

import {calculateCellWidth} from '../utils';

import {Body, BodySize} from './Body';
import {Checkbox, CheckboxProps} from './Checkbox';
import {DataTableCellVariant} from './DataTableCell';

// ---------------
// Props
// ---------------
export type DataTableCellSelectProps = ViewProps & {
  /**
   * The props spread to the data table cell select's input element.
   */
  checkboxProps?: CheckboxProps;
  /**
   * If the data table cell select is checked.
   * @default false
   */
  checked?: boolean;
  /**
   * If the data table cell select is disabled.
   * @default false
   */
  disabled?: boolean;
  /**
   * If the data table header select is indeterminate.
   * @default false
   */
  indeterminate?: boolean;
  /**
   * The name for the data table cell select.
   */
  name?: string;
  /**
   * The callback fired when the data table cell select requests to change.
   */
  onChange: (event: GestureResponderEvent) => void;
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
 * import {
 *   DataTable,
 *   DataTableBody,
 *   DataTableCell,
 *   DataTableHead,
 *   DataTableHeader,
 *   DataTableHeaderSelect,
 *   DataTableCellSelect,
 *   DataTableRow,
 * } from '@walmart/gtp-shared-components';
 *
 * const selectHeader = ['ID', 'Name'];
 * const selectData = [
 *   {id: 1, name: 'Banana'},
 *   {id: 2, name: 'Peach'},
 *   {id: 3, name: 'Strawberry'},
 * ];
 * const [simpleCellChecked, setSimpleCellChecked] = React.useState([]);
 * const onHeaderChecked = () => {
 *   if (simpleCellChecked.length < 3) {
 *     setSimpleCellChecked([1, 2, 3]);
 *   } else {
 *     setSimpleCellChecked([]);
 *   }
 * };
 * <DataTable>
 *   <DataTableHead>
 *     <DataTableRow>
 *       {selectHeader.map((header, index) => (
 *         <DataTableHeader>{header}</DataTableHeader>
 *       ))}
 *       <DataTableHeaderSelect
 *         alignment={'right'}
 *         onChange={onHeaderChecked}
 *         indeterminate={
 *           simpleCellChecked.length !== 0 && simpleCellChecked.length < 3
 *         }
 *         checked={simpleCellChecked.length === 3}
 *       />
 *     </DataTableRow>
 *   </DataTableHead>
 *   <DataTableBody hor>
 *     {selectData.map((item) => {
 *       const {id, name} = item;
 *       return (
 *         <DataTableRow>
 *           <DataTableCell>{id}</DataTableCell>
 *           <DataTableCell>{name}</DataTableCell>
 *           <DataTableCellSelect
 *             variant="numeric"
 *             checked={simpleCellChecked.includes(id)}
 *             onChange={() => {
 *               if (simpleCellChecked.includes(id)) {
 *                 const removed = simpleCellChecked.filter((item) => item !== id);
 *                 setSimpleCellChecked(removed);
 *               } else {
 *                 setSimpleCellChecked([...simpleCellChecked, id]);
 *               }
 *             }}
 *           />
 *         </DataTableRow>
 *       );
 *     })}
 *   </DataTableBody>
 * </DataTable>;
 * ```
 */
const DataTableCellSelect: React.FC<DataTableCellSelectProps> = (
  props: DataTableCellSelectProps,
) => {
  const {
    checkboxProps,
    checked,
    disabled,
    name,
    onChange,
    numberOfColumns,
    width,
    variant = 'alphanumeric',
    UNSAFE_style,
    ...rest
  } = props;
  const styles = ss(width, variant, numberOfColumns);
  // ---------------
  // Rendering
  // ---------------

  return (
    <View style={[styles.container, UNSAFE_style]} {...rest}>
      {name && (
        <Body
          isMonospace={
            variant === 'numeric' &&
            token.componentDataTableCellVariantNumericAliasOptionsIsMonospace
          }
          size={token.componentDataTableCellAliasOptionsSize as BodySize}
          UNSAFE_style={styles.textStyles}>
          {name}
        </Body>
      )}
      <Checkbox
        {...checkboxProps}
        onPress={onChange}
        checked={checked}
        disabled={disabled}
      />
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
      ? token.componentDataTableCellVariantAlphanumericTextAlign
      : token.componentDataTableCellVariantNumericTextAlign;

  return StyleSheet.create({
    container: {
      width: calculateCellWidth(cWidth, numberOfColumns) as DimensionValue,
      flexDirection: 'row',
      justifyContent: variant === 'alphanumeric' ? 'flex-start' : 'flex-end',
      padding: token.componentDataTableCellSelectContainerPadding, //"16"
      paddingRight: Platform.OS === 'android' ? 25 : 20,
    },
    textStyles: {
      width: '80%',
      marginRight: 5,
      textAlign: textAlignment,
    } as TextStyle,
  });
};
DataTableCellSelect.displayName = 'DataTableCellSelect';
export {DataTableCellSelect};
