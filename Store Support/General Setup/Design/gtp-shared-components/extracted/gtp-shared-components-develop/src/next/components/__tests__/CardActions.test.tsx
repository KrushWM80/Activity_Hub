import * as React from 'react';

import {render} from '@testing-library/react-native';

import {Button} from '../Button';
import {ButtonGroup} from '../ButtonGroup';
import {CardActions} from '../CardActions';

jest.useFakeTimers({legacyFakeTimers: true});

describe('Testing CardMedia', () => {
  it('should display correctly', () => {
    const component = render(
      <CardActions>
        <ButtonGroup>
          <Button variant="tertiary" onPress={() => {}}>
            Action1
          </Button>
          <Button variant="primary" onPress={() => {}}>
            Action2
          </Button>
        </ButtonGroup>
      </CardActions>,
    );
    expect(component).toMatchSnapshot();
  });
});
