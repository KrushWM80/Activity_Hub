import * as React from 'react';
import {StyleSheet, View, SafeAreaView, Alert as RNAlert} from 'react-native';
import {useSnackbar, colors, Button} from '@walmart/gtp-shared-components';
import {Page, Header, Section} from '../components';

const SnackbarOverview = () => {
  const {addSnack} = useSnackbar();

  return (
    <SafeAreaView style={ss.container}>
      <Page>
        <Header>SnackbarProvider + useSnackbar</Header>
        <Section space={false} inset={false}>
          <Button
            onPress={() =>
              addSnack({
                message: 'I am a snack',
              })
            }>
            Simple Snackbar
          </Button>
          <View style={ss.spacer2} />
          <Button
            onPress={() =>
              addSnack({
                message: 'I am a snack',
                customPosition: '35%',
                // customPosition: 200,
              })
            }>
            Snackbar with customPosition
          </Button>
          <View style={ss.spacer2} />
          <Button
            onPress={() =>
              addSnack({
                message: 'A snack with action button',
                actionButton: {
                  caption: 'Action',
                  onPress: () => {
                    RNAlert.alert('Action Button pressed');
                  },
                },
                onClose: () => {},
              })
            }>
            Snackbar with actionButton
          </Button>
          <View style={ss.spacer2} />
          <Button
            onPress={() =>
              addSnack({
                message:
                  'When you gonna realize it was just that the time was wrong, Juliet?',
                actionButton: {
                  caption: 'Action',
                  onPress: () => {
                    RNAlert.alert('Action Button pressed');
                  },
                },
                onClose: () => {},
              })
            }>
            Snackbar with long text
          </Button>
          <View style={ss.spacer2} />
          <Button
            onPress={() =>
              addSnack({
                message:
                  'And I dreamed your dream for you and now your dream is real How can you look at me as if I was just another one of your deals, Juliet?',
                actionButton: {
                  caption: 'Action',
                  onPress: () => {
                    RNAlert.alert('Action Button pressed');
                  },
                },
                onClose: () => {},
                customPosition: '50%',
              })
            }>
            Snackbar with long text and customPosition
          </Button>
          <View style={ss.spacer2} />
          <Button
            onPress={() =>
              addSnack({
                accessible: true,
                accessibilityLabel: 'Custom accessibility label',
                message: 'A snack with accessibility props',
                actionButton: {
                  caption: 'Action',
                  onPress: () => {
                    RNAlert.alert('Action Button pressed');
                  },
                },
                onClose: () => {},
              })
            }>
            Snackbar with accessibility props
          </Button>
          <View style={ss.spacer2} />
          <Button
            onPress={() =>
              addSnack({
                message: 'A snack with accessibility props',
                actionButton: {
                  accessible: true,
                  accessibilityLabel: 'Custom action label',
                  caption: 'Action',
                  onPress: () => {
                    RNAlert.alert('Action Button pressed');
                  },
                },
                onClose: () => {},
              })
            }>
            Snackbar with custom action accessibility props
          </Button>
        </Section>
      </Page>
    </SafeAreaView>
  );
};

const ss = StyleSheet.create({
  container: {
    flex: 1,
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
  trailing: {},
  trailingLink: {
    marginRight: 12,
    marginVertical: 8,
  },
  spacer: {
    width: '100%',
    height: '6%',
  },
  spacer2: {
    width: '100%',
    height: 20,
  },
});

SnackbarOverview.displayName = 'SnackbarOverview';
export {SnackbarOverview};
