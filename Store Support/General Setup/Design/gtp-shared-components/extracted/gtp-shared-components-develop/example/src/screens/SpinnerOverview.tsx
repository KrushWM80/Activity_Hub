/* eslint-disable react-native/no-inline-styles */
import * as React from 'react';
import {StyleSheet} from 'react-native';
import {Header, Page, Section} from '../components';
import {
  Button,
  Checkbox,
  SpinnerOverlay,
  Body,
  delay,
} from '@walmart/gtp-shared-components';

export const SpinnerOverview: React.FC = () => {
  const SpinnerOverlayWithContent = () => {
    const [showOverlay, setShowOverlay] = React.useState(false);
    const [darken, setDarken] = React.useState(false);
    const [transparent, setTransparent] = React.useState(true);

    return (
      <>
        <Header>SpinnerOverlay (with children)</Header>
        <Section>
          <Button onPress={() => setShowOverlay(true)}>
            Show Spinner Overlay
          </Button>
          <Checkbox
            label="Darkened"
            checked={darken}
            onPress={() => setDarken(!darken)}
          />
          <Checkbox
            label="Transparent"
            checked={transparent}
            onPress={() => setTransparent(!transparent)}
          />
        </Section>
        <SpinnerOverlay
          visible={showOverlay}
          onRequestClose={() => setShowOverlay(false)}
          darken={darken}
          spinnerColor={darken ? 'white' : 'gray'}
          transparent={transparent}>
          <Body
            weight="bold"
            UNSAFE_style={[styles.overlayBody, darken ? {color: 'white'} : {}]}>
            We're saving your selection
          </Body>
          <Button variant="primary" onPress={() => setShowOverlay(false)}>
            Close Overlay
          </Button>
        </SpinnerOverlay>
      </>
    );
  };

  const SpinnerOverlayAutoClosing = () => {
    const [showOverlay, setShowOverlay] = React.useState(false);
    React.useEffect(() => {
      // Simulates an API call finishing
      if (showOverlay) {
        delay(2000).then(() => setShowOverlay(false));
      }
    }, [showOverlay]);

    return (
      <>
        <Header>SpinnerOverlay (auto-closing)</Header>
        <Section>
          <Button onPress={() => setShowOverlay(true)}>
            Show Spinner Overlay
          </Button>
        </Section>
        <SpinnerOverlay
          visible={showOverlay}
          onRequestClose={() => setShowOverlay(false)}
          darken={true}
          spinnerColor={'white'}
          transparent={true}
        />
      </>
    );
  };

  return (
    <Page>
      <SpinnerOverlayWithContent />
      <SpinnerOverlayAutoClosing />
    </Page>
  );
};

const styles = StyleSheet.create({
  overlayBody: {
    textAlign: 'center',
    margin: 16,
  },
});
