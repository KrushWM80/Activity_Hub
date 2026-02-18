import * as React from 'react';
import {Platform, SafeAreaView, StyleSheet, Text} from 'react-native';
import {StackNavigationProp} from '@react-navigation/stack';
import {colors} from '@walmart/gtp-shared-icons';
import {Button} from '../components/Button';
import {NavigationProps} from '../types';
import {Page} from '../components/Page';
import {Header} from '../components/Header';
import {Section} from '../components/Section';
import {HomeScreenHeader} from '../components/HomeScreenHeader';

type Props = {
  navigation: StackNavigationProp<NavigationProps, 'Home'>;
};

const HomeScreen = ({navigation}: Props) => {
  const buttons = [{target: 'Icons' as const}];

  return (
    <SafeAreaView style={ss.container}>
      <HomeScreenHeader />
      <Page>
        <Header>Components</Header>
        <Section color={colors.gray['5']}>
          {buttons.map(({target}) => {
            return (
              <Button
                key={target}
                onPress={() => navigation.navigate(target)}
                style={ss.contentButton}>
                <Text style={ss.contentButtonText}>{target}</Text>
              </Button>
            );
          })}
        </Section>
      </Page>
    </SafeAreaView>
  );
};

const ss = StyleSheet.create({
  container: {
    backgroundColor: 'white',
    flex: 1,
    paddingTop: 18,
    justifyContent: 'space-around',
  },
  header: {
    backgroundColor: '#f8f8f8',
    paddingVertical: 16,
    marginHorizontal: 16,
    marginBottom: -16,
    borderRadius: 16,
    borderWidth: 0.3,
    borderColor: colors.gray['40'],
    zIndex: 8,
  },
  headerBackground: {
    opacity: 0.2,
    resizeMode: 'contain',
  },
  image: {
    alignSelf: 'center',
    height: 40,
    resizeMode: 'contain',
    width: '100%',
  },
  text: {
    fontFamily: Platform.OS === 'ios' ? 'Courier' : 'monospace',
    fontSize: 14,
    marginTop: 12,
    textAlign: 'center',
  },
  buttonRow: {
    flexDirection: 'row',
    justifyContent: 'space-evenly',
    marginBottom: 8,
  },
  linkText: {
    fontSize: 16,
    marginVertical: 8,
    color: colors.blue['100'],
    fontWeight: 'bold',
  },
  contentButton: {
    width: '70%',
    alignSelf: 'center',
    height: 42,
  },
  contentButtonText: {
    flexShrink: 1,
    fontSize: 16,
    fontWeight: 'bold',
    color: colors.black,
  },
});

export {HomeScreen};
