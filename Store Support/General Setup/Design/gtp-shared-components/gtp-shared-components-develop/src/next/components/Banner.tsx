import * as React from 'react';
import {
  GestureResponderEvent,
  Pressable,
  PressableProps,
  StyleProp,
  StyleSheet,
  Text,
  TextStyle,
  View,
  ViewStyle,
} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Banner';
import {Icons} from '@walmart/gtp-shared-icons';

import {getFont} from '../../theme/font';
import type {CommonViewProps} from '../types/ComponentTypes';
import {a11yRole, capitalize} from '../utils';

import {_LeadingTrailing as _Leading} from './_LeadingTrailing';
export type BannerVariant = 'error' | 'info' | 'success' | 'warning';
export type BannerProps = CommonViewProps & {
  /**
   * The variant of the Banner
   * @default info
   */
  variant?: BannerVariant;
  /**
   * The text label for the Banner.
   */
  children: React.ReactNode;
  /**
   * The props for the close button.
   */
  closeButtonProps?: PressableProps;
  /**
   * The callback fired when the banner requests to close.
   */
  onClose: (event: GestureResponderEvent) => void;
  /**
   * If provided, the <strong>style</strong> to provide to the container.
   * This property is prefixed with <strong>UNSAFE</strong> as its use
   * often results in <strong>unintended side effects</strong>.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
  ///*** NON LD PROPS */
  /**
   * To set the color for close icon.
   */
  closeIconColor?: string;
  /**
   * The leading icon for the Banner.
   * Typically an icon.
   */
  leading?: React.ReactElement;
};

/**
 * Banners provide brief information about a significant incident affecting
 * large numbers (or all) of the population.
 *
 * ## Usage
 * ```js
 * import {Banner} from '@walmart/gtp-shared-components
 *
 * <Banner
 *   variant="info"
 *   children="This is an info banner"
 *   actionButtonProps={{
 *     children: 'Action',
 *     onPress: () => Alert.alert('Action', 'Action pressed'),
 *   }}
 * />
 * ```
 */
const Banner: React.FC<BannerProps> = (props) => {
  const {
    variant = 'info',
    children,
    closeButtonProps,
    onClose,
    UNSAFE_style,
    closeIconColor = 'black',
    leading,
    ...rest
  } = props;

  const resolveContainerStyle = (v: BannerVariant) => {
    return ss[`container${capitalize(v)}` as keyof typeof ss];
  };

  const resolveTextStyle = (v: BannerVariant) => {
    return ss[`textLabel${capitalize(v)}` as keyof typeof ss];
  };

  // --------------
  // Rendering
  // --------------
  const renderLeading = () => {
    return (
      <View style={ss.closeButton}>
        <_Leading node={leading} />
      </View>
    );
  };

  const labelStyle = {
    paddingLeft: leading
      ? 0
      : token.componentBannerTextLabelContainerPaddingStart,
  };

  return (
    <View
      testID={Banner.displayName}
      style={[
        ss.container,
        resolveContainerStyle(variant) as ViewStyle,
        UNSAFE_style,
      ]}
      {...rest}>
      {leading ? renderLeading() : null}
      <View style={[ss.textLabelContainer, labelStyle]}>
        <Text
          accessibilityRole={a11yRole('alert')}
          style={[ss.textLabel, resolveTextStyle(variant)]}>
          {children}
        </Text>
      </View>

      <Pressable
        accessibilityRole={a11yRole('button')}
        accessibilityLabel="close"
        testID="close-button"
        onPress={onClose}
        {...closeButtonProps}>
        <View style={ss.closeButton}>
          <Icons.CloseIcon color={closeIconColor} />
        </View>
      </Pressable>
    </View>
  );
};

// ---------------
// StyleSheet
// ---------------
const ss = StyleSheet.create({
  container: {
    // alignItems: token.componentBannerContainerAlignVertical as any, // @cory, this token has incorrect value 'start'
    alignItems: 'flex-start',
    flexDirection: 'row',
  },
  closeButton: {
    alignItems: 'center',
    height: token.componentBannerCloseButtonHeight,
    justifyContent: 'center',
    width: token.componentBannerCloseButtonWidth,
  },
  textLabel: {
    ...getFont(),
    fontSize: token.componentBannerTextLabelFontSize,
    lineHeight: token.componentBannerTextLabelLineHeight,
    maxWidth: token.componentBannerTextLabelMaxWidth,
    textAlign: token.componentBannerTextLabelTextAlign as any,
  } as TextStyle,
  textLabelContainer: {
    flex: 1,
    paddingBottom: token.componentBannerTextLabelContainerPaddingBottom,
    paddingLeft: token.componentBannerTextLabelContainerPaddingStart,
    paddingRight: token.componentBannerTextLabelContainerPaddingEnd,
    paddingTop: token.componentBannerTextLabelContainerPaddingTop,
  },

  // ---------------
  // Variant: info
  // ---------------
  containerInfo: {
    backgroundColor: token.componentBannerContainerVariantInfoBackgroundColor,
  },
  textLabelInfo: {
    color: token.componentBannerTextLabelVariantInfoTextColor,
  },

  // ---------------
  // Variant: error
  // ---------------
  containerError: {
    backgroundColor: token.componentBannerContainerVariantErrorBackgroundColor,
  },
  textLabelError: {
    color: token.componentBannerTextLabelVariantErrorTextColor,
  },

  // ---------------
  // Variant: success
  // ---------------
  containerSuccess: {
    backgroundColor:
      token.componentBannerContainerVariantSuccessBackgroundColor,
  },
  textLabelSuccess: {
    color: token.componentBannerTextLabelVariantSuccessTextColor,
  },

  // ---------------
  // Variant: warning
  // ---------------
  containerWarning: {
    backgroundColor:
      token.componentBannerContainerVariantWarningBackgroundColor,
  },
  textLabelWarning: {
    color: token.componentBannerTextLabelVariantWarningTextColor,
  },
});

Banner.displayName = 'Banner';
export {Banner};
