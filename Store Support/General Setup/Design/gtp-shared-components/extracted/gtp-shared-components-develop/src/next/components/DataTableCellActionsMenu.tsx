import * as React from 'react';
import {
  LayoutChangeEvent,
  LayoutRectangle,
  Platform,
  StyleProp,
  StyleSheet,
  useWindowDimensions,
  View,
  ViewStyle,
} from 'react-native';

import * as menuToken from '@livingdesign/tokens/dist/react-native/light/regular/components/Menu';
import RNModal from 'react-native-modal';

import type {CommonViewProps} from '../types/ComponentTypes';
import {
  calculateMenuPosition,
  colors,
  resolveNubbinAlignmentStyle,
  resolvePopUpPositionStyle,
} from '../utils';

import {_Triangle, TriangleDirection} from './_Triangle';
import {MenuPosition} from './Menu';

// ---------------
// Props
// ---------------
export type DataTableCellActionsMenuProps = CommonViewProps & {
  /**
   * The content for the data table cell actions menu.
   */
  children: React.ReactNode;
  /**
   * If the data table cell actions menu is open.
   * @default false
   */
  isOpen?: boolean;
  /**
   * The callback fired when the data table cell actions menu requests to close.
   */
  onClose?: (() => void) | undefined;
  /**
   * The trigger for the data table cell actions menu.
   */
  trigger: React.ReactElement;
  /**
   * If provided, the <strong>style</strong> to provide to the container.
   * This property is prefixed with <strong>UNSAFE</strong> as its use
   * often results in <strong>unintended side effects</strong>.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
};

/**
 * Use DataTableCellActionsMenu and DataTableCellActionsMenuItem for overflow actions
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
 *   DataTableCellActionsMenu,
 *   DataTableCellActionsMenuItem,
 *   IconButton,
 *   Icons,
 *   DataTableRow,
 * } from '@walmart/gtp-shared-components';
 *
 * const menuHeader = ['ID', 'Name', 'Actions'];
 * const menuData = [
 *   {id: 1, name: 'Banana', isEdit: false},
 *   {id: 2, name: 'Peach', isEdit: false},
 *   {id: 3, name: 'Strawberry', isEdit: false},
 * ];
 * const [rowId, setRowId] = React.useState(0);
 * <DataTable>
 *   <DataTableHead>
 *     <DataTableRow>
 *       {menuHeader.map((header, index) => (
 *         <DataTableHeader alignment={index === 2 ? 'right' : 'left'}>
 *           {header}
 *         </DataTableHeader>
 *       ))}
 *     </DataTableRow>
 *   </DataTableHead>
 *   <DataTableBody hor>
 *     {menuData.map((item) => {
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
 *               onPress={() =>
 *                 displayPopupAlert('Action', `Edit button pressed for ${name}`)
 *               }
 *             />
 *             <IconButton
 *               children={<Icons.TrashCanIcon />}
 *               size="small"
 *               onPress={() =>
 *                 displayPopupAlert('Action', `Delete button pressed for ${name}`)
 *               }
 *             />
 *             <DataTableCellActionsMenu
 *               isOpen={rowId === id}
 *               onClose={() => setRowId(0)}
 *               trigger={
 *                 <IconButton
 *                   children={<Icons.MoreIcon />}
 *                   onPress={() => setRowId(id)}
 *                 />
 *               }>
 *               <DataTableCellActionsMenuItem
 *                 onPress={() => {
 *                   setRowId(0);
 *                 }}>
 *                 Email
 *               </DataTableCellActionsMenuItem>
 *               <DataTableCellActionsMenuItem
 *                 onPress={() => {
 *                   setRowId(0);
 *                 }}>
 *                 Print
 *               </DataTableCellActionsMenuItem>
 *               <DataTableCellActionsMenuItem
 *                 onPress={() => {
 *                   setRowId(0);
 *                 }}>
 *                 Disable
 *               </DataTableCellActionsMenuItem>
 *             </DataTableCellActionsMenu>
 *           </DataTableCellActions>
 *         </DataTableRow>
 *       );
 *     })}
 *   </DataTableBody>
 * </DataTable>;
 * ```
 */
const DataTableCellActionsMenu: React.FC<DataTableCellActionsMenuProps> = (
  props: DataTableCellActionsMenuProps,
) => {
  const {children, isOpen, onClose, trigger, UNSAFE_style, ...rest} = props;

  // ---------------
  // Rendering
  // ---------------
  const {height: screenHeight, width: screenWidth} = useWindowDimensions();
  const [position, setPosition] = React.useState<MenuPosition>('bottomLeft');

  let triggerRef = React.useRef<View | null>(null).current;

  const [dataTableMenuLayout, setDataTableMenuLayout] = React.useState<
    LayoutRectangle | undefined
  >();

  const [modalPositionStyle, setModalPositionStyle] = React.useState<
    ViewStyle | undefined
  >();

  const resolveTriangle = () => {
    let direction: TriangleDirection = 'up',
      // @ DataTableCellActionsMenuNubbin tokens are going to removed.Web team is replacing the DataTableCellActionsMenu component with Menu/MenuItem component.so we are HardCoding these Nubbin tokens.
      width = 16,
      height = 6,
      color = '#fff',
      style = {};

    switch (position) {
      case 'topRight':
        direction = 'down';
        style = {
          marginLeft: 8,
        };
        break;
      case 'topLeft':
        direction = 'down';
        style = {
          marginRight: 8,
        };
        break;
      case 'bottomRight':
        style = {
          marginLeft: 8,
        };
        break;
      case 'bottomLeft':
        style = {
          marginRight: 8,
        };
        break;
    }

    return (
      <_Triangle
        width={width}
        height={height}
        direction={direction}
        color={color}
        UNSAFE_style={style}
      />
    );
  };

  // Modal position depends on layout async calls, if not calculated yet
  // set style opacity: 0 to hide it till completed.
  const hideIfModalPositionNotReady = (): ViewStyle => {
    if (!modalPositionStyle) {
      return {opacity: 0};
    } else {
      return {};
    }
  };

  React.useEffect(() => {
    if (isOpen) {
      triggerRef?.measure((x, y, width, height, pageX, pageY) => {
        if (dataTableMenuLayout) {
          setPosition(
            calculateMenuPosition(screenWidth, screenHeight, pageX, pageY),
          );
          const distanceY = 8;
          const containerOffset = 4;
          const nubbinOffset = 8;
          const nubbinWidth = 16;
          const resolvedStyle = resolvePopUpPositionStyle(
            position,
            pageX,
            pageY,
            width,
            height,
            dataTableMenuLayout.width,
            dataTableMenuLayout.height,
            containerOffset, //8
            nubbinOffset,
            nubbinWidth,
          );
          let adjustedMenuStyle;
          switch (position) {
            case 'bottomLeft':
              adjustedMenuStyle = {
                left: resolvedStyle?.left,
                top: resolvedStyle?.top - distanceY,
              };
              break;
            case 'bottomRight':
              adjustedMenuStyle = {
                left: resolvedStyle?.left,
                top: resolvedStyle?.top - distanceY,
              };
              break;
            case 'topLeft':
              adjustedMenuStyle = {
                left: resolvedStyle?.left,
                top: resolvedStyle?.top + distanceY,
              };
              break;
            case 'topRight':
              adjustedMenuStyle = {
                left: resolvedStyle?.left,
                top: resolvedStyle?.top + distanceY,
              };
              break;
            default:
              adjustedMenuStyle = resolvedStyle;
              break;
          }
          setModalPositionStyle(adjustedMenuStyle);
        }
      });
    }
  }, [
    position,
    triggerRef,
    isOpen,
    dataTableMenuLayout,
    screenHeight,
    screenWidth,
  ]);

  // ---------------
  // Rendering
  // ---------------
  return (
    <>
      <View
        testID={DataTableCellActionsMenu.displayName + '-trigger'}
        ref={(element) => (triggerRef = element)}>
        {trigger}
      </View>
      <RNModal
        testID={DataTableCellActionsMenu.displayName}
        onLayout={(event: LayoutChangeEvent) => {
          const layout = event.nativeEvent.layout;
          setDataTableMenuLayout(layout);
        }}
        style={[ss.container, modalPositionStyle, UNSAFE_style]}
        isVisible={isOpen}
        onBackdropPress={() => onClose?.()}
        backdropColor="transparent"
        animationIn="fadeIn"
        animationInTiming={500} // @cory no LD token for animation timing in/out
        animationOut="fadeOut"
        animationOutTiming={500} // @cory no LD token for animation timing in/out
        useNativeDriver={true}
        hideModalContentWhileAnimating={true} // Fixes flicker bug when useNativeDriver: https://github.com/react-native-modal/react-native-modal/issues/268#issuecomment-494768894
        {...rest}>
        <View
          testID={DataTableCellActionsMenu.displayName + '-container'}
          style={[
            ss.secondShadow,
            resolveNubbinAlignmentStyle(position),
            hideIfModalPositionNotReady(),
          ]}>
          {resolveTriangle()}
          <View
            testID={DataTableCellActionsMenu.displayName + '-content'}
            style={[ss.content]}>
            {children}
          </View>
        </View>
      </RNModal>
    </>
  );
};

// ---------------
// Styles
// ---------------
const ss = StyleSheet.create({
  container: {
    position: 'absolute',
    margin: 0, // Removes default margin on react-native-modal
    zIndex: parseInt(menuToken.componentMenuLayoutContainerZIndex, 10), // @cory should be number instead of string
    ...Platform.select({
      android: {
        elevation: 4,
      },
      ios: {
        // Extracted from token.componentDataTableCellActionsMenuContainerElevation
        shadowColor: colors.black, // rgba(0, 0, 0, 0.15)
        shadowOpacity: 0.15, // rgba(0, 0, 0, 0.15)
        shadowRadius: 5, // blurRadius":"5px"
        shadowOffset: {
          width: 0, // offsetX
          height: 3, // offsetY
        },
      },
    }),
  },
  secondShadow: {
    ...Platform.select({
      ios: {
        // Extracted from token.componentDataTableCellActionsMenuContainerElevation
        shadowColor: colors.black, // rgba(0, 0, 0, 0.15)
        shadowOpacity: 0.1, // rgba(0, 0, 0, 0.15)
        shadowRadius: 3, // blurRadius":"5px"
        shadowOffset: {
          width: 0, // offsetX
          height: -1, // offsetY
        },
      },
    }),
  },
  content: {
    minWidth: 100, // At least enough space for nubbin offset
    backgroundColor: menuToken.componentMenuContainerBackgroundColor, // "#fff"
    borderRadius: menuToken.componentMenuContainerBorderRadius, // 4
    paddingHorizontal: menuToken.componentMenuContainerPaddingHorizontal, // 16
    paddingVertical: menuToken.componentMenuContainerPaddingVertical, // 16
  },
});

DataTableCellActionsMenu.displayName = 'DataTableCellActionsMenu';
export {DataTableCellActionsMenu};
