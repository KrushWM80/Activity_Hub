import * as React from 'react';
import {
  ImageStyle,
  LayoutAnimation,
  Pressable,
  StyleProp,
  StyleSheet,
  TextStyle,
  View,
  ViewProps,
  ViewStyle,
} from 'react-native';

import {Icons, IconSize} from '@walmart/gtp-shared-icons';

import {getFont} from '../../theme/font';
import type {CommonViewProps} from '../types/ComponentTypes';

import {Body} from './Body';
import {Divider} from './Divider';

// ---------------
// Props
// ---------------
export type CollapseProps = CommonViewProps & {
  /**
   * The details for the Collapse.
   */
  children: React.ReactNode;
  /**
   * Title text for this Collapse.
   */
  title: string;
  /**
   * Subtitle text for this Collapse.
   */
  subtitle?: string;
  /**
   * Icon for this Collapse.
   */
  icon?: React.ReactElement;
  /**
   * Whether this Collapse is expanded.
   * @default false
   */
  expanded?: boolean;
  /**
   * This Collapse's press event handler.
   */
  onToggle: (expanded: boolean) => void;
  /**
   * Whether to show the divider at the top of this Collapse.
   * @default false
   */
  dividerTop?: boolean;
  /**
   * Whether to show the divider at the bottom of this Collapse.
   * @default false
   */
  dividerBottom?: boolean;
  /**
   * Additional properties to pass into the touchable element.
   */
  touchableProps?: ViewProps;
  /**
   * size of the chevron small | 16 | medium | 24 | large | 32.
   * @default 24 | medium
   */
  size?: IconSize;
  /**
   * Additional properties to pass icon style(ImageStyle).
   */
  icon_style?: ImageStyle;
  /**
   * Additional properties to pass title style(TextStyle).
   */
  title_style?: TextStyle;
  /**
   * Additional properties to pass subtitle style(TextStyle)
   */
  subTitle_style?: TextStyle;
  /**
   * If provided, the `style` to provide to the root element. @note This property is prefixed with
   * `UNSAFE` as its use often results in unintended side effects.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
  /**
   * @deprecated use <strong>UNSAFE_style</strong> instead
   * It has no effect
   */
  style?: StyleProp<ViewStyle>;
};

/**
 * The Collapse component is used to put long sections of information under a block that users can expand or collapse.
 *
 * ## Usage
 * ```js
 * import {Collapse} from '@walmart/gtp-shared-components`;
 *
 * <Collapse dividerTop title="Single Line Collapse" onToggle={() => {}}>
 *   <Body>Collapse content appears underneath the toggle area.</Body>
 * </Collapse>
 * ```
 */
const Collapse: React.FC<CollapseProps> = (props) => {
  const {
    expanded = false,
    children,
    icon,
    title,
    subtitle,
    dividerTop = false,
    dividerBottom = false,
    onToggle,
    touchableProps,
    size = 24,
    icon_style,
    title_style,
    subTitle_style,
    UNSAFE_style,
    ...rest
  } = props;

  // ---------------
  // Rendering
  // ---------------
  const renderDetails = () => {
    if (!expanded) {
      return null;
    }
    return (
      <View style={ss.details} testID={`${Collapse.displayName}-details`}>
        {children}
      </View>
    );
  };

  const chevron = React.useMemo(() => {
    if (expanded) {
      return (
        <Icons.ChevronUpIcon
          size={size}
          UNSAFE_style={[ss.chevron, icon_style]}
        />
      );
    }

    return (
      <Icons.ChevronDownIcon
        size={size}
        UNSAFE_style={[ss.chevron, icon_style]}
      />
    );
  }, [expanded, icon_style, size]);

  const showHideCollapseComponent = () => {
    onToggle(!expanded);
    LayoutAnimation.configureNext(LayoutAnimation.Presets.easeInEaseOut);
  };

  return (
    <View
      style={[ss.container, UNSAFE_style]}
      testID={Collapse.displayName}
      {...rest}>
      {dividerTop && <Divider testID={`${Collapse.displayName}-dividerTop`} />}
      <Pressable
        accessibilityRole={!process.env.STYLEGUIDIST_ENV ? 'button' : undefined}
        accessibilityState={{expanded}}
        testID={`${Collapse.displayName}-trigger`}
        onPress={() => {
          showHideCollapseComponent();
        }}
        {...touchableProps}
        style={[ss.touchable, touchableProps?.style]}>
        {icon &&
          React.cloneElement(icon, {
            style: [ss.icon, icon.props.style],
          })}
        <View
          style={ss.textContainer}
          testID={`${Collapse.displayName}-headerContainer`}>
          {title && (
            <Body
              UNSAFE_style={[ss.title, title_style]}
              testID={`${Collapse.displayName}-title`}>
              {title}
            </Body>
          )}
          {subtitle && (
            <Body
              UNSAFE_style={[ss.subtitle, subTitle_style]}
              testID={`${Collapse.displayName}-subTitle`}>
              {subtitle}
            </Body>
          )}
        </View>
        {chevron}
      </Pressable>
      {renderDetails()}
      {dividerBottom && (
        <Divider testID={`${Collapse.displayName}-dividerBottom`} />
      )}
    </View>
  );
};

// ---------------
// Styles
// ---------------

const ss = StyleSheet.create({
  container: {
    flex: 1,
  },
  touchable: {
    padding: 16,
    flexDirection: 'row',
  },
  icon: {
    marginRight: 16,
  },
  textContainer: {
    flex: 1,
  },
  title: {
    ...getFont('bold'),
    fontSize: 16,
    lineHeight: 24,
  } as TextStyle,
  subtitle: {
    ...getFont(),
    fontSize: 14,
    lineHeight: 20,
    marginTop: 4,
  } as TextStyle,
  chevron: {
    marginLeft: 16,
  } as ImageStyle,
  details: {
    padding: 16,
    paddingTop: 0,
  },
});

Collapse.displayName = 'Collapse';
export {Collapse};
