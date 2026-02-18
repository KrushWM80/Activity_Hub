import * as React from 'react';

import {render, screen} from '@testing-library/react-native';

import {Body} from '../Body';
import {SeeDetails} from '../SeeDetails';

const toggle = jest.fn();
describe('SeeDetails', () => {
  test('renders SeeDetails before Expand', () => {
    render(
      <SeeDetails onToggle={toggle}>
        <Body>SeeDetails content appears underneath the toggle area.</Body>
      </SeeDetails>,
    );
    const element = screen.getByTestId('SeeDetails');
    expect(element).toBeDefined();
    const details = screen.queryAllByTestId('SeeDetails-details');
    expect(details.length).toEqual(0);
    const showText = screen.getByTestId('SeeDetails-title');
    expect(showText.children[0]).toEqual('See Details');
  });
  test('renders SeeDetails after Expand', () => {
    render(
      <SeeDetails onToggle={toggle} expanded>
        <Body>Collapse content appears underneath the toggle area.</Body>
      </SeeDetails>,
    );
    const element = screen.getByTestId('SeeDetails');
    expect(element).toBeDefined();
    const details = screen.queryAllByTestId('SeeDetails-details');
    expect(details.length).toEqual(1);
    const hideText = screen.getByTestId('SeeDetails-title');
    expect(hideText.children[0]).toEqual('Hide Details');
  });
  test('renders SeeDetails with custom showText ', () => {
    render(
      <SeeDetails
        onToggle={toggle}
        dividerTop
        showText="Show My Content"
        hideText="Hide My Content">
        <Body>Collapse content appears underneath the toggle area.</Body>
      </SeeDetails>,
    );
    const element = screen.getByTestId('SeeDetails');
    expect(element).toBeDefined();
    const showText = screen.getByTestId('SeeDetails-title');
    expect(showText.children[0]).toEqual('Show My Content');
    const dividerTop = screen.queryAllByTestId('SeeDetails-dividerTop');
    expect(dividerTop).toBeDefined();
  });
  test('renders SeeDetails with custom HideText', () => {
    render(
      <SeeDetails
        onToggle={toggle}
        showText="Show My Content"
        expanded
        dividerBottom
        hideText="Hide My Content">
        <Body>Collapse content appears underneath the toggle area.</Body>
      </SeeDetails>,
    );
    const element = screen.getByTestId('SeeDetails');
    expect(element).toBeDefined();
    const details = screen.queryAllByTestId('SeeDetails-details');
    expect(details.length).toEqual(1);
    const hideText = screen.getByTestId('SeeDetails-title');
    expect(hideText.children[0]).toEqual('Hide My Content');
    const dividerBottom = screen.queryAllByTestId('SeeDetails-dividerBottom');
    expect(dividerBottom).toBeDefined();
  });
});
