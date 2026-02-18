import * as React from 'react';
import {StyleSheet, View} from 'react-native';
import {Header, Page, VariantText} from '../components';
import {SpotIcon, Icons, colors} from '@walmart/gtp-shared-components';

const DefaultSpotIcon: React.FC = () => {
  const spotIconSnippet = `<SpotIcon>\n\t<Icons.TruckIcon color="blue" />\n  </SpotIcon>`;

  return (
    <>
      <Header>
        StyledText (default){'\n  '}
        <VariantText>{spotIconSnippet}</VariantText>
      </Header>
      <View style={styles.outerContainer}>
        <View style={styles.innerContainer}>
          <Spacer />
          <SpotIcon>
            <Icons.TruckIcon color="blue" />
          </SpotIcon>
        </View>
      </View>
    </>
  );
};

const SpotIconWithColor: React.FC = () => {
  const spotIconSnippet = `<SpotIcon color='white' size='small'>\n\t<Icons.HomeIcon color="green" />\n  </SpotIcon>`;

  return (
    <>
      <Header>
        StyledText (with color and size){'\n  '}
        <VariantText>{spotIconSnippet}</VariantText>
      </Header>
      <View style={styles.outerContainer}>
        <View style={styles.innerContainer}>
          <Spacer />
          <SpotIcon color="white" size="small">
            <Icons.HomeIcon color="green" />
          </SpotIcon>
        </View>
      </View>
    </>
  );
};

const SpotIconWithColorAndSize: React.FC = () => {
  const spotIconSnippet = `<SpotIcon color='white' size='large'>\n\t<Icons.HomeIcon color="green" />\n  </SpotIcon>`;

  return (
    <>
      <Header>
        StyledText (with color and size){'\n  '}
        <VariantText>{spotIconSnippet}</VariantText>
      </Header>
      <View style={styles.outerContainer}>
        <View style={styles.innerContainer}>
          <Spacer />
          <SpotIcon color="white" size="large">
            <Icons.HomeIcon color="green" />
          </SpotIcon>
        </View>
      </View>
    </>
  );
};

const Spacer = () => <View style={styles.spacer} />;
const SpotIconRecipes: React.FC = () => {
  return (
    <Page>
      <DefaultSpotIcon />
      <SpotIconWithColor />
      <SpotIconWithColorAndSize />
    </Page>
  );
};

const styles = StyleSheet.create({
  section: {
    paddingVertical: 12,
    paddingHorizontal: 16,
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
  container: {
    flex: 1,
    paddingVertical: 20,
  },
  spacer: {
    height: 8,
  },
});

export {SpotIconRecipes};
