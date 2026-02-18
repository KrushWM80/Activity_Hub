import * as React from 'react';
import {Header} from '../components';
import {tabs} from './screensFixtures';
import {View, ScrollView, StyleSheet} from 'react-native';
import {
  TabNavigation,
  TabNavigationItem,
  useSimpleReducer,
} from '@walmart/gtp-shared-components';
type TabState = {
  withLeadingTrailing: number;
  withLeading: number;
  withTrailing: number;
  labelOnly: number;
};
const initialState = {
  withLeadingTrailing: 0,
  withLeading: 0,
  withTrailing: 0,
  labelOnly: 0,
};
const TabNavigationOverview = () => {
  const [selectedTab, setSelectedTab] =
    useSimpleReducer<TabState>(initialState);
  type TabItem = {
    trailing?: React.ReactNode;
    label: string;
    leading?: React.ReactNode;
  };
  const renderNavigationItem = (item: TabItem, index: number, type: string) => {
    const {trailing, label, leading} = item;
    return (
      <TabNavigationItem
        key={index}
        testID={`TabItem_${index}`}
        isCurrent={selectedTab[type] === index}
        leading={leading}
        onPress={() => setSelectedTab(type, index)}
        trailing={trailing}>
        {label}
      </TabNavigationItem>
    );
  };
  const renderWithUnsafeStyleNavigationItem = (
    item: TabItem,
    index: number,
    type: string,
    tabCount: number,
  ) => {
    const {trailing, label, leading} = item;
    return (
      <TabNavigationItem
        key={index}
        UNSAFE_style={{minWidth: `${100 / tabCount}%`}}
        isCurrent={selectedTab[type] === index}
        leading={leading}
        onPress={() => setSelectedTab(type, index)}
        trailing={trailing}>
        {label}
      </TabNavigationItem>
    );
  };
  const renderWithTabCountNavigationItem = (
    item: TabItem,
    index: number,
    type: string,
    tabCount: number,
  ) => {
    const {trailing, label, leading} = item;
    return (
      <TabNavigationItem
        key={index}
        tabCount={tabCount}
        isCurrent={selectedTab[type] === index}
        leading={leading}
        onPress={() => setSelectedTab(type, index)}
        trailing={trailing}>
        {label}
      </TabNavigationItem>
    );
  };
  return (
    <ScrollView>
      <Header>Tabs - with Leading Trailing</Header>
      <TabNavigation>
        {tabs.withLeadingTrailing.map((item, index) =>
          renderNavigationItem(item, index, 'withLeadingTrailing'),
        )}
      </TabNavigation>
      <Header>Tabs - Leading</Header>
      <TabNavigation>
        {tabs.withLeading.map((item, index) =>
          renderNavigationItem(item, index, 'withLeading'),
        )}
      </TabNavigation>
      <Header>Tabs - Trailing</Header>
      <TabNavigation>
        {tabs.withTrailing.map((item, index) =>
          renderNavigationItem(item, index, 'withTrailing'),
        )}
      </TabNavigation>
      <Header>Tabs - Label and Scroll</Header>
      <TabNavigation>
        {tabs.labelOnly.map((item, index) =>
          renderNavigationItem(item, index, 'labelOnly'),
        )}
      </TabNavigation>
      <Header>Tabs TabNavigationItem Only- with TabCount</Header>
      <View>
        <ScrollView contentContainerStyle={ss.contentContainerStyle} horizontal>
          {tabs.withLeading.map((item, index) =>
            renderWithTabCountNavigationItem(
              item,
              index,
              'withLeading',
              tabs.withLeading.length,
            ),
          )}
        </ScrollView>
      </View>
      <Header>
        Tabs TabNavigationItem Only- with TabCount and UNSAFE_style
      </Header>
      <View>
        <ScrollView contentContainerStyle={ss.contentContainerStyle} horizontal>
          {tabs.withLeadingTrailing.map((item, index) =>
            renderWithUnsafeStyleNavigationItem(
              item,
              index,
              'withLeadingTrailing',
              tabs.withLeadingTrailing.length,
            ),
          )}
        </ScrollView>
      </View>
    </ScrollView>
  );
};
const ss = StyleSheet.create({
  contentContainerStyle: {flexGrow: 1},
});
export {TabNavigationOverview};
