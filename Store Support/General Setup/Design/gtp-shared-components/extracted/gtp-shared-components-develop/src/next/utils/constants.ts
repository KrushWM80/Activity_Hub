import {
  sizeIconLarge,
  sizeIconMedium,
  sizeIconSmall,
} from '@livingdesign/tokens/dist/react-native/light/regular/globals';

export const iconSizes = {
  // '16': sizeIconSmall,
  small: sizeIconSmall,
  // '24': sizeIconMedium,
  medium: sizeIconMedium,
  // '32': sizeIconLarge,
  large: sizeIconLarge,
  '12': 12, // non-standard, legacy
  '48': 48, // non-standard, legacy
  '64': 64, // non-standard, legacy
};

export type IconSizesKey = keyof typeof iconSizes;
export const weekDays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
export const RADIUS = 38;
export const DIAMETER = RADIUS * 2;
export const RING_WIDTH = 8;
//rotate Angle
export const ROTATE_ANGLES = {LEFT: 0, TOP: 90, RIGHT: 180, BOTTOM: 270};
export const DEFAULT_PADDING = 16;
