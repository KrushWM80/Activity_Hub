import * as React from 'react';
import {
  FlexStyle,
  GestureResponderEvent,
  LayoutChangeEvent,
  LayoutRectangle,
  Pressable,
  StyleProp,
  StyleSheet,
  TextStyle,
  useWindowDimensions,
  View,
  ViewStyle,
} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/TabNavigation';
import * as globalToken from '@livingdesign/tokens/dist/react-native/light/regular/globals';
import {IconSize} from '@walmart/gtp-shared-icons';

import {getFont, Weights} from '../../theme/font';
import type {CommonViewProps} from '../types/ComponentTypes';
import {a11yRole, calculatePercentageOf} from '../utils';

import {
  _LeadingTrailing as _Leading,
  _LeadingTrailing as _Trailing,
} from './_LeadingTrailing';
import {Body} from './Body';

// ---------------
// Props
// ---------------
export type TabNavigationItemProps = CommonViewProps & {
  /**
   * The tab Navigation item index.
   */
  index?: number;
  /**
   * The content for the tab navigation item.
   */
  children: React.ReactNode;
  /**
   * If the tab navigation item represents the current page.
   * @default false
   */
  isCurrent?: boolean;
  /**
   * The leading icon for tab navigation item.
   * typically an icon
   */
  leading?: React.ReactNode;
  /**
   * The callback fired when the tab navigation item is clicked.
   */
  onPress?: (event: GestureResponderEvent) => void;
  /**
   * The trailing content for the tab navigation item.
   * typically a badge
   */
  trailing?: React.ReactNode;
  /**
   * If provided, the `style` to provide to the root element. @note This property is prefixed with
   * `UNSAFE` as its use often results in unintended side effects.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
  //******************** NON LD PROPS *****************//
  /**
   * @internal
   * total number of tabs.
   *
   */
  tabCount?: number;
};

/**
 * Suggested way Use TabNavigationItem inside the TabNavigation
 *
 * if you are using a plain TabNavigationItem you must pass index and tabCount
 * (Total number of tabs) so that it will automatically allocate the width
 * to the tabs
 *
 * ## Usage
 * ```js
 * import {Badge, TabNavigationItem} from '@walmart/gtp-shared-components`;
 *
 * <TabNavigationItem isCurrent trailing={<Badge color="blue">10</Badge>}>
 *   {"One"}
 * </TabNavigationItem>
 * ```
 */
const TabNavigationItem: React.FC<TabNavigationItemProps> = (props) => {
  const {
    children,
    index,
    isCurrent = false,
    leading,
    onPress,
    trailing,
    tabCount,
    UNSAFE_style = {},
    ...rest
  } = props;

  const {width} = useWindowDimensions();
  const deviceWidth = process.env.STYLEGUIDIST_ENV ? 380 : width;
  //Device screen width(100%) can be divided into different percentages based on number of tabs (min 20%)
  const percentage = tabCount && 100 / tabCount;

  const [tabItemWidth, setTabItemWidth] = React.useState({minWidth: 0});

  const [tabItemLayout, setTabItemLayout] = React.useState<
    LayoutRectangle | undefined
  >();

  const minWidth = calculatePercentageOf(
    deviceWidth,
    percentage && percentage <= 20 ? 20 : percentage,
  );

  React.useEffect(() => {
    setTabItemWidth({minWidth});
  }, [deviceWidth, percentage, minWidth]);

  React.useEffect(() => {
    if (tabItemLayout && tabCount) {
      //if tabItem width is greater then minWidth then it will take it as a the tab width otherWise suggestedWidth
      if (
        (index !== tabCount - 1 &&
          tabItemLayout?.width !== 0 &&
          tabItemLayout?.width > tabItemWidth?.minWidth) ||
        (deviceWidth > globalToken.sizeBreakpointMedium && percentage! <= 20)
      ) {
        setTabItemWidth({minWidth: tabItemLayout?.width});
      } else if (tabItemLayout?.width !== 0 && index !== tabCount - 1) {
        setTabItemWidth({minWidth: tabItemWidth?.minWidth});
      } else if (index === tabCount - 1) {
        //setting the minWidth for the last tab item.on rotation of device it will take the default minWidth
        setTabItemWidth({minWidth});
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [tabItemLayout]);
  // ---------------
  // Rendering
  // ---------------
  const renderLeading = (node: React.ReactNode) => {
    return (
      <_Leading
        node={node}
        iconProps={{
          UNSAFE_style: {
            marginRight: token.componentTabNavigationItemLeadingIconMarginEnd, //8
          },
          size: token.componentTabNavigationItemLeadingIconIconSize as IconSize,
          color: token.componentTabNavigationItemLeadingIconIconColor, //#000
        }}
      />
    );
  };

  const renderTrailing = (node: React.ReactNode) => {
    return (
      <_Trailing
        node={node}
        iconProps={{
          UNSAFE_style: {
            marginLeft: token.componentTabNavigationItemTrailingMarginStart, // 8
          },
        }}
      />
    );
  };

  return (
    <View
      accessible={true}
      onLayout={(event: LayoutChangeEvent) => {
        const layout = event.nativeEvent.layout;
        setTabItemLayout(layout);
      }}
      style={[ss(isCurrent).container, tabItemWidth, UNSAFE_style]}>
      <Pressable
        testID={
          rest.testID
            ? rest.testID
            : `${TabNavigationItem.displayName}_${index}`
        }
        accessibilityRole={a11yRole('tab')}
        accessibilityState={{selected: isCurrent}}
        style={ss(isCurrent).itemContainer}
        android_ripple={ss(isCurrent).itemActive}
        onPress={onPress}
        {...rest}>
        {leading && renderLeading(leading)}
        <Body UNSAFE_style={[ss(isCurrent).label]}>{children}</Body>
        {trailing && renderTrailing(trailing)}
      </Pressable>
      <View
        testID={TabNavigationItem.displayName + '-indicator'}
        style={ss(isCurrent).indicator}
      />
    </View>
  );
};

// ---------------
// Styles
// ---------------
const ss = (isCurrent: boolean) => {
  const labelWeight = isCurrent
    ? token.componentTabNavigationItemTextLabelStateIsCurrentFontWeight //700
    : token.componentTabNavigationItemTextLabelFontWeight; //400
  const indicatorBackground = isCurrent
    ? token.componentTabNavigationItemIndicatorStateIsCurrentBackgroundColor //"#0071dc"
    : token.componentTabNavigationItemIndicatorBackgroundColorDefault; //transparent
  return StyleSheet.create({
    container: {
      flex: 1,
      height: token.componentTabNavigationItemLineHeight, //48
      backgroundColor: token.componentTabNavigationItemBackgroundColorDefault, //fff
      borderBottomColor: token.componentTabNavigationItemBorderColorBottom,
      borderBottomWidth: token.componentTabNavigationItemBorderWidthBottom,
    },
    itemContainer: {
      paddingHorizontal: token.componentTabNavigationItemPaddingHorizontal, //16
      flexDirection: 'row',
      justifyContent:
        token.componentTabNavigationItemAlignHorizontal as Extract<
          //Cory, wrong TS type here
          FlexStyle,
          'justifyContent'
        >, //"center"
      alignItems: token.componentTabNavigationItemAlignVertical as Extract<
        //Cory, wrong TS type here
        FlexStyle,
        'alignItems'
      >, //'center',
    },
    itemActive: {
      color: token.componentTabNavigationItemBackgroundColorActive, //"#e3e4e5"
    },
    indicator: {
      position: 'absolute',
      height: token.componentTabNavigationItemIndicatorHeight, //3
      borderTopLeftRadius:
        token.componentTabNavigationItemIndicatorBorderRadiusTopStart, //1000
      borderTopRightRadius:
        token.componentTabNavigationItemIndicatorBorderRadiusTopEnd, //1000
      backgroundColor: indicatorBackground,
      left: token.componentTabNavigationItemIndicatorOffsetStart, //4
      right: token.componentTabNavigationItemIndicatorOffsetEnd, //4
      bottom: token.componentTabNavigationItemIndicatorOffsetBottom, //1
    },
    label: {
      ...getFont(labelWeight.toString() as Weights), //400
      fontSize: token.componentTabNavigationItemTextLabelFontSize, //14
      lineHeight: token.componentTabNavigationItemTextLabelLineHeight, //48
      color: token.componentTabNavigationItemTextLabelTextColor, //"#2e2f32"
    } as TextStyle,
  });
};

TabNavigationItem.displayName = 'TabNavigationItem';
export {TabNavigationItem};
