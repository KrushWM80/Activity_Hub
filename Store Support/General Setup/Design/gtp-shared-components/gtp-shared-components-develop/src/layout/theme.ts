import {Platform} from 'react-native';

import {colors, composeTheme} from '../next/utils';
import {getFont} from '../theme/font';
import {
  shadowLarge,
  shadowMedium,
  shadowNone,
  shadowSmall,
} from '../theme/shadow';

const divider = {
  default: {
    container: {
      paddingHorizontal: 16,
      paddingVertical: 16,
    },
    line: {
      backgroundColor: colors.gray['50'],
      height: 1,
    },
  },
  block: {
    container: {
      paddingHorizontal: 0,
    },
  },
};

const solidCard = {
  static: {
    contentInset: {
      none: {
        padding: 0,
      },
      tiny: {
        padding: 4,
      },
      small: {
        padding: 8,
      },
      normal: {
        padding: 16,
      },
    },
    roundness: {
      small: {
        borderRadius: 4,
      },
      large: {
        borderRadius: 8,
      },
    },
  },
  default: {
    container: {
      flex: 1,
      minHeight: 10,
      borderRadius: 4,
      borderWidth: 0,
      borderStyle: 'solid',
      backgroundColor: colors.white,
      ...shadowSmall,
    },
  },
  white0: {
    container: {
      ...shadowNone,
    },
  },
  white1: {},
  white2: {
    container: {
      ...shadowMedium,
    },
  },
  white3: {
    container: {
      ...shadowLarge,
    },
  },
  blue0: {
    container: {
      backgroundColor: colors.blue['100'],
      ...shadowNone,
    },
  },
  blue1: {
    container: {
      backgroundColor: colors.blue['100'],
    },
  },
  blue2: {
    container: {
      backgroundColor: colors.blue['100'],
      ...shadowMedium,
    },
  },
  blue3: {
    container: {
      backgroundColor: colors.blue['100'],
      ...shadowLarge,
    },
  },
};

const outlineCard = {
  static: solidCard.static,
  default: {
    container: {
      flex: 1,
      minHeight: 10,
      borderRadius: 4,
      borderWidth: 1,
      borderColor: colors.black,
      borderStyle: 'solid',
      backgroundColor: colors.white,
    },
  },
  black: {},
  gray: {
    container: {
      borderColor: colors.gray['50'],
    },
  },
  blue: {
    container: {
      borderColor: colors.blue['100'],
    },
  },
};

const mediaCard = {
  static: {
    ...solidCard.static,
    container: {},
    media: {
      borderBottomRightRadius: 0,
      borderBottomLeftRadius: 0,
      overflow: 'hidden',
      justifyContent: 'center',
      alignItems: 'center',
    },
  },
};

const carousel = {
  default: {
    container: {
      padding: 16,
      borderBottomWidth: 1,
      borderBottomColor: colors.gray['10'],
    },
    header: {
      marginBottom: 16,
      flexDirection: 'row',
      alignItems: 'flex-start',
    },
    headerTitleContainer: {
      flexDirection: 'column',
      flexGrow: 1,
    },
    headerTitle: {
      ...getFont('bold'),
      fontSize: 18,
      lineHeight: 24,
    },
    headerSubtitle: {
      marginTop: 4,
      fontSize: 12,
      lineHeight: 16,
      color: colors.gray['100'],
    },
    headerLink: {
      marginLeft: 24,
      lineHeight: 24,
    },
    items: {
      padding: 16,
      paddingRight: 0,
      flexDirection: 'row',
    },
    footer: {
      marginTop: 8,
      flexDirection: 'row',
      alignItems: 'center',
      justifyContent: 'flex-end',
    },
    footerCaption: {
      marginRight: 8,
      fontSize: 16,
      lineHeight: 24,
    },
    footerTotal: {
      ...getFont('bold'),
      fontSize: 16,
      lineHeight: 24,
      flexGrow: 1,
    },
    footerLink: {
      marginLeft: 24,
    },
    footerButton: {
      minWidth: 100,
      flexShrink: 1,
      marginLeft: 24,
    },
  },
  small: {},
};

const imageSize = 104;
const smallImageSize = 64;
const carouselItem = {
  default: {
    container: {
      backgroundColor: 'white',
      marginRight: 16,
      flex: 1,
      width: 147,
      justifyContent: 'flex-start',
      alignItems: 'flex-start',
    },
    flag: {
      height: 26,
      justifyContent: 'center',
      marginBottom: 4,
    },
    imageSize,
    imageContainer: {
      height: imageSize,
      justifyContent: 'center',
      marginBottom: 16,
    },
    image: {},
    addButton: {
      position: 'absolute',
      top: 0,
      left: 88,
    },
    price: {
      ...getFont('bold'),
      fontSize: 16,
      lineHeight: 24,
    },
    wasPrice: {
      textDecorationLine: 'line-through',
      textDecorationStyle: 'solid',
      fontSize: 12,
      lineHeight: 32,
      color: colors.gray['100'],
    },
    eachPrice: {
      fontSize: 12,
      lineHeight: 24,
      color: colors.gray['100'],
    },
    weightLabel: {
      fontSize: 12,
      lineHeight: 16,
      color: colors.gray['100'],
    },
    name: {
      marginVertical: 4,
      fontSize: 14,
      lineHeight: 20,
      color: colors.gray['140'],
    },
    ratings: {},
    stock: {
      marginVertical: 8,
    },
    badge: {
      marginVertical: 4,
    },
    linkContainer: {
      marginTop: 16,
    },
  },
  small: {
    container: {
      width: 93,
    },
    imageSize: smallImageSize,
    imageContainer: {
      height: smallImageSize,
      marginBottom: 8,
    },
    addButton: {
      top: -16,
      left: 48,
    },
    price: {
      fontSize: 18,
      lineHeight: 24,
    },
    name: {
      fontSize: 12,
      lineHeight: 16,
    },
  },
};

const overlay = {
  default: {
    container: {
      position: 'absolute',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      flexDirection: 'row',
    },
    content: {
      flex: 1,
      alignSelf: 'flex-end',
    },
    closer: {
      position: 'absolute',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
    },
  },
  darken: {
    container: {
      ...Platform.select({
        ios: {
          backgroundColor: 'rgba(0,0,0,.25)',
        },
        android: {
          backgroundColor: colors.gray['10'],
        },
      }),
    },
  },
  darkenModal: {
    container: {
      backgroundColor: 'rgba(0,0,0,.25)',
    },
  },
};

const spinnerOverlay = {
  default: {
    container: {
      position: 'absolute',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      flexDirection: 'row',
      alignItems: 'center',
    },
    content: {
      flex: 1,
      alignSelf: 'center',
      alignItems: 'center',
    },
  },
  darken: {
    container: {
      backgroundColor: 'rgba(0,0,0,.25)',
    },
  },
};

const cardOverlay = {
  default: {
    container: {
      position: 'absolute',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      flexDirection: 'row',
      alignItems: 'center',
    },
    content: {
      margin: 16,
      flex: 1,
      alignSelf: 'center',
      verticalAlign: 'center',
    },
  },
  darken: {
    container: {
      backgroundColor: 'rgba(0,0,0,.25)',
    },
  },
};

const collapse = {
  default: {
    divider: {
      paddingVertical: 0,
    },
    dividerColor: colors.gray['10'],
    touchable: {
      padding: 16,
      flexDirection: 'row',
    },
    icon: {
      marginRight: 16,
    },
    textContainer: {
      flex: 1,
    },
    title: {
      ...getFont('bold'),
      fontSize: 16,
      lineHeight: 24,
    },
    subtitle: {
      ...getFont(),
      fontSize: 14,
      lineHeight: 20,
      marginTop: 4,
    },
    chevron: {
      marginLeft: 16,
    },
    details: {
      padding: 16,
      paddingTop: 0,
    },
  },
  simple: {
    container: {
      marginTop: 16,
    },
    touchable: {
      justifyContent: 'center',
    },
    textContainer: {
      flex: -1,
    },
    chevron: {
      marginLeft: 8,
    },
    details: {
      paddingTop: 16,
      paddingBottom: 0,
    },
  },
};

const bottomSheet = {
  static: {
    contentPadding: 0,
    animationDuration: 200,
  },
  default: {
    wrapper: {
      position: 'absolute',
      top: -10,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(0, 0, 0, .6)',
    },
    top: {
      minHeight: 18,
      flex: 1,
    },
    dismissArea: {
      flex: 1,
    },
    safeArea: {
      flex: 1,
    },
    safeAreaBackground: {
      backgroundColor: colors.white,
    },
    title: {
      textAlign: 'center',
      marginTop: -8,
      marginBottom: 8,
      paddingBottom: 8,
      fontSize: 18,
      lineHeight: 24,
    },
    closeButton: {
      position: 'absolute',
      top: 4,
      right: 4,
      zIndex: 1,
    },
    backButton: {
      position: 'absolute',
      top: 4,
      left: 4,
      zIndex: 1,
    },
    keyboardContainer: {
      borderTopLeftRadius: 16,
      borderTopRightRadius: 16,
      backgroundColor: colors.white,
    },
    contentContainer: {
      backgroundColor: colors.white,
      padding: 16,
      paddingTop: 0,
      paddingBottom: 0,
      borderTopLeftRadius: 16,
      borderTopRightRadius: 16,
    },
    content: {
      flexGrow: 1,
    },
    contentInner: {
      flexShrink: 1,
      paddingBottom: 16,
    },
    scrollableArea: {
      flexDirection: 'column',
      flex: 1,
    },
    divider: {},
    grip: {
      backgroundColor: colors.white,
      paddingTop: 8,
      paddingBottom: 16,
    },
    nonGrip: {
      backgroundColor: colors.white,
      paddingTop: 16,
      paddingBottom: 16,
      marginBottom: -12,
    },
    gripIndicator: {
      alignSelf: 'center',
      height: 4,
      width: 32,
      backgroundColor: colors.gray['30'],
      borderRadius: 4,
    },
  },
  active: {
    gripIndicator: {
      backgroundColor: colors.gray['100'],
    },
  },
};

const skeleton = {
  default: {
    height: 16,
    colorFrom: colors.gray[5],
    colorTo: colors.gray[20],
    container: {},
    item: {
      borderRadius: 4,
    },
  },
  lines: {
    height: 16,
    colorFrom: colors.gray[5],
    colorTo: colors.gray[20],
    container: {
      paddingVertical: 4,
    },
    item: {
      marginVertical: 4,
    },
  },
};

const list = {
  default: {
    container: {},
  },
};

const listItem = {
  default: {
    container: {
      paddingHorizontal: 16,
    },
    contentContainer: {
      flexDirection: 'row',
    },
    leading: {
      paddingRight: 16,
    },
    itemContent: {
      flex: 1,
    },
    title: {
      ...getFont('bold'),
      fontSize: 16,
      lineHeight: 24,
    },
    content: {
      ...getFont(),
      fontSize: 16,
      lineHeight: 24,
    },
    trailing: {
      paddingLeft: 16,
    },
    bottomBorder: {
      flex: 1,
      marginVertical: 8,
      paddingTop: 1,
      backgroundColor: colors.gray[10],
    },
  },
};

const theme = {
  layout: {
    divider,
    solidCard,
    outlineCard,
    mediaCard,
    carousel,
    carouselItem,
    overlay,
    spinnerOverlay,
    cardOverlay,
    collapse,
    bottomSheet,
    skeleton,
    list,
    listItem,
  },
};

export default theme;
export const composed = composeTheme(theme);
