import * as React from 'react';

import {Icons} from '@walmart/gtp-shared-icons';

import BaseButton, {BaseButtonTheme} from '../buttons/base/button';
import {ThemeContext} from '../theme/theme-provider';

export type ChipProps = {
  /**
   * The ID of this chip.
   */
  id: string;
  selected?: boolean;
  /**
   * Whether this chip is disabled.
   */
  disabled?: boolean;
  multiple?: boolean;
  theme: BaseButtonTheme;
  /**
   * The title for this chip.
   */
  title: string;
  onPress: () => void;
  icon?: React.ReactElement;
  iconRight?: boolean;
};

const Chip: React.FC<ChipProps> = ({
  multiple,
  selected,
  title,
  theme,
  icon,
  iconRight,
  ...props
}) => {
  const resolveIcon = () => {
    if (icon) {
      return icon;
    }
    if (multiple && selected) {
      return <Icons.CheckIcon size={theme.part('static.iconSize') || 12} />;
    }
    // else
    return undefined;
  };

  return (
    <BaseButton
      {...props}
      selected={selected}
      theme={theme}
      accessibilityRole="radio"
      icon={resolveIcon()}
      iconRight={iconRight || multiple}>
      {title}
    </BaseButton>
  );
};

Chip.contextTypes = ThemeContext;
Chip.displayName = 'Chip';

export default Chip;
