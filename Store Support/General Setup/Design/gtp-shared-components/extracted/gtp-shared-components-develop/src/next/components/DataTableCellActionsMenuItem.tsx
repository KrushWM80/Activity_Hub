import * as React from 'react';
import {
  GestureResponderEvent,
  Pressable,
  StyleProp,
  StyleSheet,
  TextStyle,
  ViewStyle,
} from 'react-native';

import * as menuToken from '@livingdesign/tokens/dist/react-native/light/regular/components/Menu';

import {getFont} from '../../theme/font';
import {CommonPressableProps} from '../types/ComponentTypes';

import {_LeadingTrailing as _Leading} from './_LeadingTrailing';
import {Body} from './Body';
// ---------------
// Props
// ---------------
export type DataTableCellActionsMenuItemProps = CommonPressableProps & {
  /**
   * The content for the data table cell actions menu item.
   */
  children: React.ReactNode;
  /**
   * The leading icon for the data table cell actions menu item.
   */
  leading?: React.ReactNode;
  /**
   * This menu item press event handler
   */
  onPress: (event: GestureResponderEvent) => void;
  /**
   * If provided, the <strong>style</strong> to provide to the container.
   * This property is prefixed with <strong>UNSAFE</strong> as its use
   * often results in <strong>unintended side effects</strong>.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
};

/**
 * A data table cell actions menu item.
 *
 * ## Usage
 * ```js
 * import {DataTableCellActionsMenuItem, Icons} from '@walmart/gtp-shared-components';
 * <DataTableCellActionsMenuItem
 *   onPress={() => console.log("itemPressed")}>
 * Email
 * </DataTableCellActionsMenuItem>
 * ```
 */
const DataTableCellActionsMenuItem: React.FC<
  DataTableCellActionsMenuItemProps
> = (props: DataTableCellActionsMenuItemProps) => {
  const {children, UNSAFE_style, leading, onPress} = props;
  const [isFocused, setIsFocused] = React.useState(false);

  // ---------------
  // Rendering
  // ---------------
  const renderLeading = (node: React.ReactNode) => {
    return (
      node && (
        <_Leading
          node={node}
          iconProps={{
            UNSAFE_style: {
              marginRight: menuToken.componentMenuItemLeadingIconMarginEnd,
            },
            size: menuToken.componentMenuItemLeadingIconIconSize, // "small"
            color: isFocused
              ? menuToken.componentMenuItemTextLabelTextColorActive // "#002d58"
              : menuToken.componentMenuItemTextLabelTextColorDefault, // "#000"
          }}
        />
      )
    );
  };

  const renderLabel = () => {
    return (
      <Body
        UNSAFE_style={styles.labelStyle}
        selectionColor={menuToken.componentMenuItemTextLabelTextColorActive}>
        {children}
      </Body>
    );
  };

  const handleOnPress = (event: GestureResponderEvent) => {
    setIsFocused(!isFocused);
    onPress(event);
  };
  return (
    <Pressable
      testID={DataTableCellActionsMenuItem.displayName}
      onPress={handleOnPress}
      style={[styles.container, UNSAFE_style]}>
      {renderLeading(leading)}
      {renderLabel()}
    </Pressable>
  );
};
const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    marginVertical: menuToken.componentMenuItemContainerPaddingVertical,
    alignItems: 'flex-start', //"start" @// @cory incorrect TS type here
  },
  labelStyle: {
    ...getFont(),
    lineHeight: menuToken.componentMenuItemTextLabelLineHeight,
    fontSize: menuToken.componentMenuItemTextLabelFontSize,
    textDecorationLine:
      menuToken.componentMenuItemTextLabelTextDecorationDefault,
    color: menuToken.componentMenuItemTextLabelTextColorDefault,
    flexWrap: menuToken.componentMenuItemTextLabelTextWrap ? 'wrap' : 'nowrap',
  } as TextStyle,
});

DataTableCellActionsMenuItem.displayName = 'DataTableCellActionsMenuItem';
export {DataTableCellActionsMenuItem};
