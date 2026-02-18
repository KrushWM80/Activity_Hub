import * as React from 'react';
import {Text, TextProps} from 'react-native';

import {mergeStyles} from '../../next/utils';
import {extractInvalidStyleData} from '../../theme/font';
import {getThemeFrom, ThemeContext} from '../../theme/theme-provider';
import defaultTheme from '../theme';

type ExternalProps = TextProps & {
  /** Inherit color from surrounding typography component */
  inheritColor?: boolean;
  children: React.ReactNode;
  forwardedRef?: () => React.Ref<Text>;
};

export type TextBaseExternalProps = ExternalProps;

type TextBaseProps = ExternalProps & {
  type: string;
};

export default class TextBase extends React.Component<TextBaseProps> {
  static contextTypes = ThemeContext;

  render() {
    const {
      children,
      ellipsizeMode,
      numberOfLines,
      selectable,
      style: allStyles,
      inheritColor,
      type,
      forwardedRef,
      ...rootProps
    } = this.props;
    const typography = getThemeFrom(this.context, defaultTheme, 'typography');
    const fontDefinition = {...typography.part(type)};
    if (inheritColor) {
      delete fontDefinition.color;
    }

    const {style} = extractInvalidStyleData(allStyles);

    return (
      <Text
        {...rootProps}
        ref={forwardedRef}
        ellipsizeMode={ellipsizeMode}
        numberOfLines={numberOfLines}
        selectable={selectable}
        style={mergeStyles(fontDefinition, style)}>
        {children}
      </Text>
    );
  }
}
