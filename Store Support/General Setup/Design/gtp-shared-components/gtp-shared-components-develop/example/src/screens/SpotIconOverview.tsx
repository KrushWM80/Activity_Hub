import * as React from 'react';
import {SafeAreaView, StyleSheet} from 'react-native';
import {Header, Page, Section, DirectionView} from '../components';
import {SpotIcon, Icons} from '@walmart/gtp-shared-components';

const SpotIconOverview: React.FC = () => {
  return (
    <SafeAreaView style={styles.container}>
      <Page>
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

export {SpotIconOverview};
