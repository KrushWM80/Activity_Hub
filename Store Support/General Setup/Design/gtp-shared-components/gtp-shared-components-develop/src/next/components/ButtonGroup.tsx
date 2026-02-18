import * as React from 'react';
import {
  LayoutChangeEvent,
  LayoutRectangle,
  StyleProp,
  StyleSheet,
  useWindowDimensions,
  View,
  ViewStyle,
} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/ButtonGroup';
import flattenChildren from 'react-keyed-flatten-children';

import type {CommonViewProps} from '../types/ComponentTypes';
import {DEFAULT_PADDING} from '../utils';

export type ButtonGroupVariant = 'horizontal' | 'vertical';
// ---------------
// Props
// ---------------
export type ButtonGroupProps = CommonViewProps & {
  /**
   * The content for the ButtonGroup
   */
  children: React.ReactNode;
  /**
   * Whether to display this ButtonGroup full-width
   * @default false
   */
  isFullWidth?: boolean;
  /**
   * If provided, the <strong>style</strong> to provide to the container.
   * This property is prefixed with <strong>UNSAFE</strong> as its use
   * often results in <strong>unintended side effects</strong>.
   */
  UNSAFE_style?: StyleProp<ViewStyle> | undefined;
};

/**
 * Button group displays multiple related actions in a horizontal row
 * to help with arrangement and spacing.
 *
 * ## Usage
 * ```js
 * import {ButtonGroup} from '@walmart/gtp-shared-components`;
 *
 * <ButtonGroup>
 *   <Button
 *     variant="secondary"
 *     onPress={() => {}}>
 *     Secondary
 *   </Button>
 *   <Button
 *     variant="primary"
 *     onPress={() => {}}>
 *     Primary
 *   </Button>
 * </ButtonGroup>
 * ```
 */
const ButtonGroup: React.FC<ButtonGroupProps> = (props: ButtonGroupProps) => {
  const {children, isFullWidth, UNSAFE_style} = props;
  const kids = flattenChildren(children);
  const {width: deviceWidth} = useWindowDimensions();
  const [buttonsLayout, setButtonsLayout] = React.useState<LayoutRectangle>();
  const [buttonsWidth, setButtonsWidth] = React.useState<number>(0);
  const [noButtons, setNoButtons] = React.useState<number>(0);

  React.useEffect(() => {
    if (buttonsLayout && noButtons !== kids.length) {
      setNoButtons(noButtons + 1);
      setButtonsWidth(buttonsWidth + buttonsLayout.width);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [buttonsLayout]);

  /**
   * The function getMaxWidth calculates the maximum width based on the device width and a default
   * padding, taking into account any specified maximum width in the style.
   * @returns The function `getMaxWidth` returns the value of the `maxWidth` variable.
   */
  const getMaxWidth = () => {
    let maxWidth: number = deviceWidth - 2 * DEFAULT_PADDING;
    if (StyleSheet.flatten(UNSAFE_style)?.maxWidth) {
      maxWidth = StyleSheet.flatten(UNSAFE_style)?.maxWidth as number;
    }
    return maxWidth;
  };

  /**
   * The function checks if the width of buttons exceeds the maximum width.
   * @returns a boolean value. If the condition `buttonsWidth > _buttonGroupMaxWidth` is true, then it will
   * return `true`. Otherwise, it will return `false`.
   */
  const isButtonsOverflow = () => {
    const _buttonGroupMaxWidth = getMaxWidth();
    if (buttonsWidth > _buttonGroupMaxWidth) {
      return true;
    }
    return false;
  };

  // ---------------
  // Rendering
  // ---------------
  const _marginVerticalStyle: ViewStyle = {
    marginVertical: isButtonsOverflow() ? 8 : 0,
  };

  const _wrapStyle: ViewStyle = {
    flexWrap: isButtonsOverflow() ? 'wrap' : 'nowrap',
  };

  return (
    <View
      testID={ButtonGroup.displayName}
      style={[ss.containerHorizontal, _wrapStyle, UNSAFE_style]}>
      {React.Children.map(kids, (child: React.ReactNode) => (
        <View
          style={isFullWidth ? ss.buttonContainerFullWidth : {}}
          onLayout={(event: LayoutChangeEvent) => {
            const _buttonLayout = event.nativeEvent.layout;
            setButtonsLayout(_buttonLayout);
          }}>
          {
            // @ts-ignore
            React.cloneElement(child, {
              isFullWidth,
              UNSAFE_style: isFullWidth
                ? {}
                : [ss.childHorizontal, _marginVerticalStyle],
            })
          }
        </View>
      ))}
    </View>
  );
};

// ---------------
// Styles
// ---------------
const ss = StyleSheet.create({
  containerHorizontal: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
  },
  childHorizontal: {
    marginHorizontal: 8,
  },
  buttonContainerFullWidth: {
    marginHorizontal: token.componentButtonGroupContainerGap / 2,
    flex: 1,
  },
});

ButtonGroup.displayName = 'ButtonGroup';
export {ButtonGroup};
