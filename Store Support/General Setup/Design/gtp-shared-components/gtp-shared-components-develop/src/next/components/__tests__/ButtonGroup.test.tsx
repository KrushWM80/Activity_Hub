import * as React from 'react';

import {render, screen} from '@testing-library/react-native';

import {Button} from '../Button';
import {ButtonGroup} from '../ButtonGroup';

const buttonPress = jest.fn();
describe('Test ButtonGroup match snapshot correctly', () => {
  test('with maxWidth', async () => {
    render(
      <ButtonGroup UNSAFE_style={{maxWidth: 100}}>
        <Button variant="primary" onPress={buttonPress}>
          Continue
        </Button>
      </ButtonGroup>,
    );

    expect(screen.toJSON()).toMatchSnapshot();
  });
  test(' without UNSAFE_style', async () => {
    render(
      <ButtonGroup>
        <Button variant="tertiary" onPress={buttonPress}>
          Cancel
        </Button>
        <Button variant="primary" onPress={buttonPress}>
          Continue
        </Button>
      </ButtonGroup>,
    );

    expect(screen.toJSON()).toMatchSnapshot();
  });
  test('with three buttons ', async () => {
    render(
      <ButtonGroup>
        <Button variant="tertiary" onPress={buttonPress}>
          yes delete 1 message
        </Button>
        <Button variant="tertiary" onPress={buttonPress}>
          Cancel
        </Button>
        <Button variant="primary" onPress={buttonPress}>
          Continue
        </Button>
      </ButtonGroup>,
    );

    expect(screen.toJSON()).toMatchSnapshot();
  });
});
