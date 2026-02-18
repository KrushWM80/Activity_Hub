import {Platform} from 'react-native';

import {colors} from '../next/utils';

export const shadowNone =
  Platform.OS === 'android'
    ? {
        elevation: 0,
      }
    : {
        shadowOpacity: 0,
      };

export const shadowSmall =
  Platform.OS === 'android'
    ? {
        elevation: 2,
      }
    : {
        shadowColor: colors.black,
        shadowOpacity: 0.15,
        shadowRadius: 2,
        shadowOffset: {
          height: 1,
          width: 0,
        },
      };

export const shadowMedium =
  Platform.OS === 'android'
    ? {
        elevation: 5,
      }
    : {
        shadowColor: colors.black,
        shadowOpacity: 0.15,
        shadowRadius: 5,
        shadowOffset: {
          height: 3,
          width: 0,
        },
      };

export const shadowLarge =
  Platform.OS === 'android'
    ? {
        elevation: 10,
      }
    : {
        shadowColor: colors.black,
        shadowOpacity: 0.15,
        shadowRadius: 10,
        shadowOffset: {
          height: 5,
          width: 0,
        },
      };
