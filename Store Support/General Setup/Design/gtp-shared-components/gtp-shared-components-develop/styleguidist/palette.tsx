/* eslint-disable react-native/no-inline-styles */
import * as React from 'react';
import {StyleSheet, View} from 'react-native';

import startCase from 'lodash/startCase';

import {Body} from '../src';
import {contrastColors} from '../src/next/utils';
import {colors} from '../src/next/utils';

type ColorKeys = keyof typeof colors;
type ColorTileProps = {
  backgroundColor: string;
  keyName: string;
};

const ColorTile: React.FC<ColorTileProps> = (props) => {
  const {backgroundColor, keyName} = props;
  const color = contrastColors(backgroundColor);

  return (
    <View style={[ss.tile, {backgroundColor, borderColor: color}]}>
      <Body weight="light" style={[ss.caption, {color, fontSize: 12}]}>
        {keyName}
      </Body>
    </View>
  );
};

type ColorRowProps = {
  color: ColorKeys;
};

const ColorRow: React.FC<ColorRowProps> = (props) => {
  const {color} = props;
  if (color === 'white' || color === 'black') {
    return null;
  }
  const colorValues = colors[color];
  return (
    <View style={ss.container}>
      <Body UNSAFE_style={ss.title}>{startCase(color)}</Body>
      {Object.keys(colorValues).map((key) => (
        <ColorTile
          key={`${color}_${key}`}
          backgroundColor={colorValues[key as keyof typeof colorValues]}
          keyName={key.padStart(2, '0')}
        />
      ))}
    </View>
  );
};

const Palette = () => {
  const colorKeys = Object.keys(colors).filter(
    (key) => key !== 'white' && key !== 'black',
  ) as Array<ColorKeys>;
  return (
    <View style={ss.grid}>
      <View style={ss.container}>
        <Body UNSAFE_style={ss.title}>White</Body>
        <ColorTile key={'white'} backgroundColor={'#fff'} keyName="" />
      </View>
      <View style={ss.container}>
        <Body UNSAFE_style={ss.title}>Black</Body>
        <ColorTile key={'black'} backgroundColor={'#000'} keyName="" />
      </View>
      {colorKeys.map((key) => (
        <ColorRow color={key} />
      ))}
    </View>
  );
};

const ss = StyleSheet.create({
  grid: {
    position: 'relative',
    alignSelf: 'center',
  },
  container: {
    alignItems: 'center',
    flexDirection: 'row',
  },
  title: {
    minWidth: 70,
  },
  caption: {
    alignSelf: 'center',
    textAlign: 'center',
    flex: 1,
  },
  tile: {
    flexDirection: 'row',
    margin: 1,
    width: 36,
    height: 36,
    textAlign: 'center',
    textAlignVertical: 'center',
    borderWidth: 1,
    borderStyle: 'solid',
    borderRadius: 18,
  },
});

export {Palette};
