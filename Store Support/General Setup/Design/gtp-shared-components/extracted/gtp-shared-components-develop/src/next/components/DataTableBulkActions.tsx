import * as React from 'react';
import {
  GestureResponderEvent,
  Platform,
  StyleProp,
  StyleSheet,
  View,
  ViewProps,
  ViewStyle,
} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/DataTable';
import {Icons} from '@walmart/gtp-shared-icons';
import flattenChildren from 'react-keyed-flatten-children';

import {colors} from '../utils';

import {Body, BodyWeight} from './Body';
import {Button, ButtonProps} from './Button';

// ---------------
// Props
// ---------------

export type DataTableBulkActionsProps = ViewProps & {
  /**
   * The accessibility label for the data table bulk actions.
   * @default "Table actions"
   */
  a11yLabel?: string;
  /**
   * The action content for the data table bulk actions.
   */
  actionContent?: React.ReactNode;
  /**
   * The selected row count for the data table bulk actions.
   * @default 0
   */
  count?: number;
  /**
   * The count label for the data table bulk actions.
   */
  countLabel?: string;
  /**
   * The callback fired when the data table bulk actions requests to clear selected.
   */

  onClearSelected?: (event: GestureResponderEvent) => void;

  /**
   * The props to spread to the data table bulk actions' clear selected button.
   */
  onClearSelectedButtonProps?: ButtonProps;

  /**
   * The callback fired when the data table bulk actions requests to select all.
   */
  onSelectAll?: (event: GestureResponderEvent) => void;
  /**
   * The props to spread to the data table bulk actions' select all button.
   */

  selectAllButtonProps?: ButtonProps;

  /**
   * If provided, the <strong>style</strong> to provide to the container.
   * This property is prefixed with <strong>UNSAFE</strong> as its use
   * often results in <strong>unintended side effects</strong>.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
};

/**
 * The DataTableBulkActions component can be used in conjunction with selection to perform actions on all selected rows. Note that there is no default behavior provided for bulk actions--all desired logic must be defined by the consumer of the component
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
 *   DataTableBulkActions,
 *   DataTableRow,
 *   ButtonGroup,
 *   Button,
 * } from '@walmart/gtp-shared-components';
 *
 * const bulkHeader = ['ID', 'Name'];
 * const bulkData = [
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
 * const selectAll = () => {
 *   setSimpleCellChecked([1, 2, 3]);
 * };
 * const clearAll = () => {
 *   setSimpleCellChecked([]);
 * };
 * <>
 *   <DataTableBulkActions
 *     actionContent={
 *       <ButtonGroup>
 *         <Button
 *           onPress={() =>
 *             displayPopupAlert('Action 1', `Selected Ids ${simpleCellChecked}`)
 *           }>
 *           Custom Action 1
 *         </Button>
 *         <Button
 *           onPress={() =>
 *             displayPopupAlert('Action 2', `Selected Ids ${simpleCellChecked}`)
 *           }>
 *           Custom Action 2
 *         </Button>
 *       </ButtonGroup>
 *     }
 *     count={simpleCellChecked.length}
 *     onClearSelected={clearAll}
 *     onSelectAll={selectAll}
 *   />
 *   <DataTable>
 *     <DataTableHead>
 *       <DataTableRow>
 *         <DataTableHeaderSelect
 *           onChange={onHeaderChecked}
 *           indeterminate={
 *             simpleCellChecked.length !== 0 && simpleCellChecked.length < 3
 *           }
 *           checked={simpleCellChecked.length === 3}
 *         />
 *         {bulkHeader.map((header, index) => (
 *           <DataTableHeader alignment={index === 2 ? 'right' : 'left'}>
 *             {header}
 *           </DataTableHeader>
 *         ))}
 *       </DataTableRow>
 *     </DataTableHead>
 *     <DataTableBody hor>
 *       {bulkData.map((item) => {
 *         const {id, name, isEdit} = item;
 *         return (
 *           <DataTableRow>
 *             <DataTableCellSelect
 *               checked={simpleCellChecked.includes(id)}
 *               onChange={() => {
 *                 if (simpleCellChecked.includes(id)) {
 *                   const removed = simpleCellChecked.filter(
 *                     (item) => item !== id,
 *                   );
 *                   setSimpleCellChecked(removed);
 *                 } else {
 *                   setSimpleCellChecked([...simpleCellChecked, id]);
 *                 }
 *               }}
 *             />
 *             <DataTableCell>{id}</DataTableCell>
 *             <DataTableCell key={'name'}>{name}</DataTableCell>
 *           </DataTableRow>
 *         );
 *       })}
 *     </DataTableBody>
 *   </DataTable>
 * </>;
 * ```
 */
const DataTableBulkActions: React.FC<DataTableBulkActionsProps> = (
  props: DataTableBulkActionsProps,
) => {
  const {
    a11yLabel = 'Table actions',
    actionContent,
    count = 0,
    countLabel = `${count} ${count === 1 ? 'row' : 'rows'} selected`,
    onClearSelected,
    onClearSelectedButtonProps,
    onSelectAll,
    selectAllButtonProps,
    UNSAFE_style,
    ...rest
  } = props;

  // ---------------
  // Rendering
  // ---------------

  const renderSelectAllSection = () => {
    return (
      <View style={styles.contentContainer}>
        <Icons.CheckIcon
          size={token.componentDataTableBulkActionsIconIconSize}
          color={token.componentDataTableBulkActionsIconIconColor}
          UNSAFE_style={styles.checkIcon}
        />
        <Body
          size={token.componentDataTableBulkActionsTextLabelAliasOptionsSize}
          weight={
            token.componentDataTableBulkActionsTextLabelAliasOptionsWeight.toString() as BodyWeight
          }
          UNSAFE_style={styles.countLabel}>
          {countLabel}
        </Body>
        {onSelectAll && (
          <Button
            {...selectAllButtonProps}
            variant={'tertiary'}
            testID={'selectAll'}
            onPress={onSelectAll}>
            {'Select all'}
          </Button>
        )}
        {onClearSelected && (
          <Button
            {...onClearSelectedButtonProps}
            variant={'tertiary'}
            testID={'clearSelected'}
            onPress={onClearSelected}>
            {'Clear selected'}
          </Button>
        )}
      </View>
    );
  };
  const renderActionContent = () => {
    const kids = flattenChildren(actionContent);
    return (
      <View
        style={styles.actionContent}
        testID={DataTableBulkActions.displayName + '-actions'}>
        {kids.map((child, index) => (
          <React.Fragment key={index}>{child}</React.Fragment>
        ))}
      </View>
    );
  };
  return (
    <View
      testID={DataTableBulkActions.displayName}
      style={[styles.container, UNSAFE_style]}
      accessibilityLabel={a11yLabel}
      {...rest}>
      {renderSelectAllSection()}
      {actionContent && renderActionContent()}
    </View>
  );
};

// ---------------
// StyleSheet
// ---------------
const styles = StyleSheet.create({
  container: {
    marginVertical: token.componentDataTableBulkActionsContainerGap,
    padding: token.componentDataTableBulkActionsContainerPadding,
    backgroundColor:
      token.componentDataTableBulkActionsContainerBackgroundColor,
    borderColor: token.componentDataTableBulkActionsContainerBorderColor,
    borderWidth: token.componentDataTableBulkActionsContainerBorderWidth,
    borderRadius: token.componentDataTableBulkActionsContainerBorderRadius,
    alignItems: token.componentDataTableBulkActionsContentAlignVertical,
    justifyContent:
      token.componentDataTableBulkActionsContainerAlignHorizontalBS,
    shadowColor: colors.black, // rgba(0, 0, 0, 0.15)
    ...Platform.select({
      android: {
        elevation: 5, // 5
      },
      ios: {
        // Extracted from token.componentMenuContainerElevation
        shadowOpacity: 0.1, // rgba(0, 0, 0, 0.10)
        shadowRadius: 5, // blurRadius":"10px"
        shadowOffset: {
          width: 0, // "offsetX":0,
          height: 3, // "offsetY":"5px"
        },
      },
    }),
  },
  countLabel: {
    maxWidth: 100,
    marginRight: token.componentDataTableBulkActionsTextLabelMarginEnd,
    color: token.componentDataTableBulkActionsTextLabelTextColor,
  },
  checkIcon: {
    marginRight: token.componentDataTableBulkActionsIconMarginEnd,
    flexShrink: token.componentDataTableBulkActionsIconShrinkFactor,
  },
  contentContainer: {
    flexGrow: token.componentDataTableBulkActionsActionContentGrowFactor,
    flexDirection: 'row',
    alignItems: token.componentDataTableBulkActionsContentAlignVertical,
    justifyContent:
      token.componentDataTableBulkActionsContainerAlignHorizontalBS,
  },
  actionContent: {
    marginTop: 20,
    flexDirection: token.componentDataTableBulkActionsContainerDirectionBM,
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    alignItems: token.componentDataTableBulkActionsContentAlignVertical,
  },
});

DataTableBulkActions.displayName = 'DataTableBulkActions';
export {DataTableBulkActions};
