import * as React from 'react';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Skeleton';
import {cleanup, render} from '@testing-library/react-native';
import MockDate from 'mockdate';

import {timeTravel} from '../../utils/timerUtils';
import {Skeleton, SkeletonVariant} from '../Skeleton';
import {SkeletonText} from '../SkeletonText';

beforeEach(() => {
  MockDate.set(0);
  jest.useFakeTimers({legacyFakeTimers: true});
});
const bgColor = 'rgba(248, 248, 248, 1)';
afterEach(cleanup);

describe('Basic Skeletons with no props', () => {
  test('Default Skeleton variant, width, and height ', async () => {
    const rootQueries = render(<Skeleton />);
    const skeleton = await rootQueries.findByTestId('Skeleton');
    expect(skeleton).toHaveStyle({
      height: token.componentSkeletonContainerHeight,
      width: token.componentSkeletonContainerWidth,
      borderRadius:
        token.componentSkeletonContainerVariantRectangleBorderRadius,
    });
  });

  test('SkeletonText default props has 3 lines', async () => {
    const rootQueries = render(<SkeletonText />);
    const skeletonText = await rootQueries.findByTestId('SkeletonText');
    expect(skeletonText.children.length).toBe(3);
  });

  test('SkeletonText lines={5} prop has 5 lines', async () => {
    const rootQueries = render(<SkeletonText lines={5} />);
    const skeletonText = await rootQueries.findByTestId('SkeletonText');
    expect(skeletonText.children.length).toBe(5);
  });
});

describe('Skeleton Animations', () => {
  test('Skeleton before animation', async () => {
    const rootQueries = render(<Skeleton />);
    const skeleton = await rootQueries.findByTestId('Skeleton');
    expect(skeleton).toHaveStyle({
      backgroundColor: bgColor,
    });
  });

  test('Skeleton with half animation', async () => {
    const rootQueries = render(<Skeleton />);
    const skeleton = await rootQueries.findByTestId('Skeleton');
    timeTravel(750);
    expect(skeleton).toHaveStyle({
      backgroundColor: 'rgba(227, 228, 229, 1)',
    });
  });

  test('Skeleton with finished animation', async () => {
    const rootQueries = render(<Skeleton />);
    const skeleton = await rootQueries.findByTestId('Skeleton');
    timeTravel(1500);
    expect(skeleton).toHaveStyle({
      backgroundColor: bgColor,
    });
  });

  test('Skeleton with one and half animations', async () => {
    const rootQueries = render(<Skeleton />);
    const skeleton = await rootQueries.findByTestId('Skeleton');
    timeTravel(2250);
    expect(skeleton).toHaveStyle({
      backgroundColor: 'rgba(228, 229, 230, 1)', // TODO: Why is this different from half animation?
    });
  });

  test('Skeleton with two finished animations', async () => {
    const rootQueries = render(<Skeleton />);
    const skeleton = await rootQueries.findByTestId('Skeleton');
    timeTravel(3000);
    expect(skeleton).toHaveStyle({
      backgroundColor: bgColor,
    });
  });
});

describe.each<SkeletonVariant>(['rectangle', 'rounded'])(
  'Skeletons with variant',
  (variant) => {
    describe.each<number>([50, 100])('... and width', (width) => {
      describe.each<number>([50, 100])('... and height', (height) => {
        test(`Skeleton with ${variant} variant and ${width} width and ${height} height`, async () => {
          const rootQueries = render(
            <Skeleton variant={variant} width={width} height={height} />,
          );
          if (Skeleton.displayName) {
            const skeleton = await rootQueries.findByTestId(
              Skeleton.displayName,
            );

            const getBorderRadius = () => {
              if (variant === 'rounded') {
                return token.componentSkeletonContainerVariantRoundedBorderRadius;
              }
              return token.componentSkeletonContainerVariantRectangleBorderRadius;
            };

            expect(skeleton).toHaveStyle({
              height: height,
              width: width,
              borderRadius: getBorderRadius(),
            });
          }
        });
      });
    });
  },
);
