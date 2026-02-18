import * as React from 'react';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Nudge';
import {fireEvent, render} from '@testing-library/react-native';
import {Icons} from '@walmart/gtp-shared-icons';

import {Button} from '../Button';
import {Nudge} from '../Nudge';

let mockFn: jest.Mock | (() => void);
beforeAll(() => {
  mockFn = jest.fn();
});
const titleText = 'Nudge without actions';
const contentText = `And they don't stop coming. Fed to the rules and I hit the ground
running. Didn't make sense not to`;
const action1 = 'Look away';
const _nudgeLeading = 'Nudge-leading';
const _nudgeClose = 'Nudge-close';
const _nudgeActions = 'Nudge-actions';
describe('Test ListItem', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('Nudge with all Props', async () => {
    const rootQueries = render(
      <Nudge
        title={titleText}
        onClose={() => mockFn()}
        leading={<Icons.EyeIcon size={24} />}
        actions={
          <Button variant="tertiary" onPress={mockFn}>
            {action1}
          </Button>
        }>
        {contentText}
      </Nudge>,
    );
    const leadingIcon = rootQueries.queryAllByTestId(_nudgeLeading);
    expect(leadingIcon.length).toEqual(1);
    const closeButton = rootQueries.queryAllByTestId(_nudgeClose);
    expect(closeButton.length).toEqual(1);
    const actions = await rootQueries.findByText(action1);
    expect(actions).toBeDefined();
    const content = await rootQueries.findByText(contentText);
    expect(content).toBeDefined();
    const title = await rootQueries.findByText(titleText);
    expect(title).toBeDefined();
  });

  test('Nudge with Title and Content only', async () => {
    const rootQueries = render(<Nudge title={titleText}>{contentText}</Nudge>);

    const leadingIcon = rootQueries.queryAllByTestId(_nudgeLeading);
    expect(leadingIcon.length).toEqual(0);
    const closeButton = rootQueries.queryAllByTestId(_nudgeClose);
    expect(closeButton.length).toEqual(0);
    const actions = rootQueries.queryAllByTestId(_nudgeActions);
    expect(actions.length).toEqual(0);

    const content = await rootQueries.findByText(contentText);
    expect(content).toBeDefined();
    const title = await rootQueries.findByText(titleText);
    expect(title).toBeDefined();
  });

  test('Nudge with Title, Content and Close Button', async () => {
    const rootQueries = render(
      <Nudge title={titleText} onClose={() => mockFn()}>
        {contentText}
      </Nudge>,
    );
    const leadingIcon = rootQueries.queryAllByTestId(_nudgeLeading);
    expect(leadingIcon.length).toEqual(0);
    const closeButton = rootQueries.queryAllByTestId(_nudgeClose);
    expect(closeButton.length).toEqual(1);
    const actions = rootQueries.queryAllByTestId(_nudgeActions);
    expect(actions.length).toEqual(0);
    const content = await rootQueries.findByText(contentText);
    expect(content).toBeDefined();
    const title = await rootQueries.findByText(titleText);
    expect(title).toBeDefined();
  });

  test('Nudge with Title, Content and Leading Icon', async () => {
    const rootQueries = render(
      <Nudge title={titleText} leading={<Icons.EyeIcon size={24} />}>
        {contentText}
      </Nudge>,
    );
    const leadingIcon = rootQueries.queryAllByTestId(_nudgeLeading);
    expect(leadingIcon.length).toEqual(1);
    const closeButton = rootQueries.queryAllByTestId(_nudgeClose);
    expect(closeButton.length).toEqual(0);
    const actions = rootQueries.queryAllByTestId(_nudgeActions);
    expect(actions.length).toEqual(0);
    const content = await rootQueries.findByText(contentText);
    expect(content).toBeDefined();
    const title = await rootQueries.findByText(titleText);
    expect(title).toBeDefined();
  });

  test('Nudge with Title, Content and Actions', async () => {
    const rootQueries = render(
      <Nudge
        title={titleText}
        actions={
          <Button variant="tertiary" onPress={mockFn}>
            {action1}
          </Button>
        }>
        {contentText}
      </Nudge>,
    );
    const leadingIcon = rootQueries.queryAllByTestId(_nudgeLeading);
    expect(leadingIcon.length).toEqual(0);
    const closeButton = rootQueries.queryAllByTestId(_nudgeClose);
    expect(closeButton.length).toEqual(0);
    const actions = rootQueries.queryAllByTestId(_nudgeActions);
    expect(actions.length).toEqual(1);
    const content = await rootQueries.findByText(contentText);
    expect(content).toBeDefined();
    const title = await rootQueries.findByText(titleText);
    expect(title).toBeDefined();
  });

  test('Nudge with Title, Content, Actions and Close', async () => {
    const rootQueries = render(
      <Nudge
        title={titleText}
        onClose={() => mockFn()}
        actions={
          <Button variant="tertiary" onPress={mockFn}>
            {action1}
          </Button>
        }>
        {contentText}
      </Nudge>,
    );
    const leadingIcon = rootQueries.queryAllByTestId(_nudgeLeading);
    expect(leadingIcon.length).toEqual(0);
    const closeButton = rootQueries.queryAllByTestId(_nudgeClose);
    expect(closeButton.length).toEqual(1);
    const actions = rootQueries.queryAllByTestId(_nudgeActions);
    expect(actions.length).toEqual(1);
    const content = await rootQueries.findByText(contentText);
    expect(content).toBeDefined();
    const title = await rootQueries.findByText(titleText);
    expect(title).toBeDefined();
  });

  test('Nudge with Title, Content, Actions and leading', async () => {
    const rootQueries = render(
      <Nudge
        title={titleText}
        leading={<Icons.EyeIcon size={24} />}
        actions={
          <Button variant="tertiary" onPress={mockFn}>
            {action1}
          </Button>
        }>
        {contentText}
      </Nudge>,
    );
    const leadingIcon = rootQueries.queryAllByTestId(_nudgeLeading);
    expect(leadingIcon.length).toEqual(1);
    const closeButton = rootQueries.queryAllByTestId(_nudgeClose);
    expect(closeButton.length).toEqual(0);
    const actions = rootQueries.queryAllByTestId(_nudgeActions);
    expect(actions.length).toEqual(1);
    const content = await rootQueries.findByText(contentText);
    expect(content).toBeDefined();
    const title = await rootQueries.findByText(titleText);
    expect(title).toBeDefined();
  });

  test('Nudge with Title, Content, Leading and Close Button', async () => {
    const rootQueries = render(
      <Nudge
        title={titleText}
        leading={<Icons.EyeIcon size={24} />}
        onClose={() => mockFn()}>
        {contentText}
      </Nudge>,
    );
    const leadingIcon = rootQueries.queryAllByTestId(_nudgeLeading);
    expect(leadingIcon.length).toEqual(1);
    const closeButton = rootQueries.queryAllByTestId(_nudgeClose);
    expect(closeButton.length).toEqual(1);
    const actions = rootQueries.queryAllByTestId(_nudgeActions);
    expect(actions.length).toEqual(0);
    const content = await rootQueries.findByText(contentText);
    expect(content).toBeDefined();
    const title = await rootQueries.findByText(titleText);
    expect(title).toBeDefined();
  });
});
describe('Test ListItem Actions', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('Test For Actions and Close button Press', async () => {
    const rootQueries = render(
      <Nudge
        title={titleText}
        onClose={() => mockFn()}
        leading={<Icons.EyeIcon size={24} />}
        actions={
          <Button variant="tertiary" onPress={mockFn}>
            {action1}
          </Button>
        }>
        {contentText}
      </Nudge>,
    );

    const closeButton = rootQueries.getByTestId(_nudgeClose);
    expect(closeButton).toBeDefined();

    const button = await rootQueries.findByText(action1);
    expect(button).toBeDefined();

    fireEvent.press(closeButton);
    expect(mockFn).toHaveBeenCalledTimes(1);
    fireEvent.press(button);
    expect(mockFn).toHaveBeenCalledTimes(2);
  });

  test('Test for Nudge style', async () => {
    const rootQueries = render(
      <Nudge
        title={titleText}
        onClose={() => mockFn()}
        leading={<Icons.EyeIcon size={24} />}
        actions={
          <Button variant="tertiary" onPress={mockFn}>
            {action1}
          </Button>
        }>
        {contentText}
      </Nudge>,
    );
    const leadingIcon = rootQueries.getByTestId(_nudgeLeading);
    expect(leadingIcon).toHaveStyle({
      marginRight: token.componentNudgeLeadingMarginEnd,
    });
    const closeButton = rootQueries.getByTestId(_nudgeClose);
    expect(closeButton).toHaveStyle({
      width: token.componentNudgeCloseButtonWidth,
      height: token.componentNudgeCloseButtonHeight,
      tintColor: token.componentNudgeCloseButtonIconColor,
      margin: token.componentNudgeCloseButtonMargin,
    });

    const actions = rootQueries.getByTestId(_nudgeActions);
    expect(actions).toHaveStyle({
      flexDirection: 'row',
      flexWrap: 'wrap',
      justifyContent: 'space-between',
      marginTop: token.componentNudgeActionContentMarginTop,
    });
  });
});
