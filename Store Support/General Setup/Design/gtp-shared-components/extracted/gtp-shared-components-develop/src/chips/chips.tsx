import * as React from 'react';
import {View, ViewProps} from 'react-native';

import {BaseButtonExternalProps, BaseButtonTheme} from '../buttons/base/button';
import {getThemeFrom, ThemeContext} from '../theme/theme-provider';

import Chip, {ChipProps} from './Chip';
import {composed as defaultTheme} from './theme';

type ChipsBaseProps = {
  /** This `Chips`' onPress handler. */
  onPress: (id: string) => void;
  /**
   * The size of the chips.
   *
   * `medium` size is recommended for low emphasis and hierarchy.
   * `large` size is recommended for high emphasis and hierarchy.
   */
  size?: 'medium' | 'large' | 'xlarge';
  /**
   * The selected chip IDs.
   */
  selected?: string | Array<string>;
  /**
   * List of all chips to render.
   */
  chips: Array<Omit<ChipProps, 'type' | 'theme' | 'onPress' | 'selected'>>;
};

export type ChipsExternalProps = ChipsBaseProps &
  Omit<BaseButtonExternalProps, 'onPress' | 'selected'>;

export type ChipsProps = ViewProps &
  Omit<ChipsExternalProps, 'multiple' | 'selected'> &
  (
    | {
        /** Allow multiple selections. */
        multiple: true;
        /**
         * The selected chip IDs.
         */
        selected?: Array<string>;
      }
    | {
        /** Allow multiple selections. */
        multiple?: false;
        /**
         * The selected chip ID.
         */
        selected?: string;
      }
  );

/**
 * Chips allow users to enter information, make selections, filter content, or trigger actions. Chips should appear dynamically as a group of multiple interactive elements.
 *
 * ```jsx
 * import {Chips} from '@walmart/gtp-shared-components';
 * ```
 */
class Chips extends React.Component<ChipsProps> {
  static contextTypes = ThemeContext;
  static defaultProps: Partial<ChipsBaseProps> = {
    size: 'medium',
  };
  static displayName = 'Chips';

  render() {
    const {chips, multiple, size, selected, onPress} = this.props;
    const theme = getThemeFrom(
      this.context,
      defaultTheme,
      'chips',
      `${multiple ? 'multiple' : 'single'}${size}`,
    ) as BaseButtonTheme;

    return (
      <View
        style={theme.part('static.container')}
        accessibilityRole="radiogroup">
        {chips.map((chip) => (
          <Chip
            key={chip.id}
            {...chip}
            multiple={!!multiple}
            theme={theme}
            onPress={() => onPress(chip.id)}
            selected={
              Array.isArray(selected)
                ? selected.includes(chip.id)
                : selected === chip.id
            }
          />
        ))}
      </View>
    );
  }
}

export default Chips;
