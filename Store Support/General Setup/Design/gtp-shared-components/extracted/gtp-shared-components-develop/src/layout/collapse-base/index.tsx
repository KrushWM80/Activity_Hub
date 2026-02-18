import * as React from 'react';
import {
  ImageStyle,
  TextStyle,
  TouchableOpacity,
  View,
  ViewProps,
} from 'react-native';

import {Icons, IconSize} from '@walmart/gtp-shared-icons';

import {Body} from '../../next/components/Body';
import {Divider} from '../../next/components/Divider';
import {
  getThemeFrom,
  ThemeContext,
  ThemeObject,
} from '../../theme/theme-provider';
import {composed as defaultTheme} from '../theme';

export type CollapseBaseProps = ViewProps & {
  children: React.ReactNode;
  simple?: boolean;
  /** Title text for this Collapse. */
  title: string;
  /** Subtitle text for this Collapse. */
  subtitle?: string;
  /** Icon for this Collapse. */
  icon?: React.ReactElement;
  /** Whether this Collapse is expanded. */
  expanded?: boolean;
  /** This Collapse's press event handler. */
  onToggle: (expanded: boolean) => void;
  /** Whether to show the divider at the top of this Collapse. */
  dividerTop?: boolean;
  /** Whether to show the divider at the bottom of this Collapse. */
  dividerBottom?: boolean;
  /** Additional properties to pass into the touchable element. */
  touchableProps?: ViewProps;
  /** size of the chevron small | 16 | medium | 24 | large | 32. */
  size?: IconSize;
  /** Additional properties to pass icon style(ImageStyle). */
  icon_style?: ImageStyle;
  /** Additional properties to pass title style(TextStyle). */
  title_style?: TextStyle;
  /** Additional properties to pass subtitle style(TextStyle). */
  subTitle_style?: TextStyle;
};

export default class Collapse extends React.Component<CollapseBaseProps> {
  static contextTypes = ThemeContext;

  renderDetails = (theme: ThemeObject) => {
    const {children, expanded} = this.props;
    if (!expanded) {
      return null;
    }
    return <View style={theme.part('details')}>{children}</View>;
  };

  render() {
    const {
      simple,
      expanded,
      icon,
      title,
      subtitle,
      dividerTop,
      dividerBottom,
      onToggle,
      style,
      touchableProps,
      size = 24,
      icon_style,
      title_style,
      subTitle_style,
      ...rootProps
    } = this.props;
    const theme = getThemeFrom(
      this.context,
      defaultTheme,
      'layout',
      'collapse',
      simple ? 'simple' : 'default',
    );
    const chevron = expanded ? (
      <Icons.ChevronUpIcon
        size={size}
        UNSAFE_style={[theme.part('chevron'), icon_style]}
      />
    ) : (
      <Icons.ChevronDownIcon
        size={size}
        UNSAFE_style={[theme.part('chevron'), icon_style]}
      />
    );
    return (
      <View {...rootProps} style={[theme.part('container'), style]}>
        {dividerTop && <Divider />}
        {simple && this.renderDetails(theme)}
        <TouchableOpacity
          accessibilityRole={
            !process.env.STYLEGUIDIST_ENV ? 'button' : undefined
          }
          accessibilityState={{expanded}}
          activeOpacity={1}
          onPress={() => onToggle(!expanded)}
          {...touchableProps}
          style={[theme.part('touchable'), touchableProps?.style]}>
          {icon &&
            React.cloneElement(icon, {
              style: [theme.part('icon'), icon.props.style],
            })}
          <View style={theme.part('textContainer')}>
            {title && (
              <Body UNSAFE_style={[theme.part('title'), title_style]}>
                {title}
              </Body>
            )}
            {subtitle && (
              <Body UNSAFE_style={[theme.part('subtitle'), subTitle_style]}>
                {subtitle}
              </Body>
            )}
          </View>
          {chevron}
        </TouchableOpacity>
        {!simple && this.renderDetails(theme)}
        {dividerBottom && <Divider />}
      </View>
    );
  }
}
