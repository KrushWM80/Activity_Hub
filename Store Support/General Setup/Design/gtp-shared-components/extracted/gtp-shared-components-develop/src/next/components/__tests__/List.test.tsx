import * as React from 'react';
import {GestureResponderEvent, TextStyle} from 'react-native';

import * as buttonToken from '@livingdesign/tokens/dist/react-native/light/regular/components/Button';
import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/List';
import {fireEvent, render} from '@testing-library/react-native';
import {Icons} from '@walmart/gtp-shared-icons';

import {getFont} from '../../../theme/font';
import {loremIpsum} from '../../utils';
import {Button} from '../Button';
import {List} from '../List';
import {ListItem} from '../ListItem';

let mockFn: jest.Mock | ((event: GestureResponderEvent) => void);
beforeAll(() => {
  mockFn = jest.fn();
});
describe('Test List', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('Should render correctly.', async () => {
    const rootQueries = render(
      <List>
        <ListItem
          title="Truck"
          leading={<Icons.TruckIcon size={24} />}
          trailing={
            <Button variant={'tertiary'} onPress={mockFn}>
              Action1
            </Button>
          }>
          {loremIpsum(1)}
        </ListItem>
      </List>,
    );
    const leadingIcon = await rootQueries.findByTestId('ListItem-leading');
    expect(leadingIcon).toHaveStyle({
      height: 24,
      width: 24,
      marginRight: token.componentListItemLeadingMarginEnd,
    });
    const title = await rootQueries.findByTestId('ListItem-title');
    expect(title).toHaveStyle({
      fontWeight: `${token.componentListItemTitleAliasOptionsWeight}`,
    });
    const trailingButton = await rootQueries.findByTestId('ListItem-trailing');
    expect(trailingButton).toHaveStyle({
      justifyContent: 'center',
      alignItems: 'flex-end',
      marginLeft: token.componentListItemTrailingMarginStart,
    });

    const trailingAction = await rootQueries.findByText('Action1');
    fireEvent.press(trailingAction);
    expect(mockFn).toHaveBeenCalledTimes(1);
    expect(trailingAction).toHaveStyle({
      ...getFont(),
      textAlign: 'center',
      color:
        buttonToken.componentButtonTextLabelVariantTertiaryTextColorDefault,
      textDecorationLine:
        buttonToken.componentButtonTextLabelVariantTertiaryTextDecorationDefault,
      fontSize: buttonToken.componentButtonTextLabelSizeSmallFontSize,
      lineHeight: buttonToken.componentButtonTextLabelSizeSmallLineHeight,
    } as TextStyle);
  });
});
