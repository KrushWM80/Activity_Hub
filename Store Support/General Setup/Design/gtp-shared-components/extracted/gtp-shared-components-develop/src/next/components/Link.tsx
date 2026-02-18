import * as React from 'react';
import {
  GestureResponderEvent,
  StyleProp,
  StyleSheet,
  Text,
  TextStyle,
} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Link';

import {getFont} from '../../theme/font';
import type {CommonViewProps} from '../types/ComponentTypes';
import {a11yRole, colors} from '../utils'; // TODO: Refactor/Align

// ---------------
// Props
// ---------------
export type LinkColorType = 'default' | 'white';
type LinkInteractionState = 'default' | 'pressed' | 'disabled';

export type LinkProps = CommonViewProps & {
  /**
   * This is the text label of the link
   */
  children: React.ReactNode | string;
  /**
   * The callback fired when the link is pressed.
   */
  onPress: (event: GestureResponderEvent) => void;
  /**
   * Color of the text label.
   * Valid values: <strong>'default' | 'white'</strong>
   * @default default
   */
  color?: LinkColorType;
  /**
   * Whether this Link is disabled
   * @default false
   * */
  disabled?: boolean;
  /**
   * If provided, the `style` to provide to the root element.
   * This property is prefixed with `UNSAFE` as its use
   * often results in unintended side effects.
   */
  UNSAFE_style?: StyleProp<TextStyle> | undefined;
};

/**
 * Links can be inserted within a line of text,
 * used on their own, or at the end of content.
 *
 * ## Usage
 *```js
 * import {Link} from '@walmart/gtp-shared-components';
 *
 * <Link onPress={() => {}}>Link</Link>
 * <Link disabled={true} onPress={() => {}}>Disabled Link</link>
 * <Link color="white" onPress={() => {}}>White Link</link>
 * <Link disabled={true} color="white" onPress={() => {}}>Disabled White Link</link>
 *
 * <Text>
 *   {'This '}
 *   <Link onPress={() => {}}>link</Link>
 *   {' is embedded'}
 * </Text>
 *```
 */
const Link: React.FC<LinkProps> = (props: LinkProps) => {
  const {
    children,
    onPress,
    color = 'default',
    disabled = false,
    UNSAFE_style,
    ...rest
  } = props;

  // ---------------
  // Interactions
  // ---------------
  const [interactionState, setInteractionState] =
    React.useState<LinkInteractionState>('default');

  const handleOnPress = (event: GestureResponderEvent): void => {
    onPress(event);
  };

  const handlePressIn = (): void => {
    setInteractionState('pressed');
  };

  const handlePressOut = (): void => {
    setInteractionState('default');
  };

  // ---------------
  // Styles
  // ---------------
  const [textStyle, setTextStyle] = React.useState<Array<StyleProp<TextStyle>>>(
    [styles.default],
  );

  const resolveStyles = React.useCallback(() => {
    if (color === 'default') {
      setTextStyle([styles.default, styles[`${interactionState}`]]);
    } else {
      setTextStyle([styles.default, styles[`${interactionState}White`]]);
    }
  }, [color, interactionState]);

  React.useEffect(() => {
    if (disabled) {
      setInteractionState('disabled');
    } else {
      setInteractionState('default');
    }
    resolveStyles();
  }, [disabled, resolveStyles]);

  const resolveOnPressProps = () => {
    return interactionState !== 'disabled'
      ? {
          onPress: handleOnPress,
          onPressIn: handlePressIn,
          onPressOut: handlePressOut,
        }
      : {};
  };

  // ---------------
  // Rendering
  // ---------------
  return (
    <Text
      accessibilityRole={a11yRole('link')}
      accessibilityState={{disabled}}
      testID={Link.displayName}
      style={[textStyle, UNSAFE_style]}
      {...resolveOnPressProps()}
      {...rest}>
      {children}
    </Text>
  );
};

// ---------------
// StyleSheet
// ---------------
const styles = StyleSheet.create({
  default: {
    ...getFont(),
    fontSize: 16, // TODO: no token for this? Cory to check
    lineHeight: 24, // TODO: no token? Cory to check
    textAlign: 'center', // TODO: no token? Cory to check
    color: token.componentLinkTextLabelTextColorDefault,
    textDecorationLine: token.componentLinkTextLabelTextDecorationDefault,
  } as TextStyle,
  pressed: {
    color: token.componentLinkTextLabelTextColorActive,
  },
  disabled: {
    color: colors.gray['40'], // no token ?
  },
  defaultWhite: {
    color: colors.white,
    textDecorationLine: token.componentLinkTextLabelTextDecorationDefault,
  } as TextStyle,
  pressedWhite: {
    color: colors.white,
    textDecorationLine: token.componentLinkTextLabelTextDecorationActive,
  } as TextStyle,
  disabledWhite: {
    color: colors.gray['50'],
  },
});

Link.displayName = 'Link';
export {Link};
