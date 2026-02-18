import * as React from 'react';
import {FlexStyle} from 'react-native';

import {render} from '@testing-library/react-native';

import {_Gap, Direction} from '../_Gap';
import {Badge} from '../Badge';

const badge1 = <Badge color="blue" />;
const badge2 = <Badge color="red" />;

describe.each<Direction>(['horizontal', 'vertical'])(
  'Should test the direction: ',
  (direction) => {
    test(`Test _Gap for direction="${direction}".`, async () => {
      const gap = 20;
      const rootQueries = render(
        <_Gap gap={gap} direction={direction}>
          {' '}
          {badge1} {badge2}{' '}
        </_Gap>,
      );
      const _gap = await rootQueries.findByTestId('_Gap');
      let flexDirection;
      let padding;
      if (direction === 'vertical') {
        flexDirection = 'column';
        padding = {paddingHorizontal: gap / -2};
      } else {
        flexDirection = 'row';
        padding = {paddingVertical: gap / -2};
      }
      expect(_gap).toHaveStyle({
        flexDirection,
        ...padding,
      } as FlexStyle);
    });
    test(`Test _Gap to show divider direction="${direction}".`, async () => {
      const rootQueries = render(
        <_Gap direction={direction} showSeparator={true}>
          {badge1}
          {badge2}
        </_Gap>,
      );
      const divider = rootQueries.queryAllByTestId('Divider');
      if (direction === 'vertical') {
        expect(divider.length).toEqual(1);
      } else {
        expect(divider.length).toEqual(0);
      }
    });
  },
);
