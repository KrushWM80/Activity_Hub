import * as React from 'react';
import {Animated} from 'react-native';

export type SharedAnimator = {
  value: Animated.Value;
  animation: Animated.CompositeAnimation;
};

let _animatorInstance: SharedAnimator | null = null;
let _instancesCount: number = 0;

const useSharedLoopAnimator = (duration: number) => {
  React.useEffect(() => {
    _instancesCount = _instancesCount + 1;
    return () => {
      _instancesCount = _instancesCount - 1;
      if (_instancesCount <= 0) {
        _animatorInstance = null;
      }
    };
  }, []);

  if (!_animatorInstance) {
    const value = new Animated.Value(0);
    const animation = Animated.loop(
      Animated.timing(value, {
        toValue: 2,
        duration: duration,
        useNativeDriver: false,
      }),
    );
    animation.start();
    _animatorInstance = {value, animation};
  }
  return _animatorInstance;
};

export {useSharedLoopAnimator};
