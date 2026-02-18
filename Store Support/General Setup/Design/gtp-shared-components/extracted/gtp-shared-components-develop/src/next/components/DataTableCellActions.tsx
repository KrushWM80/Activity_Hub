import * as React from 'react';
import {
  DimensionValue,
  StyleProp,
  StyleSheet,
  View,
  ViewStyle,
} from 'react-native';

import type {CommonViewProps} from '../types/ComponentTypes';
import {calculateCellWidth} from '../utils';

// ---------------
// Props
// ---------------
export type DataTableCellActionsAlignmentType = 'left' | 'right';
export type DataTableCellActionsProps = CommonViewProps & {
  /**
   * The text alignment of the header's text label.</br>
   * Valid values: left | right
   * @default left
   */
  alignment?: DataTableCellActionsAlignmentType;
  /**
   * The content for the data table cell actions.
   */
  children: React.ReactNode;
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
 * The DataTableCellActions cell component can be used with IconButton to add actions to a row.
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
 *   DataTableCellActions,
 *   TextField,
 *   IconButton,
 *   Icons,
 *   DataTableRow,
 * } from '@walmart/gtp-shared-components';
 *
 * const actHeader = ['ID', 'Name', 'Actions'];
 * const actData = [
 *   {id: 1, name: 'Banana', isEdit: false},
 *   {id: 2, name: 'Peach', isEdit: false},
 *   {id: 3, name: 'Strawberry', isEdit: false},
 * ];
 * const [actionData, setActionData] = React.useState(actData);
 * const updateData = (actionType, rowId, updatedValue) => {
 *   let updatedArray = actionData;
 *   if (actionType === 'Edit') {
 *     updatedArray = actionData.map((item) => {
 *       const {id, name, isEdit} = item;
 *       if (id === rowId) {
 *         return {id: id, name: isEdit ? updatedValue : name, isEdit: true};
 *       } else {
 *         return {id, name, isEdit};
 *       }
 *     });
 *   } else if (actionType === 'EditDone') {
 *     updatedArray = actionData.map((item) => {
 *       const {id, name, isEdit} = item;
 *       if (id === rowId) {
 *         return {id: id, name: name, isEdit: false};
 *       } else {
 *         return {id, name, isEdit};
 *       }
 *     });
 *   } else {
 *     updatedArray = actionData.filter((item) => item.id !== rowId);
 *   }
 *   setActionData(updatedArray);
 * };
 * <DataTable>
 *   <DataTableHead>
 *     <DataTableRow>
 *       {actHeader.map((header, index) => (
 *         <DataTableHeader alignment={index === 2 ? 'right' : 'left'}>
 *           {header}
 *         </DataTableHeader>
 *       ))}
 *     </DataTableRow>
 *   </DataTableHead>
 *   <DataTableBody hor>
 *     {actionData.map((item) => {
 *       const {id, name, isEdit} = item;
 *       return (
 *         <DataTableRow>
 *           <DataTableCell>{id}</DataTableCell>
 *           {isEdit ? (
 *             <TextField
 *               value={name}
 *               label={''}
 *               onChangeText={(value) => updateData('Edit', id, value)}
 *               onSubmitEditing={() => {
 *                 updateData('EditDone', id);
 *               }}
 *             />
 *           ) : (
 *             <DataTableCell key={'name'}>{name}</DataTableCell>
 *           )}
 *           <DataTableCellActions alignment="right">
 *             <IconButton
 *               children={<Icons.PencilIcon />}
 *               size="small"
 *               onPress={() => {
 *                 updateData('Edit', id);
 *               }}
 *             />
 *             <IconButton
 *               children={<Icons.TrashCanIcon />}
 *               size="small"
 *               onPress={() => {
 *                 updateData('Delete', id);
 *                 displayPopupAlert('Deleted', `Item ${id} deleted successfully`);
 *               }}
 *             />
 *           </DataTableCellActions>
 *         </DataTableRow>
 *       );
 *     })}
 *   </DataTableBody>
 * </DataTable>;
 * ```
 */
const DataTableCellActions: React.FC<DataTableCellActionsProps> = (
  props: DataTableCellActionsProps,
) => {
  const {
    children,
    alignment = 'left',
    width,
    numberOfColumns,
    UNSAFE_style,
    ...rest
  } = props;

  // ---------------
  // Rendering
  // ---------------

  return (
    <View
      testID={DataTableCellActions.displayName}
      style={[
        styles(alignment, width, numberOfColumns).container,
        UNSAFE_style,
      ]}
      {...rest}>
      {children}
    </View>
  );
};

// ---------------
// StyleSheet
// ---------------
const styles = (
  alignment: DataTableCellActionsAlignmentType,
  cWidth: number | string | undefined,
  numberOfColumns: number | undefined,
) => {
  return StyleSheet.create({
    container: {
      width: calculateCellWidth(cWidth, numberOfColumns) as DimensionValue,
      flexDirection: 'row',
      alignItems: 'center',
      justifyContent: alignment === 'right' ? 'flex-end' : 'flex-start',
    },
  });
};

DataTableCellActions.displayName = 'DataTableCellActions';
export {DataTableCellActions};
