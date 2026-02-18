import {
  sizeIconSmall,
  sizeIconMedium,
  sizeIconLarge,
} from '@livingdesign/tokens/dist/react-native/light/regular/globals';

export const iconSizes = {
  '16': sizeIconSmall,
  small: sizeIconSmall,
  '24': sizeIconMedium,
  medium: sizeIconMedium,
  '32': sizeIconLarge,
  large: sizeIconLarge,
  '12': 12, // non-standard, legacy
  '48': 48, // non-standard, legacy
  '64': 64, // non-standard, legacy
};

export type IconSize = 16 | 24 | 32 | 'small' | 'medium' | 'large';
