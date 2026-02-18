import * as React from 'react';
import {
  AccessibilityInfo,
  GestureResponderEvent,
  Platform,
  StyleSheet,
  Text,
  TextStyle,
  TouchableOpacity,
  TouchableOpacityProps,
  View,
  ViewProps,
} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Snackbar';
import {Icons} from '@walmart/gtp-shared-icons';

import {a11yRole, colors} from '../../next/utils';
import {getFont, Weight} from '../../theme/font';

import {Body} from './Body';
import {IconButton} from './IconButton';

// ---------------
// Props
// ---------------
export type SnackbarActionButtonProps = TouchableOpacityProps & {
  /** Button caption */
  caption: string;
  /** This Button's press event handler */
  onPress: (event: GestureResponderEvent) => void;
};

export type SnackbarCloseButtonProps = TouchableOpacityProps & {
  onPress: (event: GestureResponderEvent) => void;
};

export type SnackbarProps = ViewProps & {
  children: string | React.ReactNode;
  /**
   * @deprecated use <strong>actionButton</strong> instead
   */
  button?: SnackbarActionButtonProps;
  /**
   * ActionButton to show on the Snackbar
   */
  actionButton?: SnackbarActionButtonProps;
  /**
   * Close Button (transparent icon X) to show on the Snackbar
   */
  closeButton?: SnackbarCloseButtonProps;
};

/**
 * Snackbars provide brief messages regarding app processes.
 * By default, an SnackBar appears at the bottom of the screen. You can also pass an optional custom vertical position
 * it can be an absolute number (e.g. 200) or a percent (e.g 25%) of the screen height measured from the bottom of the screen.
 * Snackbars contain up to two lines of text directly related to the operation performed.
 * They may contain a text action, but no icons.
 *
 * ## Usage
 * ```js
 * import {Snackbar} from '@walmart/gtp-shared-components`;
 * ```
 */
const Snackbar: React.FC<SnackbarProps> = (props: SnackbarProps) => {
  const {children, style, closeButton, button, ...rootProps} = props;

  React.useEffect(() => {
    if (Platform.OS === 'ios' && children) {
      if (typeof children === 'string') {
        AccessibilityInfo.announceForAccessibility(children);
      } else {
        AccessibilityInfo.announceForAccessibility(children.toString());
      }
    }
  }, [children]);

  // ---------------
  // Rendering
  // ---------------
  const renderActionButton = () => {
    if (props.button) {
      const {caption, disabled, ...rest} = props.button;
      return (
        <TouchableOpacity
          testID={Snackbar.displayName + '-actionButton'}
          accessible={true}
          accessibilityRole={a11yRole('button')}
          accessibilityLabel={caption}
          disabled={!!disabled}
          hitSlop={styles.hitSlop}
          style={styles.button}
          {...rest}>
          <Text style={styles.buttonText}>{caption}</Text>
        </TouchableOpacity>
      );
    }
    if (props.actionButton) {
      const {caption, disabled, ...rest} = props.actionButton;
      return (
        <TouchableOpacity
          testID={Snackbar.displayName + '-actionButton'}
          accessible={true}
          accessibilityRole={a11yRole('button')}
          accessibilityLabel={caption}
          disabled={!!disabled}
          hitSlop={styles.hitSlop}
          style={styles.button}
          {...rest}>
          <Text style={styles.buttonText}>{caption}</Text>
        </TouchableOpacity>
      );
    }
    return null;
  };

  const renderCloseButton = () => {
    if (props.closeButton) {
      return (
        <View style={styles.closeButton}>
          <IconButton
            accessible={true}
            accessibilityRole={a11yRole('button')}
            accessibilityLabel="Close"
            children={<Icons.CloseIcon />}
            size="small"
            color={colors.white}
            onPress={props.closeButton.onPress}
          />
        </View>
      );
    }
    return null;
  };

  return (
    <View testID={Snackbar.displayName} style={[styles.container, style]}>
      <Body
        accessibilityRole={a11yRole('alert')}
        accessibilityLiveRegion={
          Platform.OS === 'android' ? 'assertive' : undefined
        }
        importantForAccessibility={
          Platform.OS === 'android' ? 'yes' : undefined
        }
        UNSAFE_style={styles.text}
        {...rootProps}>
        {children}
      </Body>
      {renderActionButton()}
      {renderCloseButton()}
    </View>
  );
};

// ---------------
// Styles
// ---------------
const styles = StyleSheet.create({
  container: {
    backgroundColor: token.componentSnackbarSnackBackgroundColor,
    margin: 16,
    flexDirection: 'row',
    borderRadius: token.componentSnackbarSnackBorderRadius,
  },
  text: {
    fontSize: token.componentSnackbarTextLabelFontSize,
    lineHeight: token.componentSnackbarTextLabelLineHeight,
    padding: token.componentSnackbarTextLabelPadding,
    color: token.componentSnackbarTextLabelTextColor,
    flex: 1,
  },
  button: {
    color: token.componentSnackbarActionButtonTextColor,
    padding: token.componentSnackbarTextLabelPadding,
    paddingLeft: token.componentSnackbarActionButtonPaddingHorizontal,
    flexShrink: 1,
    maxWidth: 120, // TODO: no token for action button width, check with Cory
  },
  buttonText: {
    ...getFont(
      token.componentSnackbarActionButtonFontWeight.toString() as Weight,
    ),
    fontSize: token.componentSnackbarActionButtonFontSize,
    lineHeight: token.componentSnackbarTextLabelLineHeight,
    color: token.componentSnackbarActionButtonTextColor,
    textDecorationLine: token.componentSnackbarActionButtonTextDecoration,
  } as TextStyle,
  hitSlop: {
    left: 16,
    top: 16,
    right: 16,
    bottom: 16,
  },
  closeButton: {
    paddingTop: 12,
    paddingRight: 4,
  },
});

Snackbar.displayName = 'Snackbar';
export {Snackbar};
