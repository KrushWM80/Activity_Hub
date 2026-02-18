import * as React from 'react';

import {fireEvent, render, screen} from '@testing-library/react-native';
import {Icons} from '@walmart/gtp-shared-icons';

import {Body} from '../Body';
import {Collapse} from '../Collapse';

const toggle = jest.fn();
describe('Collapse', () => {
  test('renders Collapse before Expand', () => {
    render(
      <Collapse
        title="Collapse with Subtitle and Icon"
        onToggle={toggle}
        dividerTop>
        <Body>Collapse content appears underneath the toggle area.</Body>
      </Collapse>,
    );
    const element = screen.getByTestId('Collapse');
    expect(element).toBeDefined();
    const details = screen.queryAllByTestId('Collapse-details');
    expect(details.length).toEqual(0);
    const trigger = screen.getByTestId('Collapse-trigger');
    fireEvent(trigger, 'press');
    expect(toggle).toHaveBeenCalledTimes(1);
    const dividerTop = screen.queryAllByTestId('Collapse-dividerTop');
    expect(dividerTop).toBeDefined();
  });
  test('renders Collapse after Expand', () => {
    render(
      <Collapse
        title="Collapse with Subtitle and Icon"
        onToggle={toggle}
        dividerBottom
        icon={<Icons.MoneyCircleIcon />}
        expanded>
        <Body>Collapse content appears underneath the toggle area.</Body>
      </Collapse>,
    );
    const element = screen.getByTestId('Collapse');
    expect(element).toBeDefined();
    const details = screen.queryAllByTestId('Collapse-details');
    expect(details.length).toEqual(1);
    const icon = screen.getByTestId('MoneyCircleIcon');
    expect(icon).toBeDefined();
    const dividerBottom = screen.queryAllByTestId('Collapse-dividerBottom');
    expect(dividerBottom).toBeDefined();
  });
});
