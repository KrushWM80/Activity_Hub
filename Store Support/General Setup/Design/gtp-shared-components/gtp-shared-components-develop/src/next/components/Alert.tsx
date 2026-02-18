import * as React from 'react';
import {
  AccessibilityInfo,
  findNodeHandle,
  StyleProp,
  StyleSheet,
  Text,
  TextStyle,
  View,
  ViewStyle,
} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Alert';
import {Icons} from '@walmart/gtp-shared-icons';

import {getFont} from '../../theme/font';
import type {CommonViewProps} from '../types/ComponentTypes';
import {a11yRole, capitalize} from '../utils';

import {Link, LinkProps} from './Link';

export type AlertVariant = 'error' | 'info' | 'success' | 'warning';
export type AlertProps = CommonViewProps & {
  /**
   * The variant of the Alert
   * @default info
   */
  variant?: AlertVariant;
  /**
   * The text label for the alert.
   */
  children: React.ReactNode;
  /**
   * The props spread to the alert's action button.
   * @note: The action button is using the Link component.
   */
  actionButtonProps?: LinkProps;
  /**
   * If provided, the <strong>style</strong> to provide to the container.
   * This property is prefixed with <strong>UNSAFE</strong> as its use
   * often results in <strong>unintended side effects</strong>.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
  /**
   * its the AccessibilityLabel for the icon.
   * if not provided, it will default to the variant of the Alert
   * example: "info icon", "error icon", "success icon", "warning icon"
   * @default "info icon"
   */
  iconAccessibilityLabel?: string;
  /**
   * @deprecated it has no effect. Provided just for API backwards compatibility.
   */
  icon?: React.JSX.Element;
  /**
   * @deprecated it has no effect. Provided just for API backwards compatibility.
   */
  onDismiss?: () => void;
};

/**
 * Alerts provide brief information and feedback to a user.
 *
 * ## Usage
 * ```js
 * import {Alert} from '@walmart/gtp-shared-components;
 *
 * <Alert
 *   variant="info"
 *   children="This is an info alert"
 *   actionButtonProps={{
 *     children: 'Action',
 *     onPress: () => Alert.alert('Action', 'Action pressed'),
 *   }}
 * />
 * ```
 */
const Alert: React.FC<AlertProps> = (props) => {
  const {
    variant = 'info',
    children,
    actionButtonProps,
    iconAccessibilityLabel = `${variant} icon`,
    UNSAFE_style,
    ...rest
  } = props;
  const alertRef = React.useRef(null);
  React.useEffect(() => {
    if (alertRef && alertRef.current) {
      const reactTag = findNodeHandle(alertRef.current);
      if (reactTag) {
        setTimeout(() => {
          // Due to screen lifecycle, we need to put a minor delay.
          AccessibilityInfo.setAccessibilityFocus(reactTag);
        }, 300);
      }
    }
  }, [alertRef]);
  const resolveContainerStyle = (v: AlertVariant) => {
    return ss[`container${capitalize(v)}` as keyof typeof ss];
  };

  const resolveTextStyle = (v: AlertVariant) => {
    return ss[`textLabel${capitalize(v)}` as keyof typeof ss];
  };

  const resolveIcon = (v: AlertVariant) => {
    switch (v) {
      case 'error':
        return (
          <Icons.ExclamationCircleIcon
            color={token.componentAlertIconVariantErrorIconColor}
            accessibilityLabel={iconAccessibilityLabel}
          />
        );
      case 'info':
        return (
          <Icons.InfoCircleIcon
            color={token.componentAlertIconVariantInfoIconColor}
            accessibilityLabel={iconAccessibilityLabel}
          />
        );
      case 'success':
        return (
          <Icons.CheckCircleIcon
            color={token.componentAlertIconVariantSuccessIconColor}
            accessibilityLabel={iconAccessibilityLabel}
          />
        );
      case 'warning':
        return (
          <Icons.WarningIcon
            color={token.componentAlertIconVariantWarningIconColor}
            accessibilityLabel={iconAccessibilityLabel}
          />
        );
      default:
        return (
          <Icons.ExclamationCircleIcon
            color={token.componentAlertIconVariantInfoIconColor}
            accessibilityLabel={iconAccessibilityLabel}
          />
        );
    }
  };

  const resolveActionButtonColor = (v: AlertVariant) => {
    switch (v) {
      case 'error':
        return token.componentAlertTextLabelVariantErrorTextColor;
      case 'info':
        return token.componentAlertTextLabelVariantInfoTextColor;
      case 'success':
        return token.componentAlertTextLabelVariantSuccessTextColor;
      case 'warning':
        return token.componentAlertTextLabelVariantWarningTextColor;
      default:
        return token.componentAlertTextLabelVariantInfoTextColor;
    }
  };

  // --------------
  // Rendering
  // --------------
  return (
    <View
      testID={Alert.displayName}
      style={[
        ss.container,
        resolveContainerStyle(variant) as ViewStyle,
        UNSAFE_style,
      ]}
      {...rest}>
      <View style={ss.icon}>{resolveIcon(variant)}</View>

      <View style={ss.content}>
        {/* to fix android device overflow issue */}
        {typeof children === 'string' ? (
          <Text
            accessible
            ref={alertRef}
            accessibilityRole={a11yRole('alert')}
            style={[ss.textLabel, resolveTextStyle(variant)]}>
            {children}
          </Text>
        ) : (
          children
        )}
        {actionButtonProps ? (
          <Link
            {...actionButtonProps}
            UNSAFE_style={[ss.link, {color: resolveActionButtonColor(variant)}]}
          />
        ) : null}
      </View>
    </View>
  );
};

// ---------------
// StyleSheet
// ---------------
const ss = StyleSheet.create({
  link: {
    ...getFont(),
    fontSize: token.componentAlertTextLabelFontSize,
    lineHeight: token.componentAlertTextLabelLineHeight,
  } as TextStyle,
  container: {
    alignItems: 'flex-start',
    borderBottomWidth: token.componentAlertContainerBorderWidthBottom,
    borderLeftWidth: token.componentAlertContainerBorderWidthStart,
    borderRadius: token.componentAlertContainerBorderRadius,
    borderRightWidth: token.componentAlertContainerBorderWidthEnd,
    borderTopWidth: token.componentAlertContainerBorderWidthTop,
    flexDirection: 'row',
    paddingLeft:
      token.componentAlertContainerPaddingHorizontal -
      token.componentAlertContainerBorderWidthStart,
    paddingRight:
      token.componentAlertContainerPaddingHorizontal -
      token.componentAlertContainerBorderWidthEnd,
    paddingVertical:
      token.componentAlertContainerPaddingVertical -
      token.componentAlertContainerBorderWidthBottom -
      token.componentAlertContainerBorderWidthTop,
  },
  content: {
    alignItems: 'flex-start',
    flexDirection: 'row',
    flex: 1,
    justifyContent: 'flex-start',
    flexWrap: 'wrap',
  },
  icon: {
    marginRight: token.componentAlertIconMarginEnd,
    marginTop: 2,
  },
  textLabel: {
    ...getFont(),
    fontSize: token.componentAlertTextLabelFontSize,
    lineHeight: token.componentAlertTextLabelLineHeight,
    maxWidth: '95%',
    marginRight: token.componentAlertContainerGapHorizontal,
    // maxWidth: token.componentAlertLabelMaxWidth // @cory this token is missing
  } as TextStyle,

  // ---------------
  // Variant: error
  // ---------------
  containerError: {
    backgroundColor: token.componentAlertContainerVariantErrorBackgroundColor,
    borderBottomColor:
      token.componentAlertContainerVariantErrorBorderColorBottom,
    borderLeftColor: token.componentAlertContainerVariantErrorBorderColorStart,
    borderRightColor: token.componentAlertContainerVariantErrorBorderColorEnd,
    borderTopColor: token.componentAlertContainerVariantErrorBorderColorTop,
  },

  textLabelError: {
    color: token.componentAlertTextLabelVariantErrorTextColor,
  },

  // ---------------
  // Variant: info
  // ---------------
  containerInfo: {
    backgroundColor: token.componentAlertContainerVariantInfoBackgroundColor,
    borderBottomColor:
      token.componentAlertContainerVariantInfoBorderColorBottom,
    borderLeftColor: token.componentAlertContainerVariantInfoBorderColorStart,
    borderRightColor: token.componentAlertContainerVariantInfoBorderColorEnd,
    borderTopColor: token.componentAlertContainerVariantInfoBorderColorTop,
  },

  textLabelInfo: {
    color: token.componentAlertTextLabelVariantInfoTextColor,
  },

  // ---------------
  // Variant: success
  // ---------------
  containerSuccess: {
    backgroundColor: token.componentAlertContainerVariantSuccessBackgroundColor,
    borderBottomColor:
      token.componentAlertContainerVariantSuccessBorderColorBottom,
    borderLeftColor:
      token.componentAlertContainerVariantSuccessBorderColorStart,
    borderRightColor: token.componentAlertContainerVariantSuccessBorderColorEnd,
    borderTopColor: token.componentAlertContainerVariantSuccessBorderColorTop,
  },

  textLabelSuccess: {
    color: token.componentAlertTextLabelVariantSuccessTextColor,
  },

  // ---------------
  // Variant: warning
  // ---------------
  containerWarning: {
    backgroundColor: token.componentAlertContainerVariantWarningBackgroundColor,
    borderBottomColor:
      token.componentAlertContainerVariantWarningBorderColorBottom,
    borderLeftColor:
      token.componentAlertContainerVariantWarningBorderColorStart,
    borderRightColor: token.componentAlertContainerVariantWarningBorderColorEnd,
    borderTopColor: token.componentAlertContainerVariantWarningBorderColorTop,
  },

  textLabelWarning: {
    color: token.componentAlertTextLabelVariantWarningTextColor,
  },
});

Alert.displayName = 'Alert';
export {Alert};
