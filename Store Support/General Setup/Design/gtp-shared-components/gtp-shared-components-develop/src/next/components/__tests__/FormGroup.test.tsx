import * as React from 'react';

import * as formToken from '@livingdesign/tokens/dist/react-native/light/regular/components/Form';
import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/FormGroup';
import {render} from '@testing-library/react-native';

import {loremIpsum} from '../../utils';
import {Checkbox} from '../Checkbox';
import {FormGroup} from '../FormGroup';
import {Radio} from '../Radio';

describe('Test FormGroup', () => {
  test('FormGroup with CheckBox', async () => {
    const rootQueries = render(
      <FormGroup>
        <Checkbox label={loremIpsum(1)} />
        <Checkbox label="Apple" />
        <Checkbox label="Cookie" />
      </FormGroup>,
    );
    expect(rootQueries.toJSON()).toMatchSnapshot();
  });
  test('FormGroup with Radio', async () => {
    const rootQueries = render(
      <FormGroup>
        <Radio label={loremIpsum(1)} />
        <Radio label="Apple" />
        <Radio label="Cookie" />
      </FormGroup>,
    );
    expect(rootQueries.toJSON()).toMatchSnapshot();
  });
  test('FormGroup with Radio helper Text', async () => {
    const rootQueries = render(
      <FormGroup helperText={'Helper Text'}>
        <Radio label={loremIpsum(1)} />
        <Radio label="Apple" />
        <Radio label="Cookie" />
      </FormGroup>,
    );
    expect(rootQueries.toJSON()).toMatchSnapshot();
    const helperText = await rootQueries.findByText('Helper Text');
    expect(helperText).toHaveStyle({
      color: formToken.componentFormHelperTextTextColor,
      paddingTop: token.componentFormGroupHelperTextStateHasLabelPaddingTop,
    });
    expect(helperText.props.style[1].color).toEqual(
      formToken.componentFormHelperTextTextColor,
    );
  });
  test('FormGroup with Radio Error Text', async () => {
    const rootQueries = render(
      <FormGroup error={'Error Text ?'}>
        <Radio label={loremIpsum(1)} />
        <Radio label="Apple" />
        <Radio label="Cookie" />
      </FormGroup>,
    );
    expect(rootQueries.toJSON()).toMatchSnapshot();
    const errorText = await rootQueries.findByText('Error Text ?');
    expect(errorText.props.style[1].color).toEqual(
      formToken.componentFormHelperTextStateErrorTextColor,
    );
  });
});
