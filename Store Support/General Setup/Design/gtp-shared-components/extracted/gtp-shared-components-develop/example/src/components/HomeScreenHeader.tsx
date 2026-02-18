import * as React from 'react';
import {
  Appearance,
  Image,
  ImageBackground,
  StyleSheet,
  Text,
  TextStyle,
  useColorScheme,
  View,
} from 'react-native';
import pkg from '../../../package.json';
import {colors, getFont, Switch} from '@walmart/gtp-shared-components';
import {HomeScreenLinks} from './HomeScreenLinks';

const HomeScreenHeader = () => {
  const isDark = useColorScheme() === 'dark';

  return (
    <>
      <ImageBackground
        style={styles.header}
        imageStyle={styles.headerBackground}
        source={require('../assets').livingdesign}>
        <View style={styles.titleContainer}>
          <Image style={styles.image} source={require('../assets').logo} />
          <Text style={styles.title}>React Native</Text>
        </View>
        <Text style={styles.version}>Version: {pkg.version}</Text>
        <HomeScreenLinks />
        <View style={styles.switch}>
          <Switch
            label="Dark Mode (alpha)"
            isOn={isDark}
            onValueChange={() => {
              Appearance.setColorScheme(isDark ? 'light' : 'dark');
            }}
          />
        </View>
      </ImageBackground>
    </>
  );
};

const styles = StyleSheet.create({
  header: {
    justifyContent: 'flex-start',
    backgroundColor: colors.white,
    paddingVertical: 16,
    opacity: 0.9,
    marginHorizontal: 16,
    marginVertical: 8,
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
    marginLeft: 20,
  },
  titleContainer: {
    flexDirection: 'row',
    justifyContent: 'flex-start',
    alignItems: 'center',
    width: '100%',
    marginBottom: 6,
  },
  title: {
    ...getFont('bold'),
    marginTop: 2,
    color: colors.black,
    fontSize: 20,
    textAlign: 'center',
  } as TextStyle,
  version: {
    ...getFont('bold'),
    textAlign: 'center',
    marginBottom: 16,
    color: colors.black,
  } as TextStyle,
  switch: {
    alignItems: 'center',
    marginTop: 16,
  },
});

export {HomeScreenHeader};
