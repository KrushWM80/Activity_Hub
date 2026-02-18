import {colors, composeTheme} from '../next/utils';
import {getFont} from '../theme/font';
import {shadowLarge} from '../theme/shadow';

const alert = {
  default: {
    container: {
      backgroundColor: colors.gray['20'],
      paddingLeft: 16,
      paddingRight: 0,
      flexDirection: 'row',
      alignItems: 'flex-start',
    },
    text: {
      marginVertical: 8,
      flex: 1,
      lineHeight: 20,
      color: colors.black,
    },
    icon: {
      marginLeft: -8,
      marginRight: 8,
      marginVertical: 9,
      tintColor: colors.black,
    },
    closeContainer: {
      borderRadius: 9999,
      marginVertical: 5,
      marginHorizontal: 4,
      paddingVertical: 4,
      paddingHorizontal: 4,
    },
    underlayColor: colors.gray['5'],
    close: {
      tintColor: colors.black,
    },
  },
  info: {
    container: {
      backgroundColor: colors.orange['120'],
    },
    text: {
      color: colors.white,
    },
    icon: {
      tintColor: colors.white,
    },
    close: {
      tintColor: colors.white,
    },
    underlayColor: colors.orange['140'],
  },
  info2: {
    container: {
      backgroundColor: colors.pink['120'],
    },
    text: {
      color: colors.white,
    },
    icon: {
      tintColor: colors.white,
    },
    close: {
      tintColor: colors.white,
    },
    underlayColor: colors.pink['140'],
  },
  info3: {
    container: {
      backgroundColor: colors.purple['110'],
    },
    text: {
      color: colors.white,
    },
    icon: {
      tintColor: colors.white,
    },
    close: {
      tintColor: colors.white,
    },
    underlayColor: colors.purple['130'],
  },
  error: {
    container: {
      backgroundColor: colors.red['120'],
    },
    text: {
      color: colors.white,
    },
    icon: {
      tintColor: colors.white,
    },
    close: {
      tintColor: colors.white,
    },
    underlayColor: colors.red['140'],
  },
};

const message = {
  default: {
    container: {
      borderRadius: 4,
      borderWidth: 0,
      borderLeftWidth: 5,
      borderColor: colors.black,
      borderStyle: 'solid',
    },
    containerInner: {
      flexDirection: 'row',
      borderTopRightRadius: 4,
      borderBottomRightRadius: 4,
      borderWidth: 1,
      borderLeftWidth: 0,
      paddingLeft: 12,
      paddingRight: 16,
      paddingVertical: 8,
      borderColor: colors.gray['50'],
      borderStyle: 'solid',
      backgroundColor: colors.gray['10'],
    },
    text: {
      flex: 1,
      lineHeight: 20,
      color: colors.black,
      alignSelf: 'center',
    },
    icon: {
      tintColor: colors.black,
      marginRight: 9,
      marginVertical: 1,
    },
  },
  error: {
    container: {
      borderColor: colors.red['100'],
    },
    containerInner: {
      backgroundColor: colors.red['10'],
      borderColor: colors.red['50'],
    },
    text: {
      color: colors.red['110'],
    },
    icon: {
      tintColor: colors.red['110'],
    },
  },
  warning: {
    container: {
      borderColor: colors.spark['100'],
    },
    containerInner: {
      backgroundColor: colors.spark['10'],
      borderColor: colors.spark['50'],
    },
    text: {
      color: colors.spark['160'],
    },
    icon: {
      tintColor: colors.spark['160'],
    },
  },
  info: {},
  success: {
    container: {
      borderColor: colors.green['100'],
    },
    containerInner: {
      backgroundColor: colors.green['10'],
      borderColor: colors.green['50'],
    },
    text: {
      color: colors.green['130'],
    },
    icon: {
      tintColor: colors.green['130'],
    },
  },
};

const snackbar = {
  static: {
    container: {
      backgroundColor: colors.gray['160'],
      margin: 16,
      flexDirection: 'row',
      borderRadius: 4,
      ...shadowLarge,
    },
    text: {
      fontSize: 14,
      padding: 16,
      color: colors.white,
      flex: 1,
    },
    button: {
      padding: 16,
      paddingLeft: 8,
      flexShrink: 1,
      maxWidth: 120,
    },
    hitSlop: {
      left: 16,
      top: 16,
      right: 16,
      bottom: 16,
    },
  },
};

const tooltip = {
  static: {
    container: {
      alignSelf: 'flex-start',
      backgroundColor: colors.yellow['100'],
      flexDirection: 'column',
      borderRadius: 4,
      padding: 8,
      position: 'relative',
      ...shadowLarge,
    },
    containerTop: {
      marginTop: 8,
    },
    containerLeft: {
      marginLeft: 8,
    },
    containerRight: {
      marginRight: 8,
    },
    containerBottom: {
      marginBottom: 8,
    },
    arrow: {
      position: 'absolute',
      borderWidth: 8,
      borderStyle: 'solid',
      borderColor: 'transparent',
    },
    top: {
      alignSelf: 'center',
      top: -8,
      borderTopWidth: 0,
      borderBottomColor: colors.yellow['100'],
    },
    topLeft: {
      left: 16,
      top: -8,
      borderTopWidth: 0,
      borderBottomColor: colors.yellow['100'],
    },
    topRight: {
      right: 16,
      top: -8,
      borderTopWidth: 0,
      borderBottomColor: colors.yellow['100'],
    },
    right: {
      top: '50%',
      right: -8,
      borderRightWidth: 0,
      borderLeftColor: colors.yellow['100'],
    },
    bottom: {
      alignSelf: 'center',
      marginLeft: 8,
      bottom: -8,
      borderBottomWidth: 0,
      borderTopColor: colors.yellow['100'],
    },
    bottomLeft: {
      left: 16,
      bottom: -8,
      borderBottomWidth: 0,
      borderTopColor: colors.yellow['100'],
    },
    bottomRight: {
      right: 16,
      bottom: -8,
      borderBottomWidth: 0,
      borderTopColor: colors.yellow['100'],
    },
    left: {
      top: '50%',
      left: -8,
      borderLeftWidth: 0,
      borderRightColor: colors.yellow['100'],
    },
  },
  default: {
    textContainer: {
      flexDirection: 'row',
    },
    text: {
      ...getFont('bold'),
      padding: 8,
      minWidth: 42 + 16,
      maxWidth: 263 + 16,
      fontSize: 14,
      lineHeight: 20,
      textAlign: 'center',
    },
    iconContainer: {
      borderRadius: 9999,
      display: 'none',
      padding: 4,
    },
    icon: {},
  },
  removable: {
    text: {
      minWidth: 30,
      maxWidth: 243,
    },
    iconContainer: {
      display: 'flex',
      alignSelf: 'flex-start',
    },
  },
  underlayColor: 'rgba(255, 255, 255, 0.5)',
};

const theme = {
  messaging: {
    alert,
    message,
    snackbar,
    tooltip,
  },
};

export default theme;
export const composed = composeTheme(theme);
