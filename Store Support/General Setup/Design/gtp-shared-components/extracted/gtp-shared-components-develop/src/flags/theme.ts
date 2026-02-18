import {colors, composeTheme} from '../next/utils';
import {getFont} from '../theme/font';

const badges = {
  default: {
    container: {
      paddingVertical: 3,
      paddingHorizontal: 7,
      borderWidth: 1,
      borderColor: 'transparent',
      borderStyle: 'solid',
      alignItems: 'center',
      justifyContent: 'center',
      alignSelf: 'flex-start',
      borderRadius: 2,
      backgroundColor: colors.white,
    },
    text: {
      ...getFont(),
      fontSize: 12,
      lineHeight: 16,
      color: colors.black,
    },
  },
  availability: {
    container: {
      backgroundColor: colors.blue['10'],
    },
    text: {
      color: colors.blue['120'],
    },
  },
  informational: {
    container: {
      backgroundColor: colors.gray['10'],
    },
    text: {
      color: colors.gray['110'],
    },
  },
  media: {
    container: {
      borderColor: colors.gray['100'],
    },
    text: {
      color: colors.gray['100'],
    },
  },
  count: {
    container: {
      paddingVertical: 1,
      paddingHorizontal: 1,
      borderRadius: 9999,
      borderColor: colors.gray['50'],
    },
    text: {
      fontSize: 10,
      lineHeight: 12,
      minWidth: 6,
      height: 12,
      marginHorizontal: 3,
      textAlign: 'center',
      color: colors.gray['110'],
    },
  },
};

const flags = {
  default: {
    container: {
      paddingVertical: 3,
      paddingHorizontal: 7,
      borderWidth: 1,
      borderColor: 'transparent',
      borderStyle: 'solid',
      alignItems: 'center',
      justifyContent: 'center',
      alignSelf: 'flex-start',
      borderRadius: 2,
      backgroundColor: colors.white,
    },
    text: {
      ...getFont(),
      fontSize: 12,
      lineHeight: 16,
      color: colors.black,
    },
  },
  general: {
    container: {
      borderColor: colors.blue['110'],
    },
    text: {
      color: colors.blue['110'],
    },
  },
  rollback: {
    container: {
      borderColor: colors.red['100'],
    },
    text: {
      color: colors.red['100'],
    },
  },
  filled: {
    container: {
      backgroundColor: colors.blue['110'],
    },
    text: {
      color: colors.white,
    },
  },
};

const supportive = {
  default: {
    container: {
      flexDirection: 'row',
      alignItems: 'center',
    },
    text: {
      fontSize: 12,
      lineHeight: 16,
      marginLeft: 4,
    },
  },
};

const tags = {
  default: {
    container: {
      paddingVertical: 3,
      paddingHorizontal: 7,
      borderWidth: 1,
      borderColor: 'transparent',
      borderStyle: 'solid',
      alignItems: 'center',
      justifyContent: 'center',
      alignSelf: 'flex-start',
      borderRadius: 2,
      backgroundColor: colors.white,
      flexDirection: 'row',
    },
    icon: {
      color: colors.white,
      marginRight: 4,
      size: 16,
    },
    text: {
      ...getFont(),
      fontSize: 12,
      lineHeight: 16,
      color: colors.white,
    },
  },
  primary: {
    container: {
      backgroundColor: colors.blue['160'],
    },
  },
  secondary: {
    container: {
      borderColor: colors.blue['130'],
    },
    icon: {
      color: colors.blue['130'],
    },
    text: {
      color: colors.blue['130'],
    },
  },
  tertiary: {
    container: {
      backgroundColor: colors.blue['10'],
    },
    icon: {
      color: colors.blue['130'],
    },
    text: {
      color: colors.blue['130'],
    },
  },
  primaryRed: {
    container: {
      backgroundColor: colors.red['100'],
    },
  },
  secondaryRed: {
    container: {
      borderColor: colors.red['130'],
    },
    icon: {
      color: colors.red['130'],
    },
    text: {
      color: colors.red['130'],
    },
  },
  tertiaryRed: {
    container: {
      backgroundColor: colors.red['10'],
    },
    icon: {
      color: colors.red['130'],
    },
    text: {
      color: colors.red['130'],
    },
  },
  primarySpark: {
    container: {
      backgroundColor: colors.spark['100'],
    },
    icon: {
      color: colors.black,
    },
    text: {
      color: colors.black,
    },
  },
  secondarySpark: {
    container: {
      borderColor: colors.spark['140'],
    },
    icon: {
      color: colors.spark['140'],
    },
    text: {
      color: colors.spark['140'],
    },
  },
  tertiarySpark: {
    container: {
      backgroundColor: colors.spark['10'],
    },
    icon: {
      color: colors.spark['140'],
    },
    text: {
      color: colors.spark['140'],
    },
  },
  primaryGreen: {
    container: {
      backgroundColor: colors.green['100'],
    },
  },
  secondaryGreen: {
    container: {
      borderColor: colors.green['130'],
    },
    icon: {
      color: colors.green['130'],
    },
    text: {
      color: colors.green['130'],
    },
  },
  tertiaryGreen: {
    container: {
      backgroundColor: colors.green['10'],
    },
    icon: {
      color: colors.green['130'],
    },
    text: {
      color: colors.green['130'],
    },
  },
  primaryPurple: {
    container: {
      backgroundColor: colors.purple['100'],
    },
  },
  secondaryPurple: {
    container: {
      borderColor: colors.purple['130'],
    },
    icon: {
      color: colors.purple['130'],
    },
    text: {
      color: colors.purple['130'],
    },
  },
  tertiaryPurple: {
    container: {
      backgroundColor: colors.purple['10'],
    },
    icon: {
      color: colors.purple['130'],
    },
    text: {
      color: colors.purple['130'],
    },
  },
  primaryGray: {
    container: {
      backgroundColor: colors.gray['100'],
    },
  },
  secondaryGray: {
    container: {
      borderColor: colors.gray['130'],
    },
    icon: {
      color: colors.gray['130'],
    },
    text: {
      color: colors.gray['130'],
    },
  },
  tertiaryGray: {
    container: {
      backgroundColor: colors.gray['10'],
    },
    icon: {
      color: colors.gray['130'],
    },
    text: {
      color: colors.gray['130'],
    },
  },
};

const theme = {
  flags: {
    flags,
    badges,
    supportive,
    tags,
  },
};

export default theme;
export const composed = composeTheme(theme);
