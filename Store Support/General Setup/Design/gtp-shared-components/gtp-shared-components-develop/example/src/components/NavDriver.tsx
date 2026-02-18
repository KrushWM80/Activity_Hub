import * as React from 'react';
import {SafeAreaView, StyleSheet} from 'react-native';
import {StackNavigationProp} from '@react-navigation/stack';
import {Button} from '@walmart/gtp-shared-components';
import type {NavigationProps} from '../types';
import {Page, Header, Section} from '.';

type ButtonsScreenProps = {
  navigation: StackNavigationProp<NavigationProps, 'Home'>;
  buttons: {target: string; title?: string}[];
  header: string;
};

const NavDriver = ({navigation, buttons, header}: ButtonsScreenProps) => {
  return (
    <SafeAreaView style={styles.container}>
      <Page>
        <Header>{header}</Header>
        <Section>
          {buttons.map(({target, title}, index) => {
            return (
              <Button
                size="small"
                key={`${target}${index}`}
                variant="secondary"
                onPress={() => navigation.navigate(target as any)}>
                {title ?? target}
              </Button>
            );
          })}
        </Section>
      </Page>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingBottom: 18,
  },
});

export {NavDriver};
