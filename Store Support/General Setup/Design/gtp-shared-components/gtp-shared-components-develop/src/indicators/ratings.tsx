import * as React from 'react';
import {View, ViewProps} from 'react-native';

import {Icons} from '@walmart/gtp-shared-icons';

import LinkButton from '../buttons/link-button';
import {Caption} from '../next/components/Caption';
import {getThemeFrom, ThemeContext} from '../theme/theme-provider';

import {composed as defaultTheme} from './theme';

export type RatingsProps = ViewProps & {
  /** The value of this ratings component, 1-5 */
  value: number;
  /** The number of ratings. */
  count: number;
  /** The press handler for this ratings component.  If set, the number of ratings will appear as a link. */
  onPress?: () => void;
};

/**
 * @deprecated use Rating instead
 */
export default class Ratings extends React.Component<RatingsProps> {
  static contextTypes = ThemeContext;

  render() {
    const {value, count, onPress, style, ...rootProps} = this.props;
    const theme = getThemeFrom(
      this.context,
      defaultTheme,
      'indicator',
      'ratings',
      'default',
    );

    const stars = [1, 2, 3, 4, 5].map((index: number) => {
      const Icon: React.ElementType =
        value >= index
          ? Icons.StarFillIcon
          : value > index - 1
          ? Icons.StarHalfIcon
          : Icons.StarIcon;
      return <Icon key={`star_${index}`} color="black" size={12} />;
    });

    return (
      <View {...rootProps} style={[theme.part('container'), style]}>
        {stars}
        {onPress ? (
          <LinkButton small onPress={onPress} style={theme.part('link')}>
            {count} Reviews
          </LinkButton>
        ) : (
          <Caption UNSAFE_style={theme.part('text')}>{count}</Caption>
        )}
      </View>
    );
  }
}
