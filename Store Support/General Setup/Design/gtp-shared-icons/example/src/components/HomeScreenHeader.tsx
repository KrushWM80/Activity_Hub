import * as React from 'react';
import {
  Image,
  ImageBackground,
  StyleSheet,
  Text,
  TextStyle,
  View,
} from 'react-native';
import pkg from '../../../package.json';
import {colors} from '@walmart/gtp-shared-icons';
import {HomeScreenLinks} from './HomeScreenLinks';

const HomeScreenHeader = () => {
  return (
    <>
      <ImageBackground
        style={ss.header}
        imageStyle={ss.headerBackground}
        source={require('../assets').livingdesign}>
        <View style={ss.titleContainer}>
          <Image style={ss.image} source={require('../assets').logo} />
          <Text style={ss.title}>React Native Icons</Text>
        </View>
        <Text style={ss.version}>Version: {pkg.version}</Text>
        <HomeScreenLinks />
      </ImageBackground>
    </>
  );
};

const ss = StyleSheet.create({
  header: {
    justifyContent: 'flex-start',
    backgroundColor: colors.white,
    paddingVertical: 16,
    opacity: 0.7,
    marginHorizontal: 16,
    marginTop: 8,
    borderRadius: 16,
    borderWidth: 0.3,
    borderColor: colors.gray['40'],
  },
  headerBackground: {
    opacity: 0.2,
    resizeMode: 'contain',
  },
  image: {
    alignSelf: 'flex-start',
    height: 40,
    resizeMode: 'contain',
    width: '50%',
  },
  titleContainer: {
    flexDirection: 'row',
    justifyContent: 'flex-start',
    alignItems: 'center',
    width: '100%',
    marginBottom: 6,
  },
  title: {
    fontWeight: 'bold',
    marginTop: 2,
    color: colors.black,
    fontSize: 19,
    marginLeft: -9,
  } as TextStyle,
  version: {
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 16,
    color: colors.black,
  } as TextStyle,
});

export {HomeScreenHeader};
