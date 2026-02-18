import * as React from 'react';

import {cleanup, render} from '@testing-library/react-native';
import {getHostChildren} from '@testing-library/react-native/build/helpers/component-tree';
import MockDate from 'mockdate';

import {colors} from '../../utils';
import {timeTravel} from '../../utils/timerUtils';
import {Spinner, SpinnerColor, SpinnerSize} from '../Spinner';

beforeEach(() => {
  MockDate.set(0);
  jest.useFakeTimers({legacyFakeTimers: true});
});

afterEach(cleanup);

describe.each<SpinnerColor>(['gray', 'white'])('Test %s', (color) => {
  describe.each<SpinnerSize>(['small', 'large'])(' and %s Spinner', (size) => {
    test('It should render SparkLeaf with half rotation.', async () => {
      const rootQueries = render(<Spinner color={color} size={size} />);
      timeTravel(600); // This is one half duration of the animation
      expect(rootQueries.toJSON()).toMatchSnapshot();
    });
    test('It should render SparkLeaf with correct rotation.', async () => {
      const rootQueries = render(<Spinner color={color} size={size} />);
      timeTravel(900);
      expect(rootQueries.toJSON()).toMatchSnapshot();
    });
    test('It should render SparkLeaf with 0 rotation, 1200ms.', async () => {
      const rootQueries = render(<Spinner color={color} size={size} />);
      timeTravel(1200); // This is one duration of the animation
      expect(rootQueries.toJSON()).toMatchSnapshot();
    });
    test('It should render SparkLeaf with 0 rotation, 2400ms.', async () => {
      const rootQueries = render(<Spinner color={color} size={size} />);
      timeTravel(2400); // This is 2 duration of the animation
      expect(rootQueries.toJSON()).toMatchSnapshot();
    });
  });
});

// Expect SpinnerColor default to gray for colors other than `gray` | `white`
// @ts-ignore
describe.each<SpinnerColor>(['red', 'gray', colors.blue['10']])(
  'Test Spinner Color %s',
  // @ts-ignore
  (color) => {
    describe.each<SpinnerSize>(['small', 'large'])(' with size %s', (size) => {
      test('Should Render Default Gray Color', async () => {
        // @ts-ignore
        const rootQueries = render(<Spinner color={color} size={size} />);
        if (Spinner.displayName) {
          const spinner = await rootQueries.findByTestId(Spinner.displayName);
          expect(getHostChildren(spinner)[0]).toHaveStyle([
            {
              tintColor: 'gray',
              position: 'absolute',
            },
          ]);
        }
      });
    });
  },
);

// Expect SpinnerColor - 'white'
// @ts-ignore
describe.each<SpinnerColor>([colors.white, 'white'])(
  'Test Spinner Color %s',
  // @ts-ignore
  (color) => {
    describe.each<SpinnerSize>(['small', 'large'])(' with size %s', (size) => {
      test('Should Render White Color', async () => {
        // @ts-ignore
        const rootQueries = render(<Spinner color={color} size={size} />);
        if (Spinner.displayName) {
          const spinner = await rootQueries.findByTestId(Spinner.displayName);
          expect(getHostChildren(spinner)[0]).toHaveStyle([
            {
              tintColor: 'white',
              position: 'absolute',
            },
          ]);
        }
      });
    });
  },
);
