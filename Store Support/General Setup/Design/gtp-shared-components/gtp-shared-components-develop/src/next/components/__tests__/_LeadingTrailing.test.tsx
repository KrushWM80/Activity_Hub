import * as React from 'react';
import {Text} from 'react-native';

import {render} from '@testing-library/react-native';
import {Icons} from '@walmart/gtp-shared-icons';

import {_LeadingTrailing} from '../_LeadingTrailing';

describe('Test _LeadingTrailing', () => {
  test('it should render correctly when passing an Icon', async () => {
    const rootQueries = render(
      <_LeadingTrailing
        node={<Icons.SparkIcon />}
        iconProps={{size: 16, UNSAFE_style: {marginLeft: 16, marginTop: 24}}}
      />,
    );
    const icon = await rootQueries.findByTestId('SparkIcon');
    expect(icon).toHaveStyle([
      {
        height: 16,
        width: 16,
        tintColor: 'black',
      },
      {
        marginLeft: 16,
        marginTop: 24,
      },
    ]);
  });

  test('it should render correctly when passing a random component', async () => {
    const rootQueries = render(
      <_LeadingTrailing
        node={
          <Text style={{fontSize: 17, color: '#000', fontWeight: '700'}}>
            testing
          </Text>
        }
      />,
    );
    const component = await rootQueries.findByText('testing');
    expect(component).toHaveStyle({
      fontSize: 17,
      color: '#000',
      fontWeight: '700',
    });
  });

  test('it should render correctly when passing a JSX construct with condition false', async () => {
    const someCondition = false;
    const rootQueries = render(
      <_LeadingTrailing
        node={
          someCondition ? (
            <Text style={{fontSize: 17, color: '#000', fontWeight: '700'}}>
              testing
            </Text>
          ) : (
            <Text style={{fontSize: 19, color: '#fff', fontWeight: '400'}}>
              testing
            </Text>
          )
        }
      />,
    );
    const component = await rootQueries.findByText('testing');
    expect(component).toHaveStyle({
      fontSize: 19,
      color: '#fff',
      fontWeight: '400',
    });
  });

  test('it should render correctly when passing a JSX construct with condition true', async () => {
    const someCondition = true;
    const rootQueries = render(
      <_LeadingTrailing
        node={
          someCondition ? (
            <Text style={{fontSize: 17, color: '#000', fontWeight: '700'}}>
              testing
            </Text>
          ) : (
            <Text style={{fontSize: 19, color: '#fff', fontWeight: '400'}}>
              testing
            </Text>
          )
        }
      />,
    );
    const component = await rootQueries.findByText('testing');
    expect(component).toHaveStyle({
      fontSize: 17,
      color: '#000',
      fontWeight: '700',
    });
  });
});
