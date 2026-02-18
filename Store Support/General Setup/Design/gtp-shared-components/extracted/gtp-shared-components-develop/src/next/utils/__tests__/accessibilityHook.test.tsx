/* eslint-disable react/react-in-jsx-scope */
// useAccessibilityFocus.test.tsx
import {NavigationContext, useFocusEffect} from '@react-navigation/native';
import {render, renderHook} from '@testing-library/react-native';

import {Button} from '../../../next/components/Button';
import {useAccessibilityFocus} from '../useAccessibilityFocus';

const mockFn = jest.fn(() => jest.fn());

// Mock NavigationContext value data
const navContext = {
  isFocused: () => true,
  // addListener returns an unsubscribe function.
  addListener: mockFn,
};

const MockComponent: React.FC = () => {
  const [focusRef, setFocus] = useAccessibilityFocus();

  useFocusEffect(setFocus);

  const renderButtons = () => {
    return (
      <>
        <Button onPress={() => {}}>Component 1</Button>
        <Button ref={focusRef} onPress={() => {}}>
          Component 2
        </Button>
      </>
    );
  };

  return renderButtons();
};

describe('useAccessibilityFocus', () => {
  test('should render accessibility hook', () => {
    const {result} = renderHook(useAccessibilityFocus);
    expect(result.current[0].current).toEqual(null);
    expect(result.current[1]).toBeTruthy();

    render(
      //@ts-ignore
      <NavigationContext.Provider value={navContext}>
        <MockComponent />
      </NavigationContext.Provider>,
    );

    expect(mockFn).toHaveBeenCalledTimes(2);
  });
});
