import * as React from 'react';
import {SafeAreaView, StyleSheet, Image} from 'react-native';
import {Header, Page, Section, DirectionView, VariantText} from '../components';
import {
  Alert,
  Banner,
  Button,
  SpotIcon,
  ErrorMessage,
  Icons,
} from '@walmart/gtp-shared-components';
import {displayPopupAlert} from './screensFixtures';
// @ts-ignore
import noInternetError from '@walmart/gtp-shared-components/assets/images/no_internet_error.png';
const MessagingOverview: React.FC = () => {
  const [isBannerErrorVisible, setIsBannerErrorVisible] = React.useState(true);
  const [isBannerInfoVisible, setIsBannerInfoVisible] = React.useState(true);
  const [isBannerSuccessVisible, setIsBannerSuccessVisible] =
    React.useState(true);
  const [isBannerWarningVisible, setIsBannerWarningVisible] =
    React.useState(true);

  const [isBannerLongInfoVisible, setIsBannerLongInfoVisible] =
    React.useState(true);
  const [isBannerLongErrorVisible, setIsBannerLongErrorVisible] =
    React.useState(true);
  const [isBannerLongSuccessVisible, setIsBannerLongSuccessVisible] =
    React.useState(true);
  const [isBannerLongWarningVisible, setIsBannerLongWarningVisible] =
    React.useState(true);

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
        <Header>
          Banner {'\n  '}
          <VariantText>variant: info, warning, success, error</VariantText>
        </Header>
        <Section>
          {isBannerInfoVisible ? (
            <Banner
              variant="info"
              onClose={() => {
                setIsBannerInfoVisible(false);
              }}>
              This is an info message
            </Banner>
          ) : null}
          {isBannerErrorVisible ? (
            <Banner
              variant="error"
              onClose={() => {
                setIsBannerErrorVisible(false);
              }}>
              This is an error message
            </Banner>
          ) : null}

          {isBannerSuccessVisible ? (
            <Banner
              variant="success"
              onClose={() => {
                setIsBannerSuccessVisible(false);
              }}>
              This is a success message
            </Banner>
          ) : null}
          {isBannerWarningVisible ? (
            <Banner
              variant="warning"
              onClose={() => {
                setIsBannerWarningVisible(false);
              }}>
              This is a warning message
            </Banner>
          ) : null}
        </Section>

        <Header>
          Banner {'\n  '}
          <VariantText>long text</VariantText>
        </Header>
        <Section>
          {isBannerLongInfoVisible ? (
            <Banner
              variant="info"
              onClose={() => {
                setIsBannerLongInfoVisible(false);
              }}>
              This is an info message and many many many other things here going
              on and on forever
            </Banner>
          ) : null}
          {isBannerLongErrorVisible ? (
            <Banner
              variant="error"
              onClose={() => {
                setIsBannerLongErrorVisible(false);
              }}>
              This is an error message and many many many other things here
              going on and on forever
            </Banner>
          ) : null}

          {isBannerLongSuccessVisible ? (
            <Banner
              variant="success"
              onClose={() => {
                setIsBannerLongSuccessVisible(false);
              }}>
              This is a success message and many many many other things here
              going on and on forever
            </Banner>
          ) : null}
          {isBannerLongWarningVisible ? (
            <Banner
              variant="warning"
              onClose={() => {
                setIsBannerLongWarningVisible(false);
              }}>
              This is a warning message and many many many other things here
              going on and on forever
            </Banner>
          ) : null}
        </Section>
        <Header>
          Banner {'\n  '}
          <VariantText>with leading and closeIconColor</VariantText>
        </Header>
        <Section>
          {isBannerInfoVisible ? (
            <Banner
              variant="info"
              leading={<Icons.WalmartPayIcon />}
              onClose={() => {
                setIsBannerInfoVisible(false);
              }}>
              This is an info message
            </Banner>
          ) : null}
          {isBannerErrorVisible ? (
            <Banner
              variant="error"
              closeIconColor={'white'}
              leading={<Icons.WalmartPayIcon color="white" />}
              onClose={() => {
                setIsBannerErrorVisible(false);
              }}>
              This is an info message and many many many other things here going
              on and on forever
            </Banner>
          ) : null}

          {isBannerSuccessVisible ? (
            <Banner
              variant="success"
              closeIconColor={'white'}
              leading={<Icons.WalmartPayIcon color="white" />}
              onClose={() => {
                setIsBannerSuccessVisible(false);
              }}>
              This is a success message
            </Banner>
          ) : null}
          {isBannerWarningVisible ? (
            <Banner
              variant="warning"
              closeIconColor={'white'}
              leading={<Icons.WalmartPayIcon color="white" />}
              onClose={() => {
                setIsBannerWarningVisible(false);
              }}>
              This is an info message and many many many other things here going
              on and on forever
            </Banner>
          ) : null}
        </Section>
        <Header>Spot Icons</Header>
        <Section space={10}>
          <DirectionView>
            <SpotIcon>
              <Icons.TruckIcon />
            </SpotIcon>
            <SpotIcon color="white">
              <Icons.CheckIcon />
            </SpotIcon>
            <SpotIcon size="large">
              <Icons.TruckIcon />
            </SpotIcon>
            <SpotIcon color="white" size="large">
              <Icons.CheckIcon />
            </SpotIcon>
          </DirectionView>
        </Section>
        <Header>Spot Icon with icon color</Header>
        <Section space={10}>
          <DirectionView>
            <SpotIcon>
              <Icons.TruckIcon color="blue" />
            </SpotIcon>
            <SpotIcon color="white">
              <Icons.CheckIcon color="green" />
            </SpotIcon>
            <SpotIcon size="large">
              <Icons.TruckIcon color="red" />
            </SpotIcon>
            <SpotIcon color="white" size="large">
              <Icons.CheckIcon color="red" />
            </SpotIcon>
          </DirectionView>
        </Section>
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

export {MessagingOverview};
