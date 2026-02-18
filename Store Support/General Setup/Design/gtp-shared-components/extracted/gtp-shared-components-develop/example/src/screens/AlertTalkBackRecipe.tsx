import * as React from 'react';
import {SafeAreaView, StyleSheet} from 'react-native';
import {Header, Page, Section, VariantText} from '../components';
import {Alert, Button} from '@walmart/gtp-shared-components';
import {displayPopupAlert} from './screensFixtures';

const AlertTalkBackRecipe: React.FC = () => {
  const [showAlert, setShowAlert] = React.useState(false);

  return (
    <SafeAreaView style={styles.container}>
      <Page>
        <Header>
          Alert {'\n  '}
          <VariantText>variant: info, warning, success, error</VariantText>
        </Header>
        <Section>
          {showAlert && (
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
          )}
          <Button variant="primary" onPress={() => setShowAlert(!showAlert)}>
            Show Alert
          </Button>
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

export {AlertTalkBackRecipe};
