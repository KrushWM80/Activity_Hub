import * as React from 'react';
import {SafeAreaView, StyleSheet, Image} from 'react-native';
import {Button, ErrorMessage} from '@walmart/gtp-shared-components';
import {displayPopupAlert} from './screensFixtures';
import {Header, Page, Section} from '../components';
// @ts-ignore
import noInternetError from '@walmart/gtp-shared-components/assets/images/no_internet_error.png';
const ErrorMessageOverview: React.FC = () => {
  return (
    <SafeAreaView style={styles.container}>
      <Page>
        <Header>ErrorMessage</Header>
        <Section space={10}>
          <ErrorMessage
            title={'No internet connection'}
            UNSAFE_style={styles.padding}
            media={<Image source={noInternetError} />}
            actions={
              <Button
                variant="primary"
                onPress={() =>
                  displayPopupAlert('No internet connection', 'Try Again')
                }>
                Try Again
              </Button>
            }>
            Make sure you’re connected to WiFi or data and try again.
          </ErrorMessage>
        </Section>
      </Page>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  spacer: {
    width: '100%',
    height: '6%',
  },
  spacer2: {
    width: '100%',
    height: 20,
  },

  padding: {
    padding: 15,
  },
});

export {ErrorMessageOverview};
