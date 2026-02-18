import * as React from 'react';
import {Platform, Text} from 'react-native';

import {render} from '@testing-library/react-native';
import {Icons} from '@walmart/gtp-shared-icons';

import * as utils from '../';

type DriverProps = {
  rNode: React.ReactNode;
};

const Driver: React.FC<DriverProps> = (props: DriverProps) => {
  const {rNode} = props;
  const isIcon = utils.checkElement(rNode, 'Icon');
  if (isIcon) {
    return (
      <>
        <Text>yes</Text>;
      </>
    );
  }
  return <>{rNode}</>;
};

describe('Test checkElement', () => {
  test('it returns true for *Icon', () => {
    const rootQueries = render(<Driver rNode={<Icons.LockIcon />} />);
    const txt = rootQueries.getByText('yes');
    expect(txt).toBeTruthy();
  });

  test('it returns false for non *Icon', () => {
    const rootQueries = render(<Driver rNode={<Text>no</Text>} />);
    const txt = rootQueries.getAllByText('no');
    expect(txt).toBeTruthy();
  });

  test('it returns false for conditional construct', () => {
    const someBool = true;
    const rootQueries = render(
      <Driver rNode={someBool ? <Text>no</Text> : <Text />} />,
    );
    const txt = rootQueries.getByText('no');
    expect(txt).toBeTruthy();
  });

  test('it returns true for conditional construct using *Icon', () => {
    const someBool = true;
    const rootQueries = render(
      <Driver rNode={someBool ? <Icons.BoxIcon /> : <Text />} />,
    );
    const txt = rootQueries.getByText('yes');
    expect(txt).toBeTruthy();
  });
});

describe('Test capitalize', () => {
  test('return the correct result', () => {
    expect(utils.capitalize('eskimo')).toEqual('Eskimo');
  });
});

describe('Test findKey', () => {
  test('it returns true for an existin key', () => {
    const driver = {
      one: 1,
      two: 'dos',
    };
    expect(utils.findKey(driver, 1)).toBeTruthy();
  });
  test('it returns false for a non-existing key', () => {
    const driver = {
      one: 'un',
      two: 'deux',
    };
    expect(utils.findKey(driver, 'troix')).toBeFalsy();
  });
});

describe('Test removeChildren', () => {
  test('it returns the correct stripped object', () => {
    const driver = {
      one: 1,
      children: 'dos',
    };
    expect(utils.removeChildren(driver)).toEqual({one: 1});
  });
  test('it returns the same object if children is not present', () => {
    const driver = {
      one: 'un',
      two: 'deux',
    };
    expect(utils.removeChildren(driver)).toEqual(driver);
  });
});

describe('Test isUndefined', () => {
  test('it returns true for undefined argument', () => {
    const driver = undefined;
    expect(utils.isUndefined(driver)).toBeTruthy();
  });
  test('it returns false for non-undefined argument', () => {
    const driver = {
      one: 'un',
      two: 'deux',
    };
    expect(utils.isUndefined(driver)).toBeFalsy();
  });
});

describe('Test isObject', () => {
  test('it returns true for object', () => {
    const driver = {
      one: 'un',
      two: 'deux',
    };
    expect(utils.isObject(driver)).toBeTruthy();
  });
  test('it returns false for array', () => {
    const driver = [1, 2, 3];
    expect(utils.isUndefined(driver)).toBeFalsy();
  });
});

describe('Test calculatePercentageOf', () => {
  test('it tab 5 more then 20% of 390 device width 78', () => {
    expect(utils.calculatePercentageOf(390, 20)).toEqual(78);
  });
  test('if tab 4 then 25% of 390 device width 97.5', () => {
    expect(utils.calculatePercentageOf(390, 25)).toEqual(97.5);
  });
  test('it tab 2 then 50% of 390 device width 195', () => {
    expect(utils.calculatePercentageOf(390, 50)).toEqual(195);
  });
});
describe('Test convertStringToMS', () => {
  test('convertStringToMS 0.9s', () => {
    expect(utils.convertStringToMS('0.9s')).toEqual(900);
  });
  test('convertStringToMS 0.5s', () => {
    expect(utils.convertStringToMS('0.5s')).toEqual(500);
  });
});

describe('Test calculateBSContainerPercentageValue', () => {
  test('calculateBSContainerPercentageValue for 680 75% 67 16 ', () => {
    expect(
      utils.calculateBSContainerPercentageValue(680, '75%', 67, 16),
    ).toEqual(427);
  });
  test('calculateBSContainerPercentageValue for 680 500 67 16 ', () => {
    expect(utils.calculateBSContainerPercentageValue(680, 500, 67, 16)).toEqual(
      484,
    );
  });
  test('calculateBSContainerPercentageValue for 680 "50%" 67 16 ', () => {
    expect(
      utils.calculateBSContainerPercentageValue(680, '50%', 67, 16),
    ).toEqual(257);
  });
});

describe('Test getBSPaddingBottomBasedOnRNVersion on Android', () => {
  beforeEach(() => {
    Platform.OS = 'android';
  });
  test('getBSPaddingBottomBasedOnRNVersion RNVersion 0.76.9', () => {
    expect(utils.getBSPaddingBottomBasedOnRNVersion('0.76.9', 312)).toEqual({
      paddingBottom: 0,
    });
  });
  test('getBSPaddingBottomBasedOnRNVersion RNVersion 0.74.5', () => {
    expect(utils.getBSPaddingBottomBasedOnRNVersion('0.74.5', 312)).toEqual({
      paddingBottom: 312,
    });
  });
});

describe('Test getBSPaddingBottomBasedOnRNVersion on ios', () => {
  beforeEach(() => {
    Platform.OS = 'ios';
  });
  test('getBSPaddingBottomBasedOnRNVersion RNVersion 0.76.9', () => {
    expect(utils.getBSPaddingBottomBasedOnRNVersion('0.76.9', 312)).toEqual({
      paddingBottom: 312,
    });
  });
  test('getBSPaddingBottomBasedOnRNVersion RNVersion 0.74.5', () => {
    expect(utils.getBSPaddingBottomBasedOnRNVersion('0.74.5', 312)).toEqual({
      paddingBottom: 312,
    });
  });
});
