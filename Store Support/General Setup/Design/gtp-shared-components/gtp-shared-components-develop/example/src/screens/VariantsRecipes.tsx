import * as React from 'react';
import {Header, Page, VariantText} from '../components';
import {colors, Variants} from '@walmart/gtp-shared-components';
import {StyleSheet, View} from 'react-native';

const Spacer = () => <View style={ss.spacer} />;

const VariantsRecipes: React.FC = () => {
  const defaultVariant = () => {
    return (
      <>
        <Header>
          Variants (with one variant){'\n  '}
          <VariantText>{`<Variants\n\tvariants={[colors.blue['100']]} />`}</VariantText>
        </Header>
        <View style={ss.outerContainer}>
          <View style={ss.innerContainer}>
            <Spacer />
            <Variants variants={[colors.blue['100']]} />
          </View>
        </View>
      </>
    );
  };

  const twoVariant = () => {
    return (
      <>
        <Header>
          Variants (with two variant){'\n  '}
          <VariantText>{`<Variants\n\tvariants={[colors.blue['100'],\n\t\tcolors.red['100']]} />`}</VariantText>
          {'\n  '}
        </Header>
        <View style={ss.outerContainer}>
          <View style={ss.innerContainer}>
            <Spacer />
            <Variants variants={[colors.blue['100'], colors.red['100']]} />
          </View>
        </View>
      </>
    );
  };

  const multipleVariant = () => {
    return (
      <>
        <Header>
          Variants (with multiple variant){'\n  '}
          <VariantText>{`<Variants
              variants={[
                colors.blue['100'],
                colors.green['100'],
                colors.red['100'],
                colors.spark['100'],
                colors.purple['100']\n\t]}/>`}</VariantText>
          {'\n  '}
        </Header>
        <View style={ss.outerContainer}>
          <View style={ss.innerContainer}>
            <Spacer />
            <Variants
              variants={[
                colors.blue['100'],
                colors.green['100'],
                colors.red['100'],
                colors.spark['100'],
                colors.purple['100'],
              ]}
            />
          </View>
        </View>
      </>
    );
  };

  const variantWithoutColor = () => {
    return (
      <>
        <Header>
          Variants (color=false){'\n  '}
          <VariantText>{`<Variants
              colors={false}
              variants={[colors.blue['100'], colors.red['100']]}
            />`}</VariantText>
          {'\n  '}
        </Header>
        <View style={ss.outerContainer}>
          <View style={ss.innerContainer}>
            <Spacer />
            <Variants
              colors={false}
              variants={[colors.blue['100'], colors.red['100']]}
            />
          </View>
        </View>
      </>
    );
  };

  const multiVariantWithoutColor = () => {
    return (
      <>
        <Header>
          Variants (color=false){'\n  '}
          <VariantText>{`<Variants
              colors={false}
              variants={[
                colors.blue['100'],
                colors.green['100'],
                colors.red['100'],
                colors.spark['100'],
                colors.purple['100'],
              ]}/>`}</VariantText>
          {'\n  '}
        </Header>
        <View style={ss.outerContainer}>
          <View style={ss.innerContainer}>
            <Spacer />
            <Variants
              colors={false}
              variants={[
                colors.blue['100'],
                colors.green['100'],
                colors.red['100'],
                colors.spark['100'],
                colors.purple['100'],
              ]}
            />
          </View>
        </View>
      </>
    );
  };

  return (
    <Page>
      {defaultVariant()}
      {twoVariant()}
      {multipleVariant()}
      {variantWithoutColor()}
      {multiVariantWithoutColor()}
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

export {VariantsRecipes};
