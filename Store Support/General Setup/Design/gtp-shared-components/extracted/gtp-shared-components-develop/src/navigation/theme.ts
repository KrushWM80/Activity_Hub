import {colors, composeTheme} from '../next/utils';
import {getFont} from '../theme/font';

const tab = {
  default: {
    container: {
      paddingTop: 13,
      paddingBottom: 13,
      paddingHorizontal: 16,
      textAlign: 'center',
      backgroundColor: colors.white,
      borderColor: colors.gray['10'],
      borderStyle: 'solid',
      borderBottomWidth: 1,
    },
    text: {
      ...getFont(),
      fontSize: 15,
      lineHeight: 20,
      alignSelf: 'center',
    },
    indicator: {
      borderWidth: 0,
      borderStyle: 'solid',
      position: 'absolute',
      height: 3,
      bottom: 0,
      left: 4,
      right: 4,
      backgroundColor: 'transparent',
      borderTopLeftRadius: 9999,
      borderTopRightRadius: 9999,
    },
  },
  selected: {
    container: {},
    indicator: {
      backgroundColor: colors.blue[100],
    },
    text: {
      ...getFont('bold'),
    },
  },
};

const tabs = {
  static: {
    container: {
      flex: 1,
      flexDirection: 'row',
    },
  },
};
const theme = {
  navigation: {
    tabs,
    tab,
  },
};

export default theme;
export const composed = composeTheme(theme);
