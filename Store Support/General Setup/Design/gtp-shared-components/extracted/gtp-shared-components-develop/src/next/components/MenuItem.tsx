import * as React from 'react';
import {
  GestureResponderEvent,
  Pressable,
  StyleProp,
  StyleSheet,
  TextStyle,
  ViewStyle,
} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Menu';

import {getFont} from '../../theme/font';
import {CommonPressableProps} from '../types/ComponentTypes';

import {_LeadingTrailing as _Leading} from './_LeadingTrailing';
import {Body} from './Body';

// ---------------
// Props
// ---------------
export type MenuItemProps = CommonPressableProps & {
  /**
   * The text label for the menu item.
   */
  children: React.ReactNode;
  /**
   * The leading icon for the menu item.
   */
  leading?: React.ReactNode;
  /**
   * This menu item press event handler
   */
  onPress: (event: GestureResponderEvent) => void;
  /**
   * 	If provided, the `style` to provide to the root element. @note This property is prefixed with
   * `UNSAFE` as its use often results in unintended side effects.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
};

/**
 * MenuItem is a single item in a Menu.
 *
 * ## Usage
 * ```js
 * import {MenuItem} from '@walmart/gtp-shared-components`;
 *
 * <MenuItem onPress={() => console.log('Item 1 clicked')}>Item 1</MenuItem>
 * ```
 */
const MenuItem: React.FC<MenuItemProps> = (props) => {
  const {children, UNSAFE_style, leading, onPress, ...rest} = props;
  const [isFocused, setIsFocused] = React.useState(false);

  // ---------------
  // Rendering
  // ---------------
  const renderLeading = (node: React.ReactNode) => {
    return (
      <_Leading
        node={node}
        iconProps={{
          UNSAFE_style: {
            marginRight: token.componentMenuItemLeadingIconMarginEnd,
          },
          size: token.componentMenuItemLeadingIconIconSize, // "small"
          color: isFocused
            ? token.componentMenuItemLeadingIconIconColorActive // "#002d58"
            : token.componentMenuItemLeadingIconIconColorDefault, // "#000"
        }}
      />
    );
  };

  const renderLabel = () => {
    return (
      <Body
        UNSAFE_style={styles.labelStyle}
        selectionColor={token.componentMenuItemTextLabelTextColorActive} //"#002d58"
      >
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
      testID={MenuItem.displayName}
      onPress={handleOnPress}
      style={[styles.container, UNSAFE_style]}
      {...rest}>
      {renderLeading(leading)}
      {renderLabel()}
    </Pressable>
  );
};
const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: token.componentMenuItemContainerAlignVertical, //"center"
    paddingHorizontal: token.componentMenuItemContainerPaddingHorizontal, //16
    paddingVertical: token.componentMenuItemContainerPaddingVertical, //8
  },
  labelStyle: {
    ...getFont(),
    lineHeight: token.componentMenuItemTextLabelLineHeight, //20
    fontSize: token.componentMenuItemTextLabelFontSize, //14
    textDecorationLine: token.componentMenuItemTextLabelTextDecorationDefault, //"underline"
    color: token.componentMenuItemTextLabelTextColorDefault, //"#2e2f32"
    flexWrap: token.componentMenuItemTextLabelTextWrap ? 'wrap' : 'nowrap', //@cory this token type is not supported in React Native
  } as TextStyle,
  iconStyle: {},
});
MenuItem.displayName = 'MenuItem';
export {MenuItem};
