---
to: example/src/screens/<%= componentName %>Screen.tsx
unless_exists: true
---

import * as React from 'react';
import {SafeAreaView, View, StyleSheet} from 'react-native';
import {colors, <%= componentName %>} from '@walmart/gtp-shared-components';
import {Header, Page} from '../components';

const <%= componentName %>Screen: React.FC = () => {
  return (
    <SafeAreaView style={ss.container}>
      <Page>
        {/* COMPONENT TEMPLATE */}

        <View key={'Template'}>
          <Header><%= componentName %></Header>

          <View style={ss.innerContainer}>
            <<%= componentName %> size={'small'} />
          </View>
        </View>
      </Page>
    </SafeAreaView>
  );
};

const ss = StyleSheet.create({
  container: {
    backgroundColor: colors.white,
    flex: 1,
    paddingBottom: 18,
  },

  innerContainer: {
    backgroundColor: colors.gray['5'],
    borderWidth: 1,
    borderBottomLeftRadius: 12,
    borderBottomRightRadius: 12,
    borderColor: colors.gray['10'],
  },
  spacer: {
    height: 8,
  },
});

export {<%= componentName %>Screen};
