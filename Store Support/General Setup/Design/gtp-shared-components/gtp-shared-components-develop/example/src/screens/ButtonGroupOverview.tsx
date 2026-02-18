import * as React from 'react';
import {Text, StyleSheet, View} from 'react-native';
import {Header, Page} from '../components';
import {colors, Button, ButtonGroup} from '@walmart/gtp-shared-components';
import {displayPopupAlert} from './screensFixtures';

const ButtonGroupOverview: React.FC = () => {
  return (
    <Page>
      <Header>ButtonGroup</Header>
      <View style={ss.outerContainer}>
        <ButtonGroup UNSAFE_style={ss.buttonGroup}>
          <Button
            variant="secondary"
            onPress={() =>
              displayPopupAlert('Action', 'Secondary button pressed')
            }>
            One
          </Button>
          <Button
            variant="secondary"
            onPress={() =>
              displayPopupAlert('Action', 'Secondary button pressed')
            }>
            Two
          </Button>
          <Button
            variant="secondary"
            onPress={() =>
              displayPopupAlert('Action', 'Secondary button pressed')
            }>
            Three
          </Button>
          <Button
            variant="primary"
            onPress={() =>
              displayPopupAlert('Action', 'Primary button pressed')
            }>
            Four
          </Button>
          <Button
            variant="primary"
            onPress={() =>
              displayPopupAlert('Action', 'Primary button pressed')
            }>
            Five
          </Button>
          <Button
            variant="primary"
            onPress={() =>
              displayPopupAlert('Action', 'Primary button pressed')
            }>
            Six
          </Button>
        </ButtonGroup>
        <ButtonGroup UNSAFE_style={ss.buttonGroup}>
          <Button
            variant="tertiary"
            onPress={() => displayPopupAlert('Action', 'Button "One" pressed')}>
            One
          </Button>
          <Button
            variant="secondary"
            onPress={() => displayPopupAlert('Action', 'Button "Two" pressed')}>
            Two
          </Button>
          <Button
            variant="primary"
            onPress={() =>
              displayPopupAlert('Action', 'Button "Three" pressed')
            }>
            Three
          </Button>
        </ButtonGroup>
        <View style={ss.spacer} />
        <Text style={ss.variantInBody}>{'isFullWidth={true}'}</Text>
        <ButtonGroup isFullWidth>
          <Button
            variant="secondary"
            onPress={() =>
              displayPopupAlert('Action', 'Secondary button pressed')
            }>
            Secondary
          </Button>
          <Button
            variant="primary"
            onPress={() =>
              displayPopupAlert('Action', 'Primary button pressed')
            }>
            Primary
          </Button>
        </ButtonGroup>
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

export {ButtonGroupOverview};
