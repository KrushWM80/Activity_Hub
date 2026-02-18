import {Platform} from 'react-native';

import {
  componentButtonContainerAlignHorizontal,
  componentButtonContainerAlignVertical,
  componentButtonContainerBorderRadius,
  componentButtonContainerSizeLargeFontSize,
  componentButtonContainerSizeLargeLineHeight,
  componentButtonContainerSizeLargePaddingHorizontal,
  componentButtonContainerSizeLargePaddingVertical,
  componentButtonContainerSizeMediumFontSize,
  componentButtonContainerSizeMediumLineHeight,
  componentButtonContainerSizeMediumPaddingHorizontal,
  componentButtonContainerSizeMediumPaddingVertical,
  componentButtonContainerSizeSmallFontSize,
  componentButtonContainerSizeSmallLineHeight,
  componentButtonContainerSizeSmallPaddingHorizontal,
  componentButtonContainerSizeSmallPaddingVertical,
  componentButtonContainerVariantDestructiveBackgroundColorDefault,
  componentButtonContainerVariantDestructiveBackgroundColorDisabled,
  componentButtonContainerVariantDestructiveFontWeight,
  componentButtonContainerVariantDestructiveTextColorDefault,
  componentButtonContainerVariantDestructiveTextColorDisabled,
  componentButtonContainerVariantPrimaryBackgroundColorDefault,
  componentButtonContainerVariantPrimaryBackgroundColorDisabled,
  componentButtonContainerVariantPrimaryFontWeight,
  componentButtonContainerVariantPrimaryTextColorDefault,
  componentButtonContainerVariantSecondaryBackgroundColorDefault,
  componentButtonContainerVariantSecondaryBackgroundColorDisabled,
  componentButtonContainerVariantSecondaryFontWeight,
  componentButtonContainerVariantSecondaryTextColorDefault,
  componentButtonContainerVariantSecondaryTextColorDisabled,
  componentButtonContainerVariantTertiaryBackgroundColor,
  componentButtonContainerVariantTertiaryFontWeight,
  componentButtonContainerVariantTertiaryTextColorDefault,
  componentButtonContainerVariantTertiaryTextColorDisabled,
  componentButtonContainerVariantTertiaryTextDecorationDefault,
} from '@livingdesign/tokens/dist/react-native/light/regular/components/Button';

import {colors, composeTheme, deepMerge} from '../next/utils';
import {getFont} from '../theme/font';

const button = {
  face: {
    borderWidth: 1,
    borderStyle: 'solid',
    borderRadius: componentButtonContainerBorderRadius,
    paddingHorizontal: 23,
    alignItems: componentButtonContainerAlignVertical,
    justifyContent: componentButtonContainerAlignHorizontal,
  },
  text: {
    ...getFont('bold'),
    fontSize: 16,
    textAlign: 'center',
    lineHeight: 38,
  },
  image: {},
  spinnerContainer: {
    position: 'absolute',
    alignItems: 'center',
    width: '100%',
    left: 23,
    marginVertical: 7,
  },
  spinner: {},
};

const small = deepMerge(button, {
  face: {
    paddingHorizontal: componentButtonContainerSizeSmallPaddingHorizontal,
    paddingVertical: componentButtonContainerSizeSmallPaddingVertical,
  },
  text: {
    fontSize: componentButtonContainerSizeSmallFontSize,
    lineHeight: componentButtonContainerSizeSmallLineHeight,
  },
  spinnerContainer: {
    left: 15,
    marginVertical: 3,
  },
});

const medium = deepMerge(button, {
  face: {
    paddingHorizontal: componentButtonContainerSizeMediumPaddingHorizontal,
    paddingVertical: componentButtonContainerSizeMediumPaddingVertical,
  },
  text: {
    fontSize: componentButtonContainerSizeMediumFontSize,
    lineHeight: componentButtonContainerSizeMediumLineHeight,
  },
  spinnerContainer: {
    left: 15,
    marginVertical: 3,
  },
});

const large = deepMerge(button, {
  face: {
    paddingHorizontal: componentButtonContainerSizeLargePaddingHorizontal,
    paddingVertical: componentButtonContainerSizeLargePaddingVertical,
  },
  text: {
    fontSize: componentButtonContainerSizeLargeFontSize,
    lineHeight: componentButtonContainerSizeLargeLineHeight,
  },
  spinnerContainer: {
    left: 15,
    marginVertical: 3,
  },
});

const primary = {
  default: deepMerge(button, {
    face: {
      borderColor: colors.blue['100'],
      backgroundColor:
        componentButtonContainerVariantPrimaryBackgroundColorDefault,
    },
    text: {
      color: componentButtonContainerVariantPrimaryTextColorDefault,
      ...Platform.select({
        android: {
          ...getFont('bold'),
        },
        ios: {
          fontWeight:
            componentButtonContainerVariantPrimaryFontWeight.toString(),
        },
      }),
    },
    image: {
      tintColor: colors.white,
    },
    spinner: {
      color: colors.white,
    },
  }),
  pressed: {
    face: {
      borderColor: colors.blue['160'],
      backgroundColor: colors.blue['160'],
    },
  },
  disabled: {
    face: {
      borderColor: colors.gray['50'],
      backgroundColor:
        componentButtonContainerVariantPrimaryBackgroundColorDisabled,
    },
  },
};

const destructive = {
  default: deepMerge(button, {
    face: {
      borderColor: colors.red['100'],
      backgroundColor:
        componentButtonContainerVariantDestructiveBackgroundColorDefault,
    },
    text: {
      color: componentButtonContainerVariantDestructiveTextColorDefault,
      ...Platform.select({
        android: {
          ...getFont('bold'),
        },
        ios: {
          fontWeight:
            componentButtonContainerVariantDestructiveFontWeight.toString(),
        },
      }),
    },
    image: {
      tintColor: colors.white,
    },
    spinner: {
      color: colors.white,
    },
  }),
  pressed: {
    face: {
      borderColor: colors.red['160'],
      backgroundColor: colors.red['160'],
    },
  },
  disabled: {
    face: {
      borderColor: colors.gray['50'],
      backgroundColor:
        componentButtonContainerVariantDestructiveBackgroundColorDisabled,
    },
    text: {
      color: componentButtonContainerVariantDestructiveTextColorDisabled,
    },
  },
};

const icon = deepMerge(primary, {
  default: {
    face: {
      paddingHorizontal: 6,
      paddingVertical: 6,
    },
    text: {
      height: 0,
      lineHeight: 0,
    },
  },
});

const secondary = {
  default: deepMerge(button, {
    face: {
      borderColor: colors.black,
      backgroundColor:
        componentButtonContainerVariantSecondaryBackgroundColorDefault,
    },
    text: {
      color: componentButtonContainerVariantSecondaryTextColorDefault,
      ...Platform.select({
        android: {
          ...getFont('bold'),
        },
        ios: {
          fontWeight:
            componentButtonContainerVariantSecondaryFontWeight.toString(),
        },
      }),
    },
    image: {
      tintColor: colors.black,
    },
    spinner: {
      color: colors.gray['100'],
    },
  }),
  pressed: {
    face: {
      backgroundColor: colors.gray['20'],
      borderColor: colors.gray['50'],
    },
    text: {
      color: colors.gray['110'],
    },
    image: {
      tintColor: colors.gray['110'],
    },
  },
  disabled: {
    face: {
      borderColor: colors.gray['50'],
      backgroundColor:
        componentButtonContainerVariantSecondaryBackgroundColorDisabled,
    },
    text: {
      color: componentButtonContainerVariantSecondaryTextColorDisabled,
    },
    image: {
      tintColor: colors.gray['50'],
    },
    spinner: {
      color: colors.gray['50'],
    },
  },
};

const transparent = {
  default: deepMerge(button, {
    face: {
      borderColor: colors.black,
      backgroundColor: 'transparent',
    },
    text: {
      color: componentButtonContainerVariantSecondaryTextColorDefault,
      fontWeight: componentButtonContainerVariantSecondaryFontWeight.toString(),
    },
    image: {
      tintColor: colors.black,
    },
    spinner: {
      color: colors.gray['100'],
    },
  }),
  pressed: {
    face: {
      backgroundColor: colors.gray['20'],
      borderColor: colors.gray['50'],
    },
    text: {
      color: colors.gray['110'],
    },
    image: {
      tintColor: colors.gray['110'],
    },
  },
  disabled: {
    face: {
      borderColor: colors.gray['50'],
      backgroundColor: 'transparent',
    },
    text: {
      color: componentButtonContainerVariantSecondaryTextColorDisabled,
    },
    image: {
      tintColor: colors.gray['50'],
    },
    spinner: {
      color: colors.gray['50'],
    },
  },
};

const transparentIcon = deepMerge(icon, {
  default: {
    face: {
      borderColor: 'transparent',
      backgroundColor: `${colors.gray['20']}00`,
    },
    text: {
      color: colors.black,
    },
    image: {
      tintColor: colors.black,
    },
    spinner: {
      color: colors.gray['100'],
    },
  },
  pressed: {
    face: {
      backgroundColor: colors.gray['20'],
      borderColor: 'transparent',
    },
    text: {
      color: colors.gray['110'],
    },
    image: {
      tintColor: colors.gray['110'],
    },
  },
  disabled: {
    face: {
      borderColor: 'transparent',
    },
    text: {
      color: colors.gray['50'],
    },
    image: {
      tintColor: colors.gray['50'],
    },
    spinner: {
      color: colors.gray['50'],
    },
  },
});

const povPrimary = {
  default: deepMerge(button, {
    face: {
      borderColor: colors.white,
      backgroundColor: colors.white,
    },
    text: {
      color: colors.blue['100'],
    },
    image: {
      tintColor: colors.blue['100'],
    },
    spinner: {
      color: colors.blue['100'],
    },
  }),
  pressed: {
    face: {
      backgroundColor: `${colors.white}00`,
    },
    text: {
      color: colors.white,
    },
    spinner: {
      color: colors.white,
    },
  },
  disabled: {
    face: {
      borderColor: colors.blue['160'],
      backgroundColor: colors.blue['160'],
    },
  },
};

const povSecondary = {
  default: deepMerge(button, {
    face: {
      borderColor: colors.white,
      backgroundColor: `${colors.gray['20']}00`,
    },
    text: {
      color: colors.white,
    },
    image: {
      tintColor: colors.white,
    },
  }),
  pressed: {
    face: {
      backgroundColor: colors.gray['20'],
      borderColor: colors.gray['50'],
    },
    text: {
      color: colors.gray['110'],
    },
    image: {
      tintColor: colors.gray['110'],
    },
  },
  disabled: {
    face: {
      borderColor: colors.blue['160'],
    },
    text: {
      color: colors.blue['160'],
    },
    image: {
      tintColor: colors.blue['160'],
    },
    spinner: {
      color: colors.blue['160'],
    },
  },
};

const banner = {
  default: deepMerge(button, {
    face: {
      borderColor: colors.blue['100'],
      backgroundColor: colors.blue['100'],
      borderRadius: 4,
      paddingHorizontal: 15,
      paddingVertical: 15,
    },
    text: {
      color: colors.white,
      textAlign: 'left',
      marginLeft: 16,
      height: 'auto',
      lineHeight: 0,
    },
    title: {
      ...getFont('bold'),
      fontSize: 20,
      lineHeight: 28,
    },
    description: {
      ...getFont(),
      fontSize: 14,
      lineHeight: 20,
    },
    image: {
      tintColor: colors.white,
    },
  }),
  pressed: {
    face: {
      borderColor: colors.blue['160'],
      backgroundColor: colors.blue['160'],
    },
  },
  disabled: {
    face: {
      borderColor: colors.gray['50'],
      backgroundColor: colors.gray['50'],
    },
  },
};

const link = {
  default: {
    face: {},
    text: {
      ...getFont(),
      fontSize: 16,
      lineHeight: 24,
      textAlign: 'center',
      color: colors.black,
      textDecorationLine: 'underline',
    },
    image: {},
    spinner: {},
  },
  pressed: {
    text: {
      color: colors.gray['110'],
    },
  },
  disabled: {
    text: {
      color: colors.gray['40'],
    },
  },
};

const linkSmall = deepMerge(link, {
  default: {
    text: {
      fontSize: 14,
      lineHeight: 20,
    },
  },
});

const linkWhite = deepMerge(link, {
  default: {
    face: {},
    text: {
      color: colors.white,
    },
    image: {},
  },
  pressed: {
    text: {
      color: colors.gray['70'],
    },
  },
  disabled: {
    text: {
      color: colors.gray['50'],
    },
  },
});

const linkWhiteSmall = deepMerge(linkWhite, {
  default: {
    text: {
      fontSize: 14,
      lineHeight: 20,
    },
  },
});

const tertiary = {
  default: {
    face: {
      backgroundColor: componentButtonContainerVariantTertiaryBackgroundColor,
    },
    text: {
      ...getFont(),
      fontSize: 16,
      lineHeight: 24,
      textAlign: 'center',
      color: componentButtonContainerVariantTertiaryTextColorDefault,
      textDecorationLine:
        componentButtonContainerVariantTertiaryTextDecorationDefault,
      ...Platform.select({
        ios: {
          fontWeight:
            componentButtonContainerVariantTertiaryFontWeight.toString(),
        },
      }),
    },
    image: {},
    spinner: {},
  },
  pressed: {
    text: {
      color: colors.gray['110'],
    },
  },
  disabled: {
    text: {
      color: componentButtonContainerVariantTertiaryTextColorDisabled,
    },
  },
};

const tertiarySmall = deepMerge(tertiary, {
  default: {
    text: {
      fontSize: componentButtonContainerSizeSmallFontSize,
      lineHeight: componentButtonContainerSizeSmallLineHeight,
    },
  },
});

const tertiaryMedium = deepMerge(tertiary, {
  default: {
    text: {
      fontSize: componentButtonContainerSizeMediumFontSize,
      lineHeight: componentButtonContainerSizeMediumLineHeight,
    },
  },
});

const tertiaryLarge = deepMerge(tertiary, {
  default: {
    text: {
      fontSize: componentButtonContainerSizeLargeFontSize,
      lineHeight: componentButtonContainerSizeLargeLineHeight,
    },
  },
});

const theme = {
  buttons: {
    primarySmall: deepMerge(primary, {default: small}),
    primaryMedium: deepMerge(primary, {default: medium}),
    primaryLarge: deepMerge(primary, {default: large}),
    destructiveSmall: deepMerge(destructive, {default: small}),
    destructiveMedium: deepMerge(destructive, {default: medium}),
    destructiveLarge: deepMerge(destructive, {default: large}),
    secondarySmall: deepMerge(secondary, {default: small}),
    secondaryMedium: deepMerge(secondary, {default: medium}),
    secondaryLarge: deepMerge(secondary, {default: large}),
    tertiarySmall,
    tertiaryMedium,
    tertiaryLarge,
    transparentSmall: deepMerge(transparent, {default: small}),
    transparentMedium: deepMerge(transparent, {default: medium}),
    transparentLarge: deepMerge(transparent, {default: large}),
    povPrimary,
    povPrimarySmall: deepMerge(povPrimary, {default: small}),
    povSecondary,
    povSecondarySmall: deepMerge(povSecondary, {default: small}),
    icon,
    transparentIcon,
    banner,
    link,
    linkSmall,
    linkWhite,
    linkWhiteSmall,
  },
};

export default theme;
export const composed = composeTheme(theme);
