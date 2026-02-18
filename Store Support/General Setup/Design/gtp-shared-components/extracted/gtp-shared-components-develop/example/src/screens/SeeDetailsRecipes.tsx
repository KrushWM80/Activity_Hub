import * as React from 'react';
import {StyleSheet, SafeAreaView, View} from 'react-native';
import {colors, Body, SeeDetails} from '@walmart/gtp-shared-components';

import {Header, Page} from '../components';

const SeeDetailsRecipes: React.FC = () => {
  const [showDetails, setShowDetails] = React.useState(false);

  return (
    <SafeAreaView style={ss.container}>
      <Page>
        <Header>SeeDetails{'\n'}(mod-flex-mini-app recipe)</Header>
        <View style={ss.innerContainer}>
          <SeeDetails
            expanded={showDetails}
            hideText="Show Less"
            onToggle={() => setShowDetails(!showDetails)}
            showText="Show More"
            size={'small'}
            UNSAFE_style={ss.seeDetailsStyle}
            title_style={ss.seeDetailsTitleStyle}>
            <Body>Children of See Details.</Body>
          </SeeDetails>
        </View>
      </Page>
    </SafeAreaView>
  );
};

const ss = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.gray['100'],
    height: '15%',
  },

  innerContainer: {
    marginHorizontal: 16,
    padding: 8,
    justifyContent: 'flex-start',
  },
  seeDetailsStyle: {
    flex: 1,
    justifyContent: 'flex-end',
    alignItems: 'flex-end',
    marginBottom: -8,
    marginRight: -17,
  },
  seeDetailsTitleStyle: {
    fontFamily: 'Bogle-Regular',
    fontSize: 12,
    fontWeight: '400',
    color: colors.black,
    lineHeight: 15,
    marginRight: -4,
  },
});

export {SeeDetailsRecipes};
