import * as React from 'react';
import {StyleSheet, View} from 'react-native';
import {Header, Page, Section, VariantText} from '../components';
import {
  Button,
  ProgressTracker,
  ProgressTrackerItem,
} from '@walmart/gtp-shared-components';

const ProgressTrackerRecipes: React.FC = () => {
  type ProgressTrackerCodeProps = {
    trackerSuccessCodeVisible: boolean;
    trackerErrorCodeVisible: boolean;
    trackerInfoCodeVisible: boolean;
  };
  const [trackerCode, setTrackerCode] =
    React.useState<ProgressTrackerCodeProps>({
      trackerSuccessCodeVisible: false,
      trackerErrorCodeVisible: false,
      trackerInfoCodeVisible: false,
    });
  /**
   *
   * @param buttonLabel
   * @param listName
   * @returns button ui to Show or hides sample code
   */
  const displayCodeButton = (buttonLabel: string, trackerName: string) => {
    const trackerNameVal: boolean =
      trackerCode[trackerName as keyof ProgressTrackerCodeProps];
    return (
      <Button
        UNSAFE_style={styles.displayCodeBtn}
        variant="tertiary"
        onPress={() =>
          setTrackerCode({...trackerCode, [trackerName]: !trackerNameVal})
        }>
        {buttonLabel}
      </Button>
    );
  };

  const infoProgressTracker = () => {
    const buttonLabel = trackerCode.trackerInfoCodeVisible
      ? 'Hide code'
      : 'Show Code';
    const codeSample = `<ProgressTracker activeIndex={0} variant="info">
    <ProgressTrackerItem>Check In</ProgressTrackerItem>
    <ProgressTrackerItem>Meal In</ProgressTrackerItem>
    <ProgressTrackerItem>Meal out</ProgressTrackerItem>
    <ProgressTrackerItem>Check Out</ProgressTrackerItem>
  </ProgressTracker>`;
    return (
      <>
        <View>
          <Header>
            Progress Tracker (with variant="info"){'\n  '}
            {trackerCode.trackerInfoCodeVisible && (
              <VariantText>{codeSample}</VariantText>
            )}
          </Header>
          {displayCodeButton(buttonLabel, 'trackerInfoCodeVisible')}
        </View>
        <Section>
          <ProgressTracker activeIndex={0} variant="info">
            <ProgressTrackerItem>Check In</ProgressTrackerItem>
            <ProgressTrackerItem>Meal In</ProgressTrackerItem>
            <ProgressTrackerItem>Meal out</ProgressTrackerItem>
            <ProgressTrackerItem>Check Out</ProgressTrackerItem>
          </ProgressTracker>
        </Section>
      </>
    );
  };

  const errorProgressTracker = () => {
    const buttonLabel = trackerCode.trackerErrorCodeVisible
      ? 'Hide code'
      : 'Show Code';
    const codeSample = `<ProgressTracker activeIndex={2} variant="error">
    <ProgressTrackerItem>Applied TOR</ProgressTrackerItem>
    <ProgressTrackerItem>Manager Reviewed</ProgressTrackerItem>
    <ProgressTrackerItem>TOR Rejected</ProgressTrackerItem>
  </ProgressTracker>`;
    return (
      <>
        <View>
          <Header>
            Progress Tracker (with variant="error"){'\n  '}
            {trackerCode.trackerErrorCodeVisible && (
              <VariantText>{codeSample}</VariantText>
            )}
          </Header>
          {displayCodeButton(buttonLabel, 'trackerErrorCodeVisible')}
        </View>
        <Section>
          <ProgressTracker activeIndex={2} variant="error">
            <ProgressTrackerItem>Applied TOR</ProgressTrackerItem>
            <ProgressTrackerItem>Manager Reviewed</ProgressTrackerItem>
            <ProgressTrackerItem>TOR Rejected</ProgressTrackerItem>
          </ProgressTracker>
        </Section>
      </>
    );
  };

  const successProgressTracker = () => {
    const buttonLabel = trackerCode.trackerSuccessCodeVisible
      ? 'Hide code'
      : 'Show Code';
    const codeSample = `<ProgressTracker activeIndex={2} variant="success">
    <ProgressTrackerItem>Applied TOR</ProgressTrackerItem>
    <ProgressTrackerItem>Manager Reviewed</ProgressTrackerItem>
    <ProgressTrackerItem>TOR Approved</ProgressTrackerItem>
  </ProgressTracker>`;
    return (
      <>
        <View>
          <Header>
            Progress Tracker (with variant="success"){'\n  '}
            {trackerCode.trackerSuccessCodeVisible && (
              <VariantText>{codeSample}</VariantText>
            )}
          </Header>
          {displayCodeButton(buttonLabel, 'trackerSuccessCodeVisible')}
        </View>
        <Section>
          <ProgressTracker activeIndex={2} variant="success">
            <ProgressTrackerItem>Applied TOR</ProgressTrackerItem>
            <ProgressTrackerItem>Manager Reviewed</ProgressTrackerItem>
            <ProgressTrackerItem>TOR Approved</ProgressTrackerItem>
          </ProgressTracker>
        </Section>
      </>
    );
  };

  return (
    <Page>
      {infoProgressTracker()}
      {errorProgressTracker()}
      {successProgressTracker()}
    </Page>
  );
};

const styles = StyleSheet.create({
  displayCodeBtn: {position: 'absolute', bottom: 0, right: 2},
});

export {ProgressTrackerRecipes};
