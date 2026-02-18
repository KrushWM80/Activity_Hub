import * as React from 'react';
import {SafeAreaView, StyleSheet, Image} from 'react-native';
import {Button, ErrorMessage, colors} from '@walmart/gtp-shared-components';
import {displayPopupAlert} from './screensFixtures';
import {Header, Page, Section, VariantText} from '../components';
// @ts-ignore
import noInternetError from '@walmart/gtp-shared-components/assets/images/no_internet_error.png';

const ErrorMessageRecipes: React.FC = () => {
  const noInternet = `No internet connection`;
  const codeSnippet1 = `<ErrorMessage \n\t title={${noInternet}!}> \n {Make sure you’re connected to WiFi or data and try again.} \n </ErrorMessage>\n`;
  const codeSnippet2 = `<ErrorMessage \n\t title={${noInternet}!}
  \tmedia={<Image source={error_img} \n\t actions={ \n\t\t <Button \n\t\t\t variant="primary" \n\t\t\t onPress={actionHandler}> \n\t}>
  \t{Make sure you’re connected to WiFi or data and try again.}
  </ErrorMessage>\n`;

  return (
    <SafeAreaView style={styles.container}>
      <Page>
        <Header>
          ErrorMessage(without media and action){'\n\n'}
          <VariantText>{codeSnippet1}</VariantText>
        </Header>
        <Section space={10}>
          <ErrorMessage title={`${noInternet}!`} UNSAFE_style={styles.padding}>
            Make sure you’re connected to WiFi or data and try again.
          </ErrorMessage>
        </Section>

        <Header>
          ErrorMessage(with media and action){'\n\n'}
          <VariantText>{codeSnippet2}</VariantText>
        </Header>
        <Section space={10}>
          <ErrorMessage
            title={`${noInternet}!`}
            UNSAFE_style={styles.padding}
            media={<Image source={noInternetError} />}
            actions={
              <Button
                variant="primary"
                onPress={() => displayPopupAlert(noInternet, 'Try Again')}>
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
});

export {ErrorMessageRecipes};
