import * as React from 'react';
import {TabNavigation, TabNavigationItem} from '@walmart/gtp-shared-components';
import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/TabNavigation.js';

import isNil from 'lodash/isNil';
import {StyleSheet, View, Text} from 'react-native';

export type ScreenProps = {
  name: string;
};

// Code provided to reporter of CEEMP-2840

const Screen: React.FC<ScreenProps> = ({name}: {name: string}) => (
  <View style={ss.screenContainer}>
    <Text style={ss.screenText}>{name}</Text>
  </View>
);

interface TabData {
  title: string;
  screen: React.ReactElement;
  telemetryKey?: string;
}

const tabs = [
  {title: 'oneOfTheTabLarge', screen: <Screen name="Pane One" />},
  {title: 'two', screen: <Screen name="Pane Two" />},
  {title: 'three', screen: <Screen name="Pane Three" />},
  {title: 'four', screen: <Screen name="Pane Four" />},
] as TabData[];

const TabNavigationRecipes = () => {
  const [selectedIndex, setSelectedIndex] = React.useState(0);
  const showTabs = tabs?.length === 1 ? false : true;

  const onTabNavSelect = (index: number) => {
    setSelectedIndex(index);
  };

  const renderTab = (title: string, index: number) => {
    return (
      <TabNavigationItem
        key={index}
        isCurrent={selectedIndex === index}
        onPress={() => onTabNavSelect(index)}>
        {title}
      </TabNavigationItem>
    );
  };

  const DisplayPane = tabs?.[selectedIndex].screen!;

  return !isNil(tabs) && showTabs ? (
    <View style={ss.container}>
      <TabNavigation>
        {tabs.map((item, index) => {
          const {title} = item;
          return renderTab(title, index);
        })}
      </TabNavigation>
      {React.cloneElement(DisplayPane)}
    </View>
  ) : null;
};

const ss = StyleSheet.create({
  screenContainer: {
    height: '60%',
    borderRadius: 16,
    borderWidth: 1,
    justifyContent: 'center',
    marginHorizontal: 20,
    marginTop: 20,
    borderColor:
      token.componentTabNavigationItemIndicatorStateIsCurrentBackgroundColor,
  },
  container: {flex: 1, backgroundColor: 'white'},
  screenText: {
    textAlign: 'center',
    fontSize: 22,
    color:
      token.componentTabNavigationItemIndicatorStateIsCurrentBackgroundColor,
  },
});

export {TabNavigationRecipes};
