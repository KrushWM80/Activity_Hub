import * as React from 'react';
import {TouchableHighlight, View, ViewProps} from 'react-native';

import {Icons} from '@walmart/gtp-shared-icons';

import {Body} from '../next/components/Body';
import {getThemeFrom, ThemeContext} from '../theme/theme-provider';

import {composed as defaultTheme} from './theme';

type NonRemovable = {
  removable?: false | null;
  onRemove?: false | null;
  /** Position of the arrow */
  point?:
    | 'top'
    | 'bottom'
    | 'left'
    | 'right'
    | 'topLeft'
    | 'topRight'
    | 'bottomLeft'
    | 'bottomRight';
};
type Removable = {
  /** Whether this tooltip has a close button */
  removable: true;
  /** This Tooltip's remove button press handler */
  onRemove: () => void;
  /** Position of the arrow */
  point?:
    | 'top'
    | 'bottom'
    | 'left'
    | 'right'
    | 'topLeft'
    | 'topRight'
    | 'bottomLeft'
    | 'bottomRight';
};

export type TooltipProps = ViewProps & (Removable | NonRemovable);

/**
 * @deprecated use Callout instead
 */
export default class Tooltip extends React.Component<TooltipProps> {
  static defaultProps = {
    point: 'top',
  };
  static contextTypes = ThemeContext;

  render() {
    const {point, removable, onRemove, style, children, ...rootProps} =
      this.props;
    const theme = getThemeFrom(
      this.context,
      defaultTheme,
      'messaging',
      'tooltip',
    );

    return (
      <View
        {...rootProps}
        style={[
          theme.part('static.container'),
          point === 'left' && theme.part('static.containerLeft'),
          point === 'right' && theme.part('static.containerRight'),
          (point === 'top' || point === 'topLeft' || point === 'topRight') &&
            theme.part('static.containerTop'),
          (point === 'bottom' ||
            point === 'bottomLeft' ||
            point === 'bottomRight') &&
            theme.part('static.containerBottom'),
          style,
        ]}>
        <View
          style={[theme.part('static.arrow'), theme.part('static', point)]}
        />
        <View
          style={theme.part(
            removable ? 'removable' : 'default',
            'textContainer',
          )}>
          <Body
            UNSAFE_style={theme.part(
              removable ? 'removable' : 'default',
              'text',
            )}>
            {children}
          </Body>
          {removable && onRemove && (
            <TouchableHighlight
              underlayColor={theme.part('underlayColor')}
              accessibilityLabel="Dismiss Alert"
              accessibilityRole={
                !process.env.STYLEGUIDIST_ENV ? 'button' : undefined
              }
              style={theme.part(
                removable ? 'removable' : 'default',
                'iconContainer',
              )}
              onPress={onRemove}>
              <Icons.CloseIcon
                UNSAFE_style={theme.part(
                  removable ? 'removable' : 'default',
                  'icon',
                )}
              />
            </TouchableHighlight>
          )}
        </View>
      </View>
    );
  }
}
