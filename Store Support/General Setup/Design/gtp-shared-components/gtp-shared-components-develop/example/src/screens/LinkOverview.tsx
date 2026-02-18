import * as React from 'react';
import {Text, StyleSheet, View} from 'react-native';
import {Header, Page} from '../components';
import {colors, Link} from '@walmart/gtp-shared-components';
import {displayPopupAlert} from './screensFixtures';

const LinkOverview: React.FC = () => {
  return (
    <Page>
      <Header>Link</Header>
      <View style={ss.outerContainer}>
        <View style={ss.innerContainer}>
          <Link
            children="This is a Link"
            color="default"
            onPress={() => displayPopupAlert('Action', 'Link pressed')}
          />
          <Link
            children="This is a disabled Link"
            onPress={() => displayPopupAlert('Action', 'Link pressed')}
            disabled
          />
        </View>
        <View style={ss.innerContainer}>
          <Text>
            {'This '}
            <Link
              children="link"
              color="default"
              onPress={() => displayPopupAlert('Action', 'Link pressed')}
            />
            {' is embedded'}
          </Text>
          <Text>
            {'This '}
            <Link
              disabled
              children="link"
              color="default"
              onPress={() => displayPopupAlert('Action', 'Link pressed')}
            />
            {' is embedded'}
          </Text>
        </View>
      </View>
      <Header>Link (white variant)</Header>
      <View style={[ss.outerContainer, {backgroundColor: colors.blue['100']}]}>
        <View style={ss.innerContainer}>
          <Link
            children="This is a Link"
            color="white"
            onPress={() => displayPopupAlert('Action', 'Link button pressed')}
          />
          <Link
            children="This is a disabled Link"
            disabled
            color="white"
            onPress={() => displayPopupAlert('Action', 'Link button pressed')}
          />
        </View>
        <View style={ss.innerContainer}>
          <Text style={ss.linkContainer}>
            {'This '}
            <Link
              children="link"
              color="white"
              onPress={() => displayPopupAlert('Action', 'Link pressed')}
            />
            {' is embedded'}
          </Text>
          <Text style={ss.linkContainer}>
            {'This '}
            <Link
              disabled
              children="link"
              color="white"
              onPress={() => displayPopupAlert('Action', 'Link pressed')}
            />
            {' is embedded'}
          </Text>
        </View>
      </View>
    </Page>
  );
};

const ss = StyleSheet.create({
  variantText: {
    fontSize: 15,
  },
  buttonGroup: {
    marginVertical: 16,
  },
  linkContainer: {
    color: 'white',
  },
  innerContainer: {
    flex: 1,
    justifyContent: 'space-around',
    flexDirection: 'row',
    padding: 10,
  },
  outerContainer: {
    backgroundColor: colors.gray['5'],
    borderWidth: 1,
    borderBottomLeftRadius: 12,
    borderBottomRightRadius: 12,
    borderColor: colors.gray['10'],
  },
  linkTextColor: {
    color: 'white',
  },
  variantInBody: {
    alignSelf: 'center',
    marginVertical: 12,
    paddingHorizontal: 12,
    marginLeft: 20,
    fontSize: 15,
    lineHeight: 20,
    color: colors.blue['90'],
    borderColor: colors.blue['90'],
    borderWidth: 0.5,
  },
  spacer: {
    height: 16,
  },
});

export {LinkOverview};
