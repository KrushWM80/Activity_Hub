import * as React from 'react';
import {ScrollView, StyleProp, StyleSheet, ViewStyle} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/TabNavigation';
import flattenChildren from 'react-keyed-flatten-children';

import type {CommonViewProps} from '../types/ComponentTypes';
import {a11yRole} from '../utils';

// ---------------
// Props
// ---------------
export type TabNavigationProps = CommonViewProps & {
  /**
   * The content for the tab navigation.
   */
  children: React.ReactNode;
  /**
   * If provided, the `style` to provide to the root element. @note This property is prefixed with
   * `UNSAFE` as its use often results in unintended side effects.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
};

/**
 * Tab Navigation allows for page-level navigation between sets of content, with a selected state, typically used at the top of the screen.
 *
 * ## Usage
 * ```js
 * import {TabNavigation,TabNavigationItem,Icons,Badge} from '@walmart/gtp-shared-components';
 *
 * const [currentTab, setCurrentTab] = React.useState(1);
 *
 * <TabNavigation>
 *   <TabNavigationItem
 *     leading={<Icons.CartIcon />}
 *     isCurrent={currentTab===0}
 *     onPress={() => setCurrentTab(0)}
 *     trailing={<Badge color="blue" UNSAFE_style={styles.badge}>10</Badge>}>
 *     {"One"}
 *   </TabNavigationItem>
 *   <TabNavigationItem
 *     isCurrent={currentTab===1}
 *     leading={<Icons.CartIcon />}
 *     onPress={() => setCurrentTab(1)}
 *     trailing={<Badge color="blue" UNSAFE_style={styles.badge}>10</Badge>}>
 *     {"Two"}
 *   </TabNavigationItem>
 *   <TabNavigationItem
 *     leading={<Icons.CartIcon />}
 *     isCurrent={currentTab===2}
 *     onPress={() => setCurrentTab(2)}
 *     trailing={<Badge color="blue" UNSAFE_style={styles.badge}>10</Badge>}>
 *     {"Three"}
 *   </TabNavigationItem>
 * </TabNavigation>
 * ```
 */

const TabNavigation: React.FC<TabNavigationProps> = (props) => {
  const {children, UNSAFE_style = {}, ...rest} = props;
  const kids = flattenChildren(children);
  const tabCount = React.Children.count(kids);

  return (
    <ScrollView
      accessibilityRole={a11yRole('tablist')}
      testID={TabNavigation.displayName}
      horizontal
      bounces={false}
      scrollsToTop={false}
      showsHorizontalScrollIndicator={false}
      showsVerticalScrollIndicator={false}
      style={[ss.container, UNSAFE_style]}
      contentContainerStyle={ss.contentContainer}
      {...rest}>
      {kids.map((kid, index) => {
        return React.cloneElement(kid as React.ReactElement, {
          index,
          tabCount: tabCount,
        });
      })}
    </ScrollView>
  );
};

// ---------------
// Styles
// ---------------
const ss = StyleSheet.create({
  container: {
    width: '100%',
    flexGrow: 0,
    //adding +1 to show borderBottom
    height: token.componentTabNavigationItemLineHeight + 1,
    borderBottomColor: token.componentTabNavigationContainerBorderColorBottom,
    borderBottomWidth: token.componentTabNavigationContainerBorderWidthBottom,
  },
  contentContainer: {
    flexGrow: 1,
    height: token.componentTabNavigationItemLineHeight,
  },
});

TabNavigation.displayName = 'TabNavigation';
export {TabNavigation};
