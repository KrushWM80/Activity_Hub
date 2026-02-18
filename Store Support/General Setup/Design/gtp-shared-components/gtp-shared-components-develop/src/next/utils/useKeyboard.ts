import {useEffect, useState} from 'react';
import {
  EventSubscription,
  Keyboard,
  KeyboardEvent,
  Platform,
} from 'react-native';

export const useKeyboard = () => {
  const [isKeyboardVisible, setKeyboardVisible] = useState(false);
  const [keyboardHeight, setKeyboardHeight] = useState<number>(0);
  const [keyboardEvent, setKeyboardEvent] = useState<
    KeyboardEvent | undefined
  >();

  useEffect(() => {
    const subscriptions: Array<EventSubscription> = [];

    // https://reactnative.dev/docs/keyboard
    // Note that only keyboardDidShow and keyboardDidHide events are available on Android,
    // but we'd like to use willShow/willHide when possible on iOS to make the events more predictive
    if (Platform.OS === 'ios') {
      subscriptions.push(
        Keyboard.addListener('keyboardWillShow', (event: KeyboardEvent) => {
          setKeyboardVisible(true);
          setKeyboardEvent(event);
          setKeyboardHeight(event.endCoordinates.height);
        }),
      );

      subscriptions.push(
        Keyboard.addListener('keyboardWillHide', (event: KeyboardEvent) => {
          setKeyboardVisible(false);
          setKeyboardEvent(event);
          setKeyboardHeight(0);
        }),
      );
    } else {
      subscriptions.push(
        Keyboard.addListener('keyboardDidShow', (event: KeyboardEvent) => {
          setKeyboardVisible(true);
          setKeyboardEvent(event);
          setKeyboardHeight(event.endCoordinates.height);
        }),
      );

      subscriptions.push(
        Keyboard.addListener('keyboardDidHide', (event: KeyboardEvent) => {
          setKeyboardVisible(false);
          setKeyboardEvent(event);
          setKeyboardHeight(0);
        }),
      );
    }

    return () => {
      while (subscriptions.length) {
        let popped = subscriptions.pop();
        popped?.remove();
      }
    };
  }, []);

  return {isKeyboardVisible, keyboardHeight, keyboardEvent};
};
