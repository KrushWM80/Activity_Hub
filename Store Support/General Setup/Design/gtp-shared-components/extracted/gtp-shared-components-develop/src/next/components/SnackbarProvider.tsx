import * as React from 'react';
import {
  Animated,
  DimensionValue,
  Easing,
  GestureResponderEvent,
  StyleSheet,
  ViewProps,
} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Snackbar';
import DropShadow from 'react-native-drop-shadow';

import {colors} from '../utils';

import {Snackbar, SnackbarActionButtonProps} from './Snackbar';

export type SnackProps = ViewProps & {
  /**
   * ActionButton to show on the Snackbar
   */
  actionButton?: SnackbarActionButtonProps;

  /**
   * Close Button (transparent icon X) to show on the Snackbar
   */
  onClose?: (event: GestureResponderEvent) => void;

  /**
   * Message for the snack
   */
  message: string;

  /**
   * Optional custom vertical positioning
   * (distance from the bottom)
   * It can be either:
   * - an absolute number (e.g. 200) or
   * - a percentage of the screen height (e.g. 25%)
   */
  customPosition?: number | string;
};

export const SnackbarContext = React.createContext<
  Readonly<{
    addSnack: (snack: SnackProps) => void;
  }>
>({
  addSnack: () => undefined,
});

export type SnackbarProviderProps = {
  /**
   * The content for the snackbar provider.
   */
  children: React.ReactNode;
};

/**
 * Add the SnackbarProvider to your application's root to access the useSnackbar hook
 *
 * ```js
 * import {SnackbarProvider} from '@walmart/gtp-shared-components`;
 *
 * <SnackbarProvider>
 *   <App />
 * </SnackbarProvider>
 * ```
 */
export const SnackbarProvider: React.FC<SnackbarProviderProps> = (props) => {
  const {children} = props;

  const [snack, setSnack] = React.useState<SnackProps>();

  const value = React.useRef({
    addSnack: setSnack,
  });

  const customPosition = snack?.customPosition
    ? snack.customPosition
    : 'default';

  const {...rootProps} = snack || {};
  const {...actionProps} = snack?.actionButton || {};

  const fadeAnim = React.useRef(new Animated.Value(0)).current; // Initial value for opacity: 0
  const timerID = React.useRef<ReturnType<typeof setTimeout> | null>(null);
  const AnimatedDropShadow = Animated.createAnimatedComponent(DropShadow);

  const fadeOutSnackbar = React.useCallback(() => {
    if (snack) {
      Animated.timing(fadeAnim, {
        toValue: 0,
        duration: 700,
        easing: Easing.ease,
        useNativeDriver: true,
      }).start(() => {
        setSnack(undefined);
        if (timerID.current) {
          clearTimeout(timerID.current);
        }
      });
    }
  }, [fadeAnim, snack]);

  const timerToCloseSnackbar = React.useCallback(() => {
    if (snack?.message) {
      const {message} = snack;
      const duration =
        message.length > 120 ? 3500 + (message.length - 120) * 60 : 3500;
      timerID.current = setTimeout(() => fadeOutSnackbar(), duration);
    }
  }, [snack, fadeOutSnackbar]);

  const fadeInSnackBar = React.useCallback(() => {
    Animated.timing(fadeAnim, {
      toValue: 1,
      duration: 500,
      easing: Easing.ease,
      useNativeDriver: true,
    }).start(() => timerToCloseSnackbar());
  }, [fadeAnim, timerToCloseSnackbar]);

  React.useEffect(() => {
    if (snack) {
      fadeInSnackBar();
    }
  }, [snack, fadeInSnackBar]);

  return (
    <SnackbarContext.Provider value={value.current}>
      {children}
      {snack && (
        <AnimatedDropShadow
          style={{...ss(customPosition).container, opacity: fadeAnim}}>
          <Snackbar
            {...rootProps} // spread props go on top so as to not override intended behaviors
            actionButton={
              snack?.actionButton
                ? {
                    ...actionProps, // spread props go on top so as to not override intended behaviors
                    caption: snack.actionButton?.caption,
                    onPress: (event: GestureResponderEvent) => {
                      snack.actionButton?.onPress?.(event);
                      fadeOutSnackbar();
                    },
                  }
                : undefined
            }
            closeButton={{
              onPress: (event: GestureResponderEvent) => {
                snack.onClose?.(event);
                fadeOutSnackbar();
              },
            }}>
            {snack?.message}
          </Snackbar>
        </AnimatedDropShadow>
      )}
    </SnackbarContext.Provider>
  );
};

// ---------------
// Styles
// ---------------
const ss = (customPosition: number | string) => {
  const _customPosition =
    customPosition === 'default'
      ? token.componentSnackbarContainerPaddingBottomBM
      : customPosition;
  return StyleSheet.create({
    container: {
      width: '100%',
      position: 'absolute',
      bottom: _customPosition as DimensionValue,
      shadowColor: colors.black,
      shadowOpacity: 0.15,
      shadowRadius: 10,
      shadowOffset: {
        height: 5,
        width: 0,
      },
      // TODO: how to determine small/medium device breakpoints, check with Cory
      // https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/150#discussion_r3856982
    },
  });
};

SnackbarProvider.displayName = 'SnackbarProvider';
