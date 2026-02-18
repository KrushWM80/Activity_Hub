import * as React from 'react';
import {View, StyleSheet} from 'react-native';
import {colors, Badge} from '@walmart/gtp-shared-components';
import {Header, Page, VariantText} from '../components';

const Spacer = () => <View style={ss.spacer} />;

const DefaultBadge: React.FC = () => {
  return (
    <>
      <Header>
        Badge (with no text){'\n  '}
        <VariantText>{'<Badge />'}</VariantText>
      </Header>
      <View style={ss.outerContainer}>
        <View style={ss.innerContainer}>
          <Spacer />
          <Badge />
        </View>
      </View>
    </>
  );
};

const BadgeWithLabel: React.FC = () => {
  return (
    <>
      <Header>
        Badge (with text){'\n  '}
        <VariantText>{"<Badge>{'10'}</Badge>"}</VariantText>
      </Header>
      <View style={ss.outerContainer}>
        <View style={ss.innerContainer}>
          <Spacer />
          <Badge>{10}</Badge>
        </View>
      </View>
    </>
  );
};

const BadgeWithColor: React.FC = () => {
  return (
    <>
      <Header>
        Badge (color and numerals){'\n  '}
        <VariantText>{"<Badge color={'red'}>{'1.24 lb'}</Badge>"}</VariantText>
      </Header>
      <View style={ss.outerContainer}>
        <View style={ss.innerContainer}>
          <Badge color={'red'}>{'1.24 lb'}</Badge>
        </View>
      </View>
    </>
  );
};

const BadgeRecipes: React.FC = () => {
  return (
    <Page>
      <DefaultBadge />
      <BadgeWithLabel />
      <BadgeWithColor />
    </Page>
  );
};

const ss = StyleSheet.create({
  section: {
    paddingVertical: 12,
    paddingHorizontal: 16,
  },
  innerContainer: {
    padding: 10,
    alignItems: 'flex-start',
  },
  outerContainer: {
    backgroundColor: colors.gray['5'],
    borderWidth: 1,
    borderBottomLeftRadius: 12,
    borderBottomRightRadius: 12,
    borderColor: colors.gray['10'],
  },
  spacer: {
    height: 8,
  },
});

export {BadgeRecipes};
