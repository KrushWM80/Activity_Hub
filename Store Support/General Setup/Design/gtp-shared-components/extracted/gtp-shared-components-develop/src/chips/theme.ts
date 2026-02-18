import {colors, composeTheme, deepMerge} from '../next/utils';
import {getFont} from '../theme/font';

const single = {
  static: {
    container: {
      paddingVertical: 8,
      paddingHorizontal: 12,
      flexDirection: 'row',
    },
  },
  default: {
    face: {
      borderWidth: 1,
      borderRadius: 4,
      backgroundColor: colors.white,
      borderColor: colors.gray['50'],
      borderStyle: 'solid',
      marginVertical: 8,
      marginHorizontal: 4,
      paddingVertical: 6,
      paddingHorizontal: 16,
      alignItems: 'center',
    },
    text: {
      ...getFont(),
      fontSize: 14,
      lineHeight: 20,
      color: colors.black,
    },
    image: {},
    spinnerContainer: {
      position: 'absolute',
      alignItems: 'center',
      width: '100%',
      left: 23,
      marginVertical: 7,
    },
    spinner: {
      color: colors.white,
    },
  },
  disabled: {
    face: {
      backgroundColor: colors.gray['10'],
      borderColor: 'transparent',
    },
    text: {
      color: colors.gray['50'],
    },
    image: {},
  },
  pressed: {
    face: {
      backgroundColor: colors.gray['10'],
    },
    text: {},
    image: {},
  },
  selected: {
    face: {
      borderColor: colors.black,
    },
    text: {
      ...getFont('bold'),
      fontSize: 14,
      lineHeight: 20,
      color: colors.black,
    },
    image: {},
  },
  selectedpressed: {
    face: {
      borderColor: colors.black,
      backgroundColor: colors.gray['10'],
    },
    text: {
      ...getFont('bold'),
      fontSize: 14,
      lineHeight: 20,
      color: colors.black,
    },
    image: {},
  },
};

const multiple = {
  static: {
    container: {
      justifyContent: 'center',
      flexWrap: 'wrap',
    },
  },
};

const singlemedium = single;
const multiplemedium = deepMerge(single, multiple);
const singlelarge = deepMerge(single, {
  default: {
    face: {
      paddingHorizontal: 8,
      paddingVertical: 10,
    },
  },
});
const multiplelarge = deepMerge(singlelarge, multiple);
const singlexlarge = deepMerge(single, {
  default: {
    face: {
      paddingHorizontal: 8,
      paddingVertical: 14,
    },
  },
});
const multiplexlarge = deepMerge(singlexlarge, multiple);

const theme = {
  chips: {
    singlemedium,
    multiplemedium,
    singlelarge,
    multiplelarge,
    singlexlarge,
    multiplexlarge,
  },
};
export default theme;
export const composed = composeTheme(theme);
