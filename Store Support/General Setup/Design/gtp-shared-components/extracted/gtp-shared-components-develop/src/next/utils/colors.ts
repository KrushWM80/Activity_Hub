import * as globals from '@livingdesign/tokens/dist/react-native/light/regular/globals';

export type Color =
  | 'gray'
  | 'blue'
  | 'green'
  | 'orange'
  | 'pink'
  | 'purple'
  | 'red'
  | 'spark'
  | 'yellow';

export type ColorNumber =
  | '5'
  | '10'
  | '20'
  | '30'
  | '40'
  | '50'
  | '60'
  | '70'
  | '80'
  | '90'
  | '100'
  | '110'
  | '120'
  | '130'
  | '140'
  | '150'
  | '160'
  | '170'
  | '180';
type ColorTint = Record<ColorNumber, string>;
type Colors = Record<Color, ColorTint>;

type ColorVariant = 'positive' | 'primary' | 'negative' | 'warning';
type ColorVariantValue = 'min' | 'low' | 'base' | 'high' | 'max';
type ColorVariants = Record<ColorVariant, Record<ColorVariantValue, string>>;

export type ColorsType = Colors &
  ColorVariants & {
    black: string;
    white: string;
    separator: Partial<ColorTint>;
  };

export const colors: ColorsType = {
  black: globals.colorCoreBlack, // '#000'
  white: globals.colorCoreWhite, // '#fff'
  gray: {
    '5': globals.colorCoreGray5, // '#f8f8f8',
    '10': globals.colorCoreGray10, // '#f1f1f2',
    '20': globals.colorCoreGray20, // '#e3e4e5',
    '30': globals.colorCoreGray30, // '#d5d6d8',
    '40': globals.colorCoreGray40, // '#c7c8cb',
    '50': globals.colorCoreGray50, // '#babbbe',
    '60': globals.colorCoreGray60, // '#acadb0',
    '70': globals.colorCoreGray70, // '#9e9fa3',
    '80': globals.colorCoreGray80, // '#909196',
    '90': globals.colorCoreGray90, // '#828489',
    '100': globals.colorCoreGray100, // '#74767c',
    '110': globals.colorCoreGray110, // '#686a70',
    '120': globals.colorCoreGray120, // '#5d5e63',
    '130': globals.colorCoreGray130, // '#515357',
    '140': globals.colorCoreGray140, // '#46474a',
    '150': globals.colorCoreGray150, // '#3a3b3e',
    '160': globals.colorCoreGray160, // '#2e2f32',
    '170': globals.colorCoreGray170, // '#232325',
    '180': globals.colorCoreGray180, // '#171819',
  },
  blue: {
    '5': globals.colorCoreBlue5, // '#f2f8fd'
    '10': globals.colorCoreBlue10, // '#e6f1fc'
    '20': globals.colorCoreBlue20, // '#cce3f8'
    '30': globals.colorCoreBlue30, // '#b3d4f5'
    '40': globals.colorCoreBlue40, // '#99c6f1'
    '50': globals.colorCoreBlue50, // '#80b8ee'
    '60': globals.colorCoreBlue60, // '#66aaea'
    '70': globals.colorCoreBlue70, // '#4d9ce7'
    '80': globals.colorCoreBlue80, // '#338de3'
    '90': globals.colorCoreBlue90, // '#1a7fe0'
    '100': globals.colorCoreBlue100, // '#0071dc'
    '110': globals.colorCoreBlue110, // '#0066c6'
    '120': globals.colorCoreBlue120, // '#005ab0'
    '130': globals.colorCoreBlue130, // '#004f9a'
    '140': globals.colorCoreBlue140, // '#004484'
    '150': globals.colorCoreBlue150, // '#00396e'
    '160': globals.colorCoreBlue160, // '#002d58'
    '170': globals.colorCoreBlue170, // '#002242'
    '180': globals.colorCoreBlue180, // '#00162c'
  },
  green: {
    '5': globals.colorCoreGreen5, // '#f4f9f2'
    '10': globals.colorCoreGreen10, // '#eaf3e6'
    '20': globals.colorCoreGreen20, // '#d4e7cd'
    '30': globals.colorCoreGreen30, // '#bfdbb3'
    '40': globals.colorCoreGreen40, // '#aacf9a'
    '50': globals.colorCoreGreen50, // '#95c381'
    '60': globals.colorCoreGreen60, // '#7fb768'
    '70': globals.colorCoreGreen70, // '#6aab4f'
    '80': globals.colorCoreGreen80, // '#559f35'
    '90': globals.colorCoreGreen90, // '#3f931c'
    '100': globals.colorCoreGreen100, // '#2a8703'
    '110': globals.colorCoreGreen110, // '#267a03'
    '120': globals.colorCoreGreen120, // '#226c02'
    '130': globals.colorCoreGreen130, // '#1d5f02'
    '140': globals.colorCoreGreen140, // '#195102'
    '150': globals.colorCoreGreen150, // '#154402'
    '160': globals.colorCoreGreen160, // '#113601'
    '170': globals.colorCoreGreen170, // '#0d2901'
    '180': globals.colorCoreGreen180, // '#081b01'
  },
  orange: {
    '5': globals.colorCoreOrange5, // '#fff7f2'
    '10': globals.colorCoreOrange10, // '#fff0e6'
    '20': globals.colorCoreOrange20, // '#fee0cc'
    '30': globals.colorCoreOrange30, // '#fed1b3'
    '40': globals.colorCoreOrange40, // '#fdc199'
    '50': globals.colorCoreOrange50, // '#fdb280'
    '60': globals.colorCoreOrange60, // '#fca266'
    '70': globals.colorCoreOrange70, // '#fc934d'
    '80': globals.colorCoreOrange80, // '#fb8333'
    '90': globals.colorCoreOrange90, // '#fb741a'
    '100': globals.colorCoreOrange100, // '#fa6400'
    '110': globals.colorCoreOrange110, // '#e15300'
    '120': globals.colorCoreOrange120, // '#c83c00'
    '130': globals.colorCoreOrange130, // '#af2f00'
    '140': globals.colorCoreOrange140, // '#962300'
    '150': globals.colorCoreOrange150, // '#7d1900'
    '160': globals.colorCoreOrange160, // '#641100'
    '170': globals.colorCoreOrange170, // '#4b0a00'
    '180': globals.colorCoreOrange180, // '#320500'
  },
  pink: {
    '5': globals.colorCorePink5, // '#fcf4f9'
    '10': globals.colorCorePink10, // '#faeaf4'
    '20': globals.colorCorePink20, // '#f5d5e9'
    '30': globals.colorCorePink30, // '#efc0de'
    '40': globals.colorCorePink40, // '#eaabd3'
    '50': globals.colorCorePink50, // '#e596c8'
    '60': globals.colorCorePink60, // '#e080bc'
    '70': globals.colorCorePink70, // '#db6bb1'
    '80': globals.colorCorePink80, // '#d556a6'
    '90': globals.colorCorePink90, // '#d0419b'
    '100': globals.colorCorePink100, // '#cb2c90'
    '110': globals.colorCorePink110, // '#b72882'
    '120': globals.colorCorePink120, // '#a22373'
    '130': globals.colorCorePink130, // '#8e1f65'
    '140': globals.colorCorePink140, // '#7a1a56'
    '150': globals.colorCorePink150, // '#661648'
    '160': globals.colorCorePink160, // '#51123a'
    '170': globals.colorCorePink170, // '#3d0d2b'
    '180': globals.colorCorePink180, // '#29091d'
  },
  purple: {
    '5': globals.colorCorePurple5, // '#f7f5f9'
    '10': globals.colorCorePurple10, // '#efebf2'
    '20': globals.colorCorePurple20, // '#e0d6e5'
    '30': globals.colorCorePurple30, // '#d0c2d8'
    '40': globals.colorCorePurple40, // '#c1adcb'
    '50': globals.colorCorePurple50, // '#b199bf'
    '60': globals.colorCorePurple60, // '#a184b2'
    '70': globals.colorCorePurple70, // '#9270a5'
    '80': globals.colorCorePurple80, // '#825b98'
    '90': globals.colorCorePurple90, // '#73478b'
    '100': globals.colorCorePurple100, // '#63327e'
    '110': globals.colorCorePurple110, // '#592d71'
    '120': globals.colorCorePurple120, // '#4f2865'
    '130': globals.colorCorePurple130, // '#452358'
    '140': globals.colorCorePurple140, // '#3b1e4c'
    '150': globals.colorCorePurple150, // '#32193f'
    '160': globals.colorCorePurple160, // '#281432'
    '170': globals.colorCorePurple170, // '#1e0f26'
    '180': globals.colorCorePurple180, // '#140a19'
  },
  red: {
    '5': globals.colorCoreRed5, // '#fdf4f4'
    '10': globals.colorCoreRed10, // '#fce8e9'
    '20': globals.colorCoreRed20, // '#f8d2d3'
    '30': globals.colorCoreRed30, // '#f5bbbd'
    '40': globals.colorCoreRed40, // '#f2a4a7'
    '50': globals.colorCoreRed50, // '#ef8e92'
    '60': globals.colorCoreRed60, // '#eb777c'
    '70': globals.colorCoreRed70, // '#e86066'
    '80': globals.colorCoreRed80, // '#e54950'
    '90': globals.colorCoreRed90, // '#e1333a'
    '100': globals.colorCoreRed100, // '#de1c24'
    '110': globals.colorCoreRed110, // '#c81920'
    '120': globals.colorCoreRed120, // '#b2161d'
    '130': globals.colorCoreRed130, // '#9b1419'
    '140': globals.colorCoreRed140, // '#851116'
    '150': globals.colorCoreRed150, // '#6f0e12'
    '160': globals.colorCoreRed160, // '#590b0e'
    '170': globals.colorCoreRed170, // '#43080b'
    '180': globals.colorCoreRed180, // '#2c0607'
  },
  spark: {
    '5': globals.colorCoreSpark5, // '#fffcf4'
    '10': globals.colorCoreSpark10, // '#fff9e9'
    '20': globals.colorCoreSpark20, // '#fff3d2'
    '30': globals.colorCoreSpark30, // '#ffedbc'
    '40': globals.colorCoreSpark40, // '#ffe7a6'
    '50': globals.colorCoreSpark50, // '#ffe190'
    '60': globals.colorCoreSpark60, // '#ffda79'
    '70': globals.colorCoreSpark70, // '#ffd463'
    '80': globals.colorCoreSpark80, // '#ffce4d'
    '90': globals.colorCoreSpark90, // '#ffc836'
    '100': globals.colorCoreSpark100, // '#ffc220'
    '110': globals.colorCoreSpark110, // '#e6a31d'
    '120': globals.colorCoreSpark120, // '#cc851a'
    '130': globals.colorCoreSpark130, // '#b36a16'
    '140': globals.colorCoreSpark140, // '#995213'
    '150': globals.colorCoreSpark150, // '#803d10'
    '160': globals.colorCoreSpark160, // '#662b0d'
    '170': globals.colorCoreSpark170, // '#4d1c0a'
    '180': globals.colorCoreSpark180, // '#330f06'
  },
  yellow: {
    '5': globals.colorCoreYellow5, // '#fffef2'
    '10': globals.colorCoreYellow10, // '#fffee6'
    '20': globals.colorCoreYellow20, // '#fffccc'
    '30': globals.colorCoreYellow30, // '#fffbb3'
    '40': globals.colorCoreYellow40, // '#fffa99'
    '50': globals.colorCoreYellow50, // '#fff980'
    '60': globals.colorCoreYellow60, // '#fff766'
    '70': globals.colorCoreYellow70, // '#fff64d'
    '80': globals.colorCoreYellow80, // '#fff533'
    '90': globals.colorCoreYellow90, // '#fff31a'
    '100': globals.colorCoreYellow100, // '#fff200'
    '110': globals.colorCoreYellow110, // '#e6cb00'
    '120': globals.colorCoreYellow120, // '#cca700'
    '130': globals.colorCoreYellow130, // '#b38600'
    '140': globals.colorCoreYellow140, // '#996900'
    '150': globals.colorCoreYellow150, // '#804f00'
    '160': globals.colorCoreYellow160, // '#663800'
    '170': globals.colorCoreYellow170, // '#4d2500'
    '180': globals.colorCoreYellow180, // '#331500'
  },
  positive: {
    min: globals.colorPositiveMin, // #eaf3e6
    low: globals.colorPositiveLow, // #95c381
    base: globals.colorPositiveBase, // #2a8703
    high: globals.colorPositiveHigh, // #1d5f02
    max: globals.colorPositiveMax, // #113601
  },
  primary: {
    min: globals.colorPrimaryMin, // #e6f1fc
    low: globals.colorPrimaryLow, // #80b8ee
    base: globals.colorPrimaryBase, // #0071dc
    high: globals.colorPrimaryHigh, // #004f9a
    max: globals.colorPrimaryMax, // #002d58
  },
  negative: {
    min: globals.colorNegativeMin, // #fce8e9
    low: globals.colorNegativeLow, // #ef8e92
    base: globals.colorNegativeBase, // #de1c24
    high: globals.colorNegativeHigh, // #9b1419
    max: globals.colorNegativeMax, // #590b0e
  },
  warning: {
    min: globals.colorWarningMin, // #fff9e9
    low: globals.colorWarningLow, // #ffe190
    base: globals.colorWarningBase, // #ffc220
    high: globals.colorWarningHigh, // #b36a16
    max: globals.colorWarningMax, // #662b02
  },
  separator: {
    '100': globals.colorSeparator100, // #e2e4e5
  },
};

export const colorVariants = Object.keys(colors);

export type TypographyColors =
  | 'black'
  | 'blue5'
  | 'blue10'
  | 'blue20'
  | 'blue30'
  | 'blue40'
  | 'blue50'
  | 'blue60'
  | 'blue70'
  | 'blue80'
  | 'blue90'
  | 'blue100'
  | 'blue110'
  | 'blue120'
  | 'blue130'
  | 'blue140'
  | 'blue150'
  | 'blue160'
  | 'blue170'
  | 'blue180'
  | 'gray5'
  | 'gray10'
  | 'gray20'
  | 'gray30'
  | 'gray40'
  | 'gray50'
  | 'gray60'
  | 'gray70'
  | 'gray80'
  | 'gray90'
  | 'gray100'
  | 'gray110'
  | 'gray120'
  | 'gray130'
  | 'gray140'
  | 'gray150'
  | 'gray160'
  | 'gray170'
  | 'gray180'
  | 'green5'
  | 'green10'
  | 'green20'
  | 'green30'
  | 'green40'
  | 'green50'
  | 'green60'
  | 'green70'
  | 'green80'
  | 'green90'
  | 'green100'
  | 'green110'
  | 'green120'
  | 'green130'
  | 'green140'
  | 'green150'
  | 'green160'
  | 'green170'
  | 'green180'
  | 'orange5'
  | 'orange10'
  | 'orange20'
  | 'orange30'
  | 'orange40'
  | 'orange50'
  | 'orange60'
  | 'orange70'
  | 'orange80'
  | 'orange90'
  | 'orange100'
  | 'orange110'
  | 'orange120'
  | 'orange130'
  | 'orange140'
  | 'orange150'
  | 'orange160'
  | 'orange170'
  | 'orange180'
  | 'pink5'
  | 'pink10'
  | 'pink20'
  | 'pink30'
  | 'pink40'
  | 'pink50'
  | 'pink60'
  | 'pink70'
  | 'pink80'
  | 'pink90'
  | 'pink100'
  | 'pink110'
  | 'pink120'
  | 'pink130'
  | 'pink140'
  | 'pink150'
  | 'pink160'
  | 'pink170'
  | 'pink180'
  | 'purple5'
  | 'purple10'
  | 'purple20'
  | 'purple30'
  | 'purple40'
  | 'purple50'
  | 'purple60'
  | 'purple70'
  | 'purple80'
  | 'purple90'
  | 'purple100'
  | 'purple110'
  | 'purple120'
  | 'purple130'
  | 'purple140'
  | 'purple150'
  | 'purple160'
  | 'purple170'
  | 'purple180'
  | 'red5'
  | 'red10'
  | 'red20'
  | 'red30'
  | 'red40'
  | 'red50'
  | 'red60'
  | 'red70'
  | 'red80'
  | 'red90'
  | 'red100'
  | 'red110'
  | 'red120'
  | 'red130'
  | 'red140'
  | 'red150'
  | 'red160'
  | 'red170'
  | 'red180'
  | 'spark5'
  | 'spark10'
  | 'spark20'
  | 'spark30'
  | 'spark40'
  | 'spark50'
  | 'spark60'
  | 'spark70'
  | 'spark80'
  | 'spark90'
  | 'spark100'
  | 'spark110'
  | 'spark120'
  | 'spark130'
  | 'spark140'
  | 'spark150'
  | 'spark160'
  | 'spark170'
  | 'spark180'
  | 'yellow5'
  | 'yellow10'
  | 'yellow20'
  | 'yellow30'
  | 'yellow40'
  | 'yellow50'
  | 'yellow60'
  | 'yellow70'
  | 'yellow80'
  | 'yellow90'
  | 'yellow100'
  | 'yellow110'
  | 'yellow120'
  | 'yellow130'
  | 'yellow140'
  | 'yellow150'
  | 'yellow160'
  | 'yellow170'
  | 'yellow180'
  | 'white';
