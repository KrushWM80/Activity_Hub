import * as React from 'react';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/TabNavigation';
import {fireEvent, render} from '@testing-library/react-native';
import {Icons} from '@walmart/gtp-shared-icons';

import {iconSizes, IconSizesKey} from '../../utils';
import {Badge} from '../Badge';
import {TabNavigation} from '../TabNavigation';
import {TabNavigationItem} from '../TabNavigationItem';

let mockFn: jest.Mock | (() => void);
beforeAll(() => {
  mockFn = jest.fn();
});
const tabLabel = 'Tab';
const leading = <Icons.BoxIcon />;
const trailing = (
  <Badge color="blue" UNSAFE_style={{marginLeft: 8}}>
    10
  </Badge>
);

describe('Test TabNavigation', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('TabNavigation with all Props', async () => {
    const rootQueries = render(
      <TabNavigation>
        <TabNavigationItem
          leading={leading}
          trailing={trailing}
          onPress={mockFn}>
          {tabLabel}
        </TabNavigationItem>
      </TabNavigation>,
    );
    const leadingIcon = rootQueries.getByTestId('BoxIcon');
    expect(leadingIcon).toHaveStyle({
      marginRight: token.componentTabNavigationItemLeadingIconMarginEnd, //8
      width:
        iconSizes[
          token.componentTabNavigationItemLeadingIconIconSize as IconSizesKey
        ], //small
      height:
        iconSizes[
          token.componentTabNavigationItemLeadingIconIconSize as IconSizesKey
        ], //small
      tintColor: token.componentTabNavigationItemLeadingIconIconColor, //#000
    });
    const tabItem = rootQueries.getByTestId('TabNavigationItem_0');
    fireEvent.press(tabItem);
    expect(mockFn).toHaveBeenCalledTimes(1);
    const label = rootQueries.getByText('Tab');
    expect(label).toHaveStyle({
      fontSize: token.componentTabNavigationItemTextLabelFontSize, //14
      lineHeight: token.componentTabNavigationItemTextLabelLineHeight, //48
      color: token.componentTabNavigationItemTextLabelTextColor, //"#2e2f32"
    });
    const trailingBadge = rootQueries.getByTestId('Badge');
    expect(trailingBadge).toHaveStyle({marginLeft: 8});
  });

  test('TabNavigation with Leading', async () => {
    const rootQueries = render(
      <TabNavigation>
        <TabNavigationItem leading={leading} onPress={mockFn}>
          {tabLabel}
        </TabNavigationItem>
      </TabNavigation>,
    );
    const leadingIcon = rootQueries.queryAllByTestId('BoxIcon');
    expect(leadingIcon.length).toEqual(1);

    const trailingBadge = rootQueries.queryAllByTestId('Badge');
    expect(trailingBadge.length).toEqual(0);
  });

  test('TabNavigation with Trailing', async () => {
    const rootQueries = render(
      <TabNavigation>
        <TabNavigationItem trailing={trailing} onPress={mockFn}>
          {tabLabel}
        </TabNavigationItem>
      </TabNavigation>,
    );
    const leadingIcon = rootQueries.queryAllByTestId('BoxIcon');
    expect(leadingIcon.length).toEqual(0);

    const trailingBadge = rootQueries.queryAllByTestId('Badge');
    expect(trailingBadge.length).toEqual(1);
  });

  test('TabNavigation with Label', async () => {
    const rootQueries = render(
      <TabNavigation>
        <TabNavigationItem isCurrent={true} onPress={mockFn}>
          {tabLabel}
        </TabNavigationItem>
      </TabNavigation>,
    );
    const selectedIndicator = rootQueries.getByTestId(
      'TabNavigationItem-indicator',
    );
    expect(selectedIndicator).toHaveStyle({
      position: 'absolute',
      height: token.componentTabNavigationItemIndicatorHeight, //3
      borderTopLeftRadius:
        token.componentTabNavigationItemIndicatorBorderRadiusTopStart, //3
      borderTopRightRadius:
        token.componentTabNavigationItemIndicatorBorderRadiusTopEnd, //3
      backgroundColor:
        token.componentTabNavigationItemIndicatorStateIsCurrentBackgroundColor, //"#0071dc"
      left: token.componentTabNavigationItemIndicatorOffsetStart, //4
      right: token.componentTabNavigationItemIndicatorOffsetEnd, //4
      bottom: token.componentTabNavigationItemIndicatorOffsetBottom, //1});
    });
  });
});
