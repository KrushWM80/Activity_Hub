/* eslint-disable react-native/no-inline-styles */
import * as React from 'react';
import {StyleSheet, View, Text} from 'react-native';
import colors from '../src/theme/colors.json';
import _ from 'lodash';
import {contrastColors} from '../src/utils/utils';

const styles = StyleSheet.create({
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
    width: 35,
    height: 35,
    textAlign: 'center',
    textAlignVertical: 'center',
    borderWidth: 1,
    borderStyle: 'solid',
    borderRadius: 99999,
  },
});

type colorKeys = keyof typeof colors;

const ColorTile = ({
  backgroundColor,
  keyName,
}: {
  backgroundColor: string;
  keyName: string;
}) => {
  const color = contrastColors(backgroundColor);

  return (
    <View style={[styles.tile, {backgroundColor, borderColor: color}]}>
      <Text style={[styles.caption, {color, fontSize: 12}]}>{keyName}</Text>
    </View>
  );
};

const ColorRow = ({color}: {color: colorKeys}) => {
  if (color === 'white' || color === 'black') {
    return null;
  }
  const colorValues = colors[color];
  return (
    <View style={styles.container}>
      <Text style={styles.title}>{_.startCase(color)}</Text>
      {Object.keys(colorValues).map((key) => (
        //@ts-ignore
        <ColorTile
          key={`${color}_${key}`}
          backgroundColor={colorValues[key as keyof typeof colorValues]}
          keyName={key.padStart(2, '0')}
        />
      ))}
    </View>
  );
};

export const Palette = () => {
  const colorKeys = Object.keys(colors).filter(
    (key) => key !== 'white' && key !== 'black',
  ) as Array<colorKeys>;
  return (
    <View style={styles.grid}>
      <View style={styles.container}>
        <Text style={styles.title}>White</Text>
        <ColorTile key={'white'} backgroundColor={'#fff'} keyName="" />
      </View>
      <View style={styles.container}>
        <Text style={styles.title}>Black</Text>
        <ColorTile key={'black'} backgroundColor={'#000'} keyName="" />
      </View>
      {colorKeys.map((key) => (
        <ColorRow color={key} />
      ))}
    </View>
  );
};
