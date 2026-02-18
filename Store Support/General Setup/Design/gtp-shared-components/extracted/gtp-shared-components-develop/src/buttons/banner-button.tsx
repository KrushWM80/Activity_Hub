import * as React from 'react';
import {Text} from 'react-native';

import {removeChildren} from '../next/utils';
import {getThemeFrom, ThemeContext} from '../theme/theme-provider';

import BaseButton, {BaseButtonExternalProps} from './base/button';
import {composed as defaultTheme} from './theme';

export type BannerButtonProps = Omit<
  BaseButtonExternalProps,
  'block' | 'isFullWidth' | 'iconRight' | 'children'
> & {
  /** This Banner Button's title text */
  title: string;
  /** This Banner Button's description text */
  description: string;
};

/**
 * @deprecated this is not in the LD3 specs
 */
export default class BannerButton extends React.Component<BannerButtonProps> {
  static contextTypes = ThemeContext;
  static displayName = 'BannerButton';
  render() {
    const {title, description, ...props} = this.props;
    const theme = getThemeFrom(this.context, defaultTheme, 'buttons.banner');

    return (
      <BaseButton
        isFullWidth
        theme={theme}
        {...removeChildren(props)}
        iconNoMargin>
        <Text style={theme.part('default.title')}>{title}</Text>
        {'\n'}
        <Text style={theme.part('default.description')}>{description}</Text>
      </BaseButton>
    );
  }
}
