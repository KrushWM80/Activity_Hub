import * as React from 'react';
import {StyleSheet, Text, View} from 'react-native';
import {Button} from '../components/Button';
import pkg from '../../../package.json';
import {colors} from '@walmart/gtp-shared-icons';

let openURLInBrowser: (arg0: string) => void;
if (!process.env.STYLEGUIDIST_ENV) {
  openURLInBrowser = require('react-native/Libraries/Core/Devtools/openURLInBrowser');
} else {
  openURLInBrowser = () => {};
}

const links = [
  {
    title: 'Docs',
    url: pkg.homepage,
  },
  {
    title: 'Repo',
    url: pkg.repository.url,
  },
  {
    title: 'Living Design',
    url: 'https://livingdesign.walmart.com',
  },
];

const HomeScreenLinks = () => {
  return (
    <View style={ss.buttonRow}>
      {links.map(item => {
        const {title, url} = item;
        return (
          <Button
            key={title}
            style={ss.contentButton}
            onPress={() => openURLInBrowser(url)}>
            <Text style={ss.contentButtonText}>{title}</Text>
          </Button>
        );
      })}
    </View>
  );
};

const ss = StyleSheet.create({
  buttonRow: {
    flexDirection: 'row',
    justifyContent: 'space-evenly',
  },
  contentButtonText: {
    flexShrink: 1,
    fontSize: 16,
    fontWeight: 'bold',
    color: colors.black,
  },
  contentButton: {
    alignSelf: 'center',
    height: 36,
  },
});

export {HomeScreenLinks};
