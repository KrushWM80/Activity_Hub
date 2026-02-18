// Don't want to simmplify this to preserve readability
import {TextStyle} from 'react-native';

type Weight = {
  [key: string]: TextStyle;
};

type ExpectedStyles = {
  regular: Weight;
  monospace: Weight;
};

export const expectedStylesDefaultsIOS: TextStyle = {
  fontFamily: 'Bogle',
  fontStyle: 'normal',
  fontWeight: '400',
};

export const expectedStylesDefaultsAndroid: TextStyle = {
  fontFamily: 'Bogle-Regular',
};

export const expectedStylesIOS: ExpectedStyles = {
  regular: {
    thin: {
      fontFamily: 'Bogle',
      fontStyle: 'normal',
      fontWeight: '100',
    },
    light: {
      fontFamily: 'Bogle',
      fontStyle: 'normal',
      fontWeight: '300',
    },
    normal: {
      fontFamily: 'Bogle',
      fontStyle: 'normal',
      fontWeight: '400',
    },
    medium: {
      fontFamily: 'Bogle',
      fontStyle: 'normal',
      fontWeight: '500',
    },
    bold: {fontFamily: 'Bogle', fontStyle: 'normal', fontWeight: '700'},
    black: {
      fontFamily: 'Bogle',
      fontStyle: 'normal',
      fontWeight: '900',
    },
    '100': {
      fontFamily: 'Bogle',
      fontStyle: 'normal',
      fontWeight: '100',
    },
    '300': {
      fontFamily: 'Bogle',
      fontStyle: 'normal',
      fontWeight: '300',
    },
    '400': {
      fontFamily: 'Bogle',
      fontStyle: 'normal',
      fontWeight: '400',
    },
    '500': {
      fontFamily: 'Bogle',
      fontStyle: 'normal',
      fontWeight: '500',
    },
    '700': {
      fontFamily: 'Bogle',
      fontStyle: 'normal',
      fontWeight: '700',
    },
    '900': {
      fontFamily: 'Bogle',
      fontStyle: 'normal',
      fontWeight: '900',
    },
  },
  monospace: {
    thin: {
      fontFamily: 'Bogle Mono',
      fontStyle: 'normal',
      fontWeight: '100',
    },
    light: {
      fontFamily: 'Bogle Mono',
      fontStyle: 'normal',
      fontWeight: '300',
    },
    normal: {
      fontFamily: 'Bogle Mono',
      fontStyle: 'normal',
      fontWeight: '400',
    },
    medium: {
      fontFamily: 'Bogle Mono',
      fontStyle: 'normal',
      fontWeight: '500',
    },
    bold: {
      fontFamily: 'Bogle Mono',
      fontStyle: 'normal',
      fontWeight: '700',
    },
    black: {
      fontFamily: 'Bogle Mono',
      fontStyle: 'normal',
      fontWeight: '900',
    },
    '100': {
      fontFamily: 'Bogle Mono',
      fontStyle: 'normal',
      fontWeight: '100',
    },
    '300': {
      fontFamily: 'Bogle Mono',
      fontStyle: 'normal',
      fontWeight: '300',
    },
    '400': {
      fontFamily: 'Bogle Mono',
      fontStyle: 'normal',
      fontWeight: '400',
    },
    '500': {
      fontFamily: 'Bogle Mono',
      fontStyle: 'normal',
      fontWeight: '500',
    },
    '700': {
      fontFamily: 'Bogle Mono',
      fontStyle: 'normal',
      fontWeight: '700',
    },
    '900': {
      fontFamily: 'Bogle Mono',
      fontStyle: 'normal',
      fontWeight: '900',
    },
  },
};

export const expectedStylesAndroid: ExpectedStyles = {
  regular: {
    thin: {
      fontFamily: 'Bogle-Thin',
    },
    light: {
      fontFamily: 'Bogle-Light',
    },
    normal: {
      fontFamily: 'Bogle-Regular',
    },
    medium: {
      fontFamily: 'Bogle-Medium',
    },
    bold: {
      fontFamily: 'Bogle-Bold',
    },
    black: {
      fontFamily: 'Bogle-Black',
    },
    '100': {
      fontFamily: 'Bogle-Thin',
    },
    '300': {
      fontFamily: 'Bogle-Light',
    },
    '400': {
      fontFamily: 'Bogle-Regular',
    },
    '500': {
      fontFamily: 'Bogle-Medium',
    },
    '700': {
      fontFamily: 'Bogle-Bold',
    },
    '900': {
      fontFamily: 'Bogle-Black',
    },
  },
  monospace: {
    thin: {
      fontFamily: 'BogleMono-Regular',
    },
    light: {
      fontFamily: 'BogleMono-Regular',
    },
    normal: {
      fontFamily: 'BogleMono-Regular',
    },
    medium: {
      fontFamily: 'BogleMono-Regular',
    },
    bold: {
      fontFamily: 'BogleMono-Bold',
    },
    black: {
      fontFamily: 'BogleMono-Bold',
    },
    '100': {
      fontFamily: 'BogleMono-Regular',
    },
    '300': {
      fontFamily: 'BogleMono-Regular',
    },
    '400': {
      fontFamily: 'BogleMono-Regular',
    },
    '500': {
      fontFamily: 'BogleMono-Regular',
    },
    '700': {
      fontFamily: 'BogleMono-Bold',
    },
    '900': {
      fontFamily: 'BogleMono-Bold',
    },
  },
};
