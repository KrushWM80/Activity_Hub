import * as React from 'react';
import {
  StyleProp,
  StyleSheet,
  Text,
  TextStyle,
  View,
  ViewStyle,
} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Badge';

import {getFont} from '../../theme/font';
import type {CommonViewProps} from '../types/ComponentTypes';
import {a11yRole} from '../utils';

// ---------------
// Props
// ---------------
export type BadgeColor =
  | 'blue'
  | 'gray'
  | 'green'
  | 'purple'
  | 'red'
  | 'spark'
  | 'white';
export type BadgeProps = CommonViewProps & {
  /**
   * Color of Badge. Valid values:
   * | 'blue'
   * | 'gray'
   * | 'green'
   * | 'purple'
   * | 'red'
   * | 'spark'
   * | 'white'
   * @default blue
   */
  color?: BadgeColor;
  /**
   * The text label for the badge.
   */
  children?: React.ReactNode;
  /**
   * If provided, the <strong>style</strong> to provide to the container.
   * This property is prefixed with <strong>UNSAFE</strong> as its use
   * often results in <strong>unintended side effects</strong>.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
};

/**
 * Badges are visual indicators of status or count.
 *
 * ## Usage
 * ```js
 * import {Badge} from '@walmart/gtp-shared-components`;
 *
 * <Badge color="blue">1</Badge>
 * <Badge color="gray">2</Badge>
 * <Badge color="green">3</Badge>
 * <Badge color="purple">4</Badge>
 * <Badge color="red">5</Badge>
 * <Badge color="spark">6</Badge>
 * <Badge color="white">7</Badge>
 *
 * ```
 */
const Badge: React.FC<BadgeProps> = (props: BadgeProps) => {
  const {color = 'blue', children, UNSAFE_style, ...rest} = props;

  // ---------------
  // Styles
  // ---------------
  const [containerStyle, setContainerStyle] = React.useState([
    styles.containerHasNoTextLabel,
  ]);
  const [textStyle, setTextStyle] = React.useState([styles.text]);
  const resolveStyles = React.useCallback(() => {
    // Two dimensions which determine styling:
    // - elements that need styles (container, text)
    // - incoming props (color)
    // Note Badges dont require interaction states
    // e.g. [redContainer, blueText]
    setContainerStyle([
      styles[`${color}Container` as keyof typeof styles],
      !children ? styles.containerHasNoTextLabel : styles.containerHasTextLabel,
    ]);
    setTextStyle([styles.text, styles[`${color}Text` as keyof typeof styles]]);
  }, [children, color]);

  React.useEffect(() => {
    resolveStyles();
  }, [resolveStyles]);

  // ---------------
  // Rendering
  // ---------------
  return (
    <View
      testID={Badge.displayName}
      style={[containerStyle, UNSAFE_style]}
      {...rest}>
      <Text accessibilityRole={a11yRole('alert')} style={textStyle}>
        {children}
      </Text>
    </View>
  );
};

// ---------------
// StyleSheet
// ---------------
const styles = StyleSheet.create({
  text: {
    ...getFont('700'),
    fontSize: token.componentBadgeTextLabelFontSize,
    lineHeight: token.componentBadgeTextLabelLineHeight,
  } as TextStyle,
  containerHasTextLabel: {
    alignItems: 'center',
    borderRadius: token.componentBadgeContainerStateHasTextLabelBorderRadius,
    height: token.componentBadgeContainerStateHasTextLabelHeight,
    justifyContent: 'center',
    paddingHorizontal:
      token.componentBadgeContainerStateHasTextLabelPaddingHorizontal,
    minWidth: token.componentBadgeContainerStateHasTextLabelMinWidth,
  } as TextStyle,
  containerHasNoTextLabel: {
    borderRadius: token.componentBadgeContainerStateHasNoTextLabelBorderRadius,
    height: token.componentBadgeContainerStateHasNoTextLabelHeight,
    width: token.componentBadgeContainerStateHasNoTextLabelWidth,
  } as TextStyle,
  //------------------------
  // Colors
  //------------------------
  // blue
  //------------------------
  blueContainer: {
    backgroundColor: token.componentBadgeContainerColorBlueBackgroundColor,
  },
  blueText: {
    color: token.componentBadgeTextLabelColorBlueTextColor,
  },
  //------------------------
  // gray
  //------------------------
  grayContainer: {
    backgroundColor: token.componentBadgeContainerColorGrayBackgroundColor,
  },
  grayText: {
    color: token.componentBadgeTextLabelColorGrayTextColor,
  },
  //------------------------
  // green
  //------------------------
  greenContainer: {
    backgroundColor: token.componentBadgeContainerColorGreenBackgroundColor,
  },
  greenText: {
    color: token.componentBadgeTextLabelColorGreenTextColor,
  },
  //------------------------
  // purple
  //------------------------
  purpleContainer: {
    backgroundColor: token.componentBadgeContainerColorPurpleBackgroundColor,
  },
  purpleText: {
    color: token.componentBadgeTextLabelColorPurpleTextColor,
  },
  //------------------------
  // red
  //------------------------
  redContainer: {
    backgroundColor: token.componentBadgeContainerColorRedBackgroundColor,
  },
  redText: {
    color: token.componentBadgeTextLabelColorRedTextColor,
  },
  //------------------------
  // spark
  //------------------------
  sparkContainer: {
    backgroundColor: token.componentBadgeContainerColorSparkBackgroundColor,
    borderColor: token.componentBadgeContainerColorSparkBorderColor,
    borderWidth: token.componentBadgeContainerColorSparkBorderWidth,
  },
  sparkText: {
    color: token.componentBadgeTextLabelColorSparkTextColor,
    marginTop: -1,
  },
  //------------------------
  // white
  //------------------------
  whiteContainer: {
    backgroundColor: token.componentBadgeContainerColorWhiteBackgroundColor,
    borderColor: token.componentBadgeContainerColorWhiteBorderColor,
    borderWidth: token.componentBadgeContainerColorWhiteBorderWidth,
  },
  whiteText: {
    color: token.componentBadgeTextLabelColorWhiteTextColor,
    marginTop: -1,
  },
});

Badge.displayName = 'Badge';
export {Badge};
