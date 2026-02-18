import * as React from 'react';
import {StyleSheet, View} from 'react-native';
import {Button} from '@walmart/gtp-shared-components';
import pkg from '../../../package.json';

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
    <View style={styles.buttonRow}>
      {links.map(item => {
        const {title, url} = item;
        return (
          <Button
            key={title}
            onPress={() => openURLInBrowser(url)}
            variant="secondary">
            {title}
          </Button>
        );
      })}
    </View>
  );
};

const styles = StyleSheet.create({
  buttonRow: {
    flexDirection: 'row',
    justifyContent: 'space-evenly',
  },
});

export {HomeScreenLinks};
