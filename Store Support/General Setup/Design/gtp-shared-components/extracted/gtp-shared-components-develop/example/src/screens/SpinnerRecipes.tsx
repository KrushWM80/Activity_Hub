/* eslint-disable react-native/no-inline-styles */
import * as React from 'react';
import {StyleSheet, View} from 'react-native';
import {
  Button,
  SpinnerOverlay,
  Body,
  delay,
} from '@walmart/gtp-shared-components';
import {Header, Page, Section, VariantText} from '../components';

const Spacer = () => <View style={ss.spacer} />;

export const SpinnerRecipes: React.FC = () => {
  type Traits = {
    childVisible: boolean;
    visible: boolean;
    darken: boolean;
    transparent: boolean;
  };
  const [traits, setTraits] = React.useState<Traits>({
    childVisible: false,
    visible: false,
    darken: false,
    transparent: true,
  });

  const defaultTag = () => {
    return (
      <>
        <Header>
          Spinner (auto close){'\n  '}
          <VariantText>{`<SpinnerOverlay
          visible={showOverlay}
          transparent={true} />`}</VariantText>
        </Header>
        <Section space={10}>
          <View style={ss.innerContainer}>
            <Spacer />
            <Button
              onPress={() =>
                setTraits({
                  ...traits,
                  visible: !traits.visible,
                })
              }>
              Show Spinner
            </Button>
          </View>
        </Section>
      </>
    );
  };

  const darkenSpinner = () => {
    return (
      <>
        <Header>
          Spinner (with darken true){'\n  '}
          <VariantText>{`<SpinnerOverlay
          visible={true}
          darken={true}
          spinnerColor={'white'}
          transparent={true} />`}</VariantText>
        </Header>
        <Section space={10}>
          <View style={ss.innerContainer}>
            <Spacer />
            <Button
              onPress={() =>
                setTraits({
                  ...traits,
                  visible: !traits.visible,
                  darken: true,
                })
              }>
              Show Spinner
            </Button>
          </View>
        </Section>
      </>
    );
  };

  const spinnerWithChildren = () => {
    return (
      <>
        <Header>
          Spinner (with children){'\n  '}
          <VariantText>{`<SpinnerOverlay
          visible={true}
          transparent={true}>
          \t{Children}\n   </SpinnerOverlay>`}</VariantText>
        </Header>
        <Section space={10}>
          <View style={ss.innerContainer}>
            <Spacer />
            <Button
              onPress={() =>
                setTraits({
                  ...traits,
                  visible: !traits.visible,
                  childVisible: !traits.childVisible,
                  darken: true,
                })
              }>
              Show Spinner
            </Button>
          </View>
        </Section>
      </>
    );
  };

  const darkenSpinnerWithChildren = () => {
    return (
      <>
        <Header>
          Spinner (with darken, transparent=false and children){'\n  '}
          <VariantText>{`<SpinnerOverlay
          visible={true}
          darken={true}
          spinnerColor={'white'}
          transparent={false}>
          \t{Children}\n   </SpinnerOverlay>`}</VariantText>
        </Header>
        <Section space={10}>
          <View style={ss.innerContainer}>
            <Spacer />
            <Button
              onPress={() =>
                setTraits({
                  ...traits,
                  visible: !traits.visible,
                  childVisible: !traits.childVisible,
                  darken: true,
                  transparent: false,
                })
              }>
              Show Spinner
            </Button>
          </View>
        </Section>
      </>
    );
  };

  React.useEffect(() => {
    // Simulates an API call finishing
    if (!traits.childVisible && traits.visible) {
      delay(2000).then(() => {
        setTraits({...traits, visible: false, darken: false});
      });
    }
  }, [traits]);

  const spinnerOverlay = (): React.ReactNode => {
    return (
      <SpinnerOverlay
        visible={traits.visible}
        darken={traits.darken}
        spinnerColor={traits.darken ? 'white' : 'gray'}
        transparent={traits.transparent}>
        {traits.childVisible && (
          <>
            <Body
              weight="bold"
              UNSAFE_style={[
                ss.overlayBody,
                traits.darken ? {color: 'white'} : {},
              ]}>
              We're saving your selection
            </Body>
            <Button
              variant="primary"
              onPress={() =>
                setTraits({
                  ...traits,
                  childVisible: false,
                  visible: false,
                  darken: false,
                  transparent: true,
                })
              }>
              Close Overlay
            </Button>
          </>
        )}
      </SpinnerOverlay>
    );
  };

  return (
    <Page>
      {defaultTag()}
      {darkenSpinner()}
      {spinnerWithChildren()}
      {spinnerOverlay()}
      {darkenSpinnerWithChildren()}
    </Page>
  );
};

const ss = StyleSheet.create({
  overlayBody: {
    textAlign: 'center',
    margin: 16,
  },
  innerContainer: {
    padding: 10,
    alignItems: 'center',
    justifyContent: 'center',
  },
  spacer: {
    height: 8,
  },
});
