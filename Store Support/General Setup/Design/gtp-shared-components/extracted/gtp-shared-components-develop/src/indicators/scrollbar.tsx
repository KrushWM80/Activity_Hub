import * as React from 'react';
import {View, ViewProps} from 'react-native';

import {getThemeFrom, ThemeContext} from '../theme/theme-provider';

import {composed as defaultTheme} from './theme';

export type ScrollbarProps = ViewProps & {
  /** Display this scrollbar full-width. */
  block?: boolean;
  /** The number of segments in this scrollbar. */
  segments: number;
  /** The selected segment. */
  selected: number;
};

/**
 * @deprecated This not in the LD specs and will be removed in a future release
 */
export default class Scrollbar extends React.Component<ScrollbarProps> {
  static contextTypes = ThemeContext;
  static defaultProps: Partial<ScrollbarProps> = {
    block: false,
    segments: 3,
    selected: 0,
  };
  render() {
    const {block, segments, selected, ...rootProps} = this.props;
    const theme = getThemeFrom(
      this.context,
      defaultTheme,
      'indicator',
      'scrollbar',
      block ? 'block' : 'default',
    );
    const renderedSegments = [];
    for (let x = 0; x < segments; x++) {
      renderedSegments.push(
        <View
          key={`Segment_${x}`}
          style={[
            {width: `${100 / segments}%`},
            theme.part(x === selected - 1 ? 'selected' : 'segment'),
          ]}
        />,
      );
    }
    return (
      <View {...rootProps} style={theme.part('container')}>
        <View style={theme.part('line')}>{renderedSegments}</View>
      </View>
    );
  }
}
