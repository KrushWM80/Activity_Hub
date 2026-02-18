import * as React from 'react';
import {View, StyleSheet} from 'react-native';
import {colors, Checkbox} from '@walmart/gtp-shared-components';
import {Header, Page, VariantText} from '../components';

const Spacer = () => <View style={ss.spacer} />;

const DefaultCheckbox: React.FC = () => {
  return (
    <>
      <Header>
        Checkbox (Default){'\n  '}
        <VariantText>{`<Checkbox />`}</VariantText>
      </Header>
      <View style={ss.outerContainer}>
        <View style={ss.innerContainer}>
          <Spacer />
          <Checkbox />
        </View>
      </View>
    </>
  );
};

const LabeledCheckbox: React.FC = () => {
  return (
    <>
      <Header>
        Checkbox (label){'\n  '}
        <VariantText>{`<Checkbox label={'label text'} />`}</VariantText>
      </Header>
      <View style={ss.outerContainer}>
        <View style={ss.innerContainer}>
          <Spacer />
          <Checkbox label={'label text'} checked={true} />
        </View>
      </View>
    </>
  );
};

const CheckedCheckbox: React.FC = () => {
  return (
    <>
      <Header>
        Checkbox (checked){'\n  '}
        <VariantText>{`<Checkbox checked={true} />`}</VariantText>
      </Header>
      <View style={ss.outerContainer}>
        <View style={ss.innerContainer}>
          <Checkbox checked={true} />
        </View>
      </View>
    </>
  );
};

const IndeterminateCheckbox: React.FC = () => {
  return (
    <>
      <Header>
        Checkbox (indeterminate){'\n  '}
        <VariantText>{`<Checkbox indeterminate={true} />`}</VariantText>
      </Header>
      <View style={ss.outerContainer}>
        <View style={ss.innerContainer}>
          <Spacer />
          <Checkbox indeterminate={true} />
        </View>
      </View>
    </>
  );
};

const ChackedAndDisabledCheckbox: React.FC = () => {
  return (
    <>
      <Header>
        Checkbox (checked and disabled){'\n  '}
        <VariantText>{`<Checkbox checked={true} disabled={true} />`}</VariantText>
      </Header>
      <View style={ss.outerContainer}>
        <View style={ss.innerContainer}>
          <Spacer />
          <Checkbox checked={true} disabled={true} />
        </View>
      </View>
    </>
  );
};

const CheckboxRecipes: React.FC = () => {
  return (
    <Page>
      <DefaultCheckbox />
      <LabeledCheckbox />
      <CheckedCheckbox />
      <IndeterminateCheckbox />
      <ChackedAndDisabledCheckbox />
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
  },
  outerContainer: {
    backgroundColor: colors.gray['5'],
    borderWidth: 1,
    borderBottomLeftRadius: 12,
    borderBottomRightRadius: 12,
    borderColor: colors.gray['10'],
  },
  sectionVerticalZero: {
    paddingVertical: 0,
  },
  noLabels: {
    paddingVertical: 12,
    paddingHorizontal: 16,
    flexDirection: 'row',
    alignItems: 'flex-start',
  },
  spacer: {
    height: 8,
  },
});

export {CheckboxRecipes};
