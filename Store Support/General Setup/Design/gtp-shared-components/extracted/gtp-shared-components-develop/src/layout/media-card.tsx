import * as React from 'react';
import {View} from 'react-native';

import {getThemeFrom, ThemeContext} from '../theme/theme-provider';

import Card, {SolidCardBaseProps} from './card';
import {composed as defaultTheme} from './theme';

export type MediaCardProps = Omit<SolidCardBaseProps, 'type'> & {
  /** Media content
   *
   * Example: `<Image source={mediaImage} />`
   */
  media: React.ReactNode;
};

/**
 * @deprecated use <strong><Card ... /></strong> instead
 */
class MediaCard extends React.Component<MediaCardProps> {
  static contextTypes = ThemeContext;
  static defaultProps: Partial<MediaCardProps> = {
    contentInset: 'normal',
    roundness: 'small',
  };
  render() {
    const {media, style, roundness, contentInset, children, ...props} =
      this.props;
    const theme = getThemeFrom(
      this.context,
      defaultTheme,
      'layout',
      'mediaCard',
      'static',
    );
    return (
      <Card
        contentInset="none"
        type="solid"
        roundness={roundness}
        style={[theme.part('container'), style]}
        {...props}>
        <View style={[theme.part('media'), theme.part('roundness', roundness)]}>
          {media}
        </View>
        <View style={[theme.part('contentInset', contentInset)]}>
          {children}
        </View>
      </Card>
    );
  }
}

export default MediaCard;
