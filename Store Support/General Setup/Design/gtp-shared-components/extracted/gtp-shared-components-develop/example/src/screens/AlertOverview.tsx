import * as React from 'react';
import {SafeAreaView, StyleSheet} from 'react-native';
import {Header, Page, Section, VariantText} from '../components';
import {Alert} from '@walmart/gtp-shared-components';
import {displayPopupAlert} from './screensFixtures';

const AlertOverview: React.FC = () => {
  return (
    <SafeAreaView style={styles.container}>
      <Page>
        <Header>
          Alert {'\n  '}
          <VariantText>variant: info, warning, success, error</VariantText>
        </Header>
        <Section>
          <Alert
            variant="info"
            children="Reservation about to expire"
            actionButtonProps={{
              children: 'Reserve now',
              onPress: () => {
                displayPopupAlert('Action', 'Reserve now pressed');
              },
            }}
          />
          <Alert
            variant="error"
            children="Reservation expired"
            actionButtonProps={{
              children: 'Find another time',
              onPress: () => {
                displayPopupAlert('Action', 'Find another time pressed');
              },
            }}
          />
          <Alert
            variant="success"
            children="Pickup reservation booked"
            actionButtonProps={{
              children: 'Pickup now',
              onPress: () => {
                displayPopupAlert('Action', 'Pickup now pressed');
              },
            }}
          />
          <Alert
            variant="warning"
            children="Reservation about to expire"
            actionButtonProps={{
              children: 'Reserve now',
              onPress: () => {
                displayPopupAlert('Action', 'Reserve now pressed');
              },
            }}
          />
        </Section>
        <Header>
          Alert {'\n  '}
          <VariantText>long text label</VariantText>
        </Header>
        <Section>
          <Alert
            variant="info"
            children="Reservation about to expire and many many many other things here going on and on forever"
            actionButtonProps={{
              children: 'Reserve now',
              onPress: () => {
                displayPopupAlert('Action', 'Reserve now pressed');
              },
            }}
          />
          <Alert
            variant="error"
            children="Reservation expired and many many many other things here going on and on forever"
            actionButtonProps={{
              children: 'Find another time',
              onPress: () => {
                displayPopupAlert('Action', 'Find another time pressed');
              },
            }}
          />
          <Alert
            variant="success"
            children="Pickup reservation booked and many many many other things here going on and on forever"
            actionButtonProps={{
              children: 'Pickup now',
              onPress: () => {
                displayPopupAlert('Action', 'Pickup now pressed');
              },
            }}
          />
          <Alert
            variant="warning"
            children="Reservation about to expire and many many many other things here going on and on forever"
            actionButtonProps={{
              children: 'Reserve now',
              onPress: () => {
                displayPopupAlert('Action', 'Reserve now pressed');
              },
            }}
          />
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

export {AlertOverview};
