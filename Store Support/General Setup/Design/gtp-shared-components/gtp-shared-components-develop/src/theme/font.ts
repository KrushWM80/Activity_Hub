import {Platform} from 'react-native';

import {isObject} from '../next/utils';
import {capitalize, findKey} from '../next/utils';

type FontWeightValue = '100' | '300' | '400' | '500' | '700' | '900';
type FontWeightAlias =
  | 'thin'
  | 'light'
  | 'normal'
  | 'medium'
  | 'bold'
  | 'black';

type WeightMap = Record<FontWeightAlias, FontWeightValue>;
const weightMap: WeightMap = {
  thin: '100',
  light: '300',
  normal: '400',
  medium: '500',
  bold: '700',
  black: '900',
};

const weights = [
  '100',
  '300',
  '400',
  '500',
  '700',
  '900',
  'thin',
  'light',
  'normal',
  'medium',
  'bold',
  'black',
] as const;

export type Weights = FontWeightValue | FontWeightAlias;
export type WeightStrings = Weights; // for backwards compatibility
export type Weight = (typeof weights)[number];
const isValidWeight = (w: any): w is Weight => weights.includes(w);
const isWeightValue = (w: any): w is FontWeightValue =>
  isValidWeight(w) && !!parseInt(w.charAt(0), 10);

export type FontFamily =
  // iOS
  | 'Bogle'
  | 'Bogle Mono'
  // Android
  | 'Bogle-Regular'
  | 'Bogle-Bold'
  | 'Bogle-Black'
  | 'BogleMono-Regular'
  | 'BogleMono-Bold'
  | 'BogleMono-Black';

export type FontDetails = {
  fontFamily?: FontFamily;
  fontWeight?: FontWeightValue;
  fontStyle?: string;
  fontSize: number;
  lineHeight: number;
};

const getFont = (
  weight: Weights = 'normal',
  isMonospace: boolean = false,
  platformOS = Platform.OS,
): Partial<FontDetails> | undefined => {
  if (!isValidWeight(weight)) {
    return undefined;
  }

  const fontFamilyIOS = `Bogle${isMonospace ? ' Mono' : ''}` as FontFamily;
  const fontFamilyAndroid = `Bogle${isMonospace ? 'Mono' : ''}` as FontFamily;
  let fontWeight;
  let fontVariant = 'Regular';

  if (isWeightValue(weight)) {
    fontWeight = weight;
  } else {
    fontWeight = weightMap[weight];
  }

  if (['400', 'normal'].includes(weight)) {
    fontVariant = 'Regular';
  } else if (['700', 'bold'].includes(weight)) {
    fontVariant = 'Bold';
  } else if (['900', 'black'].includes(weight)) {
    if (isMonospace) {
      fontVariant = 'Bold';
    } else {
      fontVariant = 'Black';
    }
  } else if (isWeightValue(weight)) {
    if (!isMonospace) {
      fontVariant = capitalize(findKey(weightMap, weight) as string);
    }
  } else {
    if (!isMonospace) {
      fontVariant = capitalize(weight);
    }
  }

  return platformOS === 'android'
    ? {
        fontFamily: `${fontFamilyAndroid}-${fontVariant}` as FontFamily,
      }
    : {
        fontFamily: fontFamilyIOS,
        fontWeight,
        fontStyle: 'normal', // hardcoded b/c LD3 is not supporting italics anymore (see: CEEMP-2583)
      };
};

const extractKeys = (keys: Array<string>, data: any): any => {
  const datum: Record<string, any> = {...data};
  const newKeys: Record<string, any> = {};
  keys.forEach((key) => {
    newKeys[key] = datum[key] || newKeys[key];
    delete datum[key];
  });
  return {
    ...newKeys,
    data: {...datum},
  };
};

const splitStyleData = (style: any) => {
  if (!isObject(style)) {
    return {style};
  }
  const {fontWeight, fontStyle, data} = extractKeys(
    ['fontWeight', 'fontStyle'],
    style,
  );
  return {
    fontWeight,
    fontStyle,
    style: data,
  };
};

const reduceStyleData = (result: any, style: any) => {
  if (Array.isArray(style)) {
    return style.reduce(reduceStyleData, result);
  }
  if (isObject(style)) {
    const splitStyle = splitStyleData(style);
    return {
      fontWeight: splitStyle.fontWeight || result.fontWeight,
      fontStyle: splitStyle.fontStyle || result.fontStyle,
      style: (result.style || []).concat(splitStyle.style),
    };
  }
  return {
    fontWeight: result.fontWeight,
    fontStyle: result.fontStyle,
    style: (result.style || []).concat(style),
  };
};

const extractInvalidStyleData = (...styles: Array<any>) => {
  if (!styles.length) {
    return {
      fontWeight: undefined,
      fontStyle: undefined,
      style: undefined,
    };
  }
  return styles.reduce(reduceStyleData, {
    fontWeight: undefined,
    fontStyle: undefined,
    style: undefined,
  });
};

type FontTheme = {
  [key: string]: {
    [key: string]: FontDetails;
  };
};

const font: FontTheme = {
  price: {
    small: {
      ...getFont('bold'),
      fontSize: 16,
      lineHeight: 20,
    },
    medium: {
      ...getFont('bold'),
      fontSize: 18,
      lineHeight: 24,
    },
    large: {
      ...getFont('bold'),
      fontSize: 24,
      lineHeight: 32,
    },
  },
  text: {
    display: {
      ...getFont('bold'),
      fontSize: 28,
      lineHeight: 40,
    },
    display2: {
      ...getFont('bold'),
      fontSize: 24,
      lineHeight: 36,
    },
    headline: {
      ...getFont('bold'),
      fontSize: 18,
      lineHeight: 24,
    },
    title: {
      ...getFont('bold'),
      fontSize: 20,
      lineHeight: 28,
    },
    title2: {
      ...getFont(),
      fontSize: 18,
      lineHeight: 24,
    },
    title3: {
      ...getFont('bold'),
      fontSize: 18,
      lineHeight: 24,
    },
    subheader: {
      ...getFont(),
      fontSize: 16,
      lineHeight: 20,
    },
    subheader2: {
      ...getFont('bold'),
      fontSize: 16,
      lineHeight: 20,
    },
    body: {
      ...getFont(),
      fontSize: 14,
      lineHeight: 20,
    },
    body2: {
      ...getFont('bold'),
      fontSize: 14,
      lineHeight: 20,
    },
    caption: {
      ...getFont(),
      fontSize: 12,
      lineHeight: 16,
    },
    caption2: {
      ...getFont('bold'),
      fontSize: 12,
      lineHeight: 12,
    },
  },
};

export {
  weightMap,
  weights,
  getFont,
  extractInvalidStyleData,
  font,
  isValidWeight,
  isWeightValue,
};
