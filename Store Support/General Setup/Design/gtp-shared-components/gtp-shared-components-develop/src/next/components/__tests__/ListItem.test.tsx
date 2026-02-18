import * as React from 'react';
import {GestureResponderEvent} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/List';
import {fireEvent, render} from '@testing-library/react-native';
import {Icons} from '@walmart/gtp-shared-icons';

import {loremIpsum} from '../../utils';
import {Button} from '../Button';
import {IconButton} from '../IconButton';
import {ListItem} from '../ListItem';

let mockFn: jest.Mock | ((event: GestureResponderEvent) => void);
const _listItemLeading = 'ListItem-leading';
const _listItemTitle = 'ListItem-title';
const _listItemTrailing = 'ListItem-trailing';
const _listItemContent = 'ListItem-content';
beforeAll(() => {
  mockFn = jest.fn();
});
describe('Test ListItem', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('ListItem with Content only', async () => {
    const rootQueries = render(<ListItem>{loremIpsum(1)}</ListItem>);
    const leadingIcon = rootQueries.queryAllByTestId(_listItemLeading);
    expect(leadingIcon.length).toEqual(0);
    const title = rootQueries.queryAllByTestId(_listItemTitle);
    expect(title.length).toEqual(0);
    const trailingButton = rootQueries.queryAllByTestId(_listItemTrailing);
    expect(trailingButton.length).toEqual(0);
    const content = rootQueries.queryAllByTestId(_listItemContent);
    expect(content.length).toEqual(1);
  });
  test('ListItem with  Content & Leading', async () => {
    const rootQueries = render(
      <ListItem leading={<Icons.InfoCircleIcon />}>{loremIpsum(1)}</ListItem>,
    );
    const leadingIcon = rootQueries.queryAllByTestId(_listItemLeading);
    expect(leadingIcon.length).toEqual(1);
    const title = rootQueries.queryAllByTestId(_listItemTitle);
    expect(title.length).toEqual(0);
    const trailingButton = rootQueries.queryAllByTestId(_listItemTrailing);
    expect(trailingButton.length).toEqual(0);
    const content = rootQueries.queryAllByTestId(_listItemContent);
    expect(content.length).toEqual(1);
  });
  test('ListItem with  Content & Trailing', async () => {
    const rootQueries = render(
      <ListItem trailing={<Button onPress={mockFn}>Action</Button>}>
        {loremIpsum(1)}
      </ListItem>,
    );
    const leadingIcon = rootQueries.queryAllByTestId(_listItemLeading);
    expect(leadingIcon.length).toEqual(0);
    const title = rootQueries.queryAllByTestId(_listItemTitle);
    expect(title.length).toEqual(0);
    const trailingButton = rootQueries.queryAllByTestId(_listItemTrailing);
    expect(trailingButton.length).toEqual(1);
    const content = rootQueries.queryAllByTestId(_listItemContent);
    expect(content.length).toEqual(1);
  });
  test('ListItem with Title and Content', async () => {
    const rootQueries = render(
      <ListItem title="Truck">{loremIpsum(1)}</ListItem>,
    );
    const leadingIcon = rootQueries.queryAllByTestId(_listItemLeading);
    expect(leadingIcon.length).toEqual(0);
    const title = rootQueries.queryAllByTestId(_listItemTitle);
    expect(title.length).toEqual(1);
    const trailingButton = rootQueries.queryAllByTestId(_listItemTrailing);
    expect(trailingButton.length).toEqual(0);
    const content = rootQueries.queryAllByTestId(_listItemContent);
    expect(content.length).toEqual(1);
  });
  test('ListItem with Title, Content & Leading', async () => {
    const rootQueries = render(
      <ListItem title="Truck" leading={<Icons.InfoCircleIcon />}>
        {loremIpsum(1)}
      </ListItem>,
    );
    const leadingIcon = rootQueries.queryAllByTestId(_listItemLeading);
    expect(leadingIcon.length).toEqual(1);
    const title = rootQueries.queryAllByTestId(_listItemTitle);
    expect(title.length).toEqual(1);
    const trailingButton = rootQueries.queryAllByTestId(_listItemTrailing);
    expect(trailingButton.length).toEqual(0);
    const content = rootQueries.queryAllByTestId(_listItemContent);
    expect(content.length).toEqual(1);
  });
  test('ListItem with Title, Content & Trailing', async () => {
    const rootQueries = render(
      <ListItem
        title="Truck"
        trailing={<Button onPress={mockFn}>Action</Button>}>
        {loremIpsum(1)}
      </ListItem>,
    );
    const leadingIcon = rootQueries.queryAllByTestId(_listItemLeading);
    expect(leadingIcon.length).toEqual(0);
    const title = rootQueries.queryAllByTestId(_listItemTitle);
    expect(title.length).toEqual(1);
    const trailingButton = rootQueries.queryAllByTestId(_listItemTrailing);
    expect(trailingButton.length).toEqual(1);
    const content = rootQueries.queryAllByTestId(_listItemContent);
    expect(content.length).toEqual(1);
  });
  test('ListItem with Title, Content, Leading & Trailing', async () => {
    const rootQueries = render(
      <ListItem
        title="Truck"
        leading={<Icons.InfoCircleIcon />}
        trailing={<Button onPress={mockFn}>Action</Button>}>
        {loremIpsum(1)}
      </ListItem>,
    );
    const leadingIcon = rootQueries.queryAllByTestId(_listItemLeading);
    expect(leadingIcon.length).toEqual(1);
    const title = rootQueries.queryAllByTestId(_listItemTitle);
    expect(title.length).toEqual(1);
    const trailingButton = rootQueries.queryAllByTestId(_listItemTrailing);
    expect(trailingButton.length).toEqual(1);
    const content = rootQueries.queryAllByTestId(_listItemContent);
    expect(content.length).toEqual(1);
  });
  test('ListItem render correctly and perform action', async () => {
    const rootQueries = render(
      <ListItem
        title="Truck"
        leading={<Icons.TruckIcon size={24} />}
        trailing={
          <IconButton
            children={<Icons.ChevronRightIcon />}
            size="small"
            onPress={mockFn}
          />
        }>
        {loremIpsum(1)}
      </ListItem>,
    );
    const leadingIcon = await rootQueries.findByTestId(_listItemLeading);
    expect(leadingIcon).toHaveStyle({
      height: 24,
      width: 24,
      marginRight: token.componentListItemLeadingMarginRight,
    });
    const title = await rootQueries.findByTestId(_listItemTitle);
    expect(title).toHaveStyle({
      fontWeight: `${token.componentListItemTitleAliasOptionsWeight}`,
    });
    const trailingButton = await rootQueries.findByTestId(_listItemTrailing);
    expect(trailingButton).toHaveStyle({
      justifyContent: 'center',
      alignItems: 'flex-end',
      marginLeft: token.componentListItemTrailingMarginLeft,
    });
    const trailingAction = await rootQueries.findByTestId('ChevronRightIcon');
    fireEvent.press(trailingAction);
    expect(mockFn).toHaveBeenCalledTimes(1);
    expect(trailingAction).toHaveStyle({
      height: 16,
      width: 16,
      tintColor: '#000',
    });
  });
});
