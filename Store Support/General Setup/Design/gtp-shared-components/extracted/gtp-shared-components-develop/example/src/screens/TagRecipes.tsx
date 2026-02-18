import * as React from 'react';
import {View, StyleSheet} from 'react-native';
import {colors, Icons, Tag} from '@walmart/gtp-shared-components';
import {Header, Page, VariantText} from '../components';

const Spacer = () => <View style={ss.spacer} />;

const DefaultTag: React.FC = () => {
  return (
    <>
      <Header>
        Tag (with variant & color){'\n  '}
        <VariantText>{`variant='primary' color="green"`}</VariantText>
      </Header>
      <View style={ss.outerContainer}>
        <View style={ss.innerContainer}>
          <Spacer />
          <Tag variant="primary" color="green">
            Green
          </Tag>
        </View>
      </View>
    </>
  );
};

const SecondaryTag: React.FC = () => {
  return (
    <>
      <Header>
        Tag (with variant & color){'\n  '}
        <VariantText>{`variant='secondary' color="spark"`}</VariantText>
      </Header>
      <View style={ss.outerContainer}>
        <View style={ss.innerContainer}>
          <Spacer />
          <Tag variant="secondary" color="spark">
            Green
          </Tag>
        </View>
      </View>
    </>
  );
};

const TertiaryTag: React.FC = () => {
  return (
    <>
      <Header>
        Tag (with variant & color){'\n  '}
        <VariantText>{`variant='tertiary' color="purple"`}</VariantText>
      </Header>
      <View style={ss.outerContainer}>
        <View style={ss.innerContainer}>
          <Spacer />
          <Tag variant="tertiary" color="purple">
            Green
          </Tag>
        </View>
      </View>
    </>
  );
};

const LeadingTag: React.FC = () => {
  return (
    <>
      <Header>
        Tag (with variant & color){'\n  '}
        <VariantText>{`variant='primary' color="red" leading={<Icons.ThumbUpIcon />`}</VariantText>
      </Header>
      <View style={ss.outerContainer}>
        <View style={ss.innerContainer}>
          <Spacer />
          <Tag variant="primary" color="red" leading={<Icons.ThumbUpIcon />}>
            Red
          </Tag>
        </View>
      </View>
    </>
  );
};

const TagRecipes: React.FC = () => {
  return (
    <Page>
      <DefaultTag />
      <SecondaryTag />
      <TertiaryTag />
      <LeadingTag />
    </Page>
  );
};

const ss = StyleSheet.create({
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

export {TagRecipes};
