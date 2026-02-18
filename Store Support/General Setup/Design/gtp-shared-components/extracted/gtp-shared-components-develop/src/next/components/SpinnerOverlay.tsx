import * as React from 'react';
import {
  Modal,
  SafeAreaView,
  StyleProp,
  StyleSheet,
  View,
  ViewStyle,
} from 'react-native';

import {CommonModalBaseProps} from '../types/ComponentTypes';

import {Spinner, SpinnerColor, SpinnerSize} from './Spinner';

export type SpinnerOverlayProps = CommonModalBaseProps & {
  /**
   * The optional content that will display under the Spinner
   */
  children?: React.ReactNode;

  /**
   * Color for the foreground of the spinner
   * valid values: <strong>'gray' | 'white'</strong>.
   * @default gray
   */
  spinnerColor?: SpinnerColor;

  /**
   * The size of the spinner
   * valid values: <strong>'small' | 'large'</strong>.
   * @default large
   */
  spinnerSize?: SpinnerSize;

  /**
   * Whether to darken the background of the overlay
   * @default false
   */
  darken?: boolean;

  /**
   * Whether the overlay is transparent
   * @default true
   */
  transparent?: boolean;

  /**
   * Whether the overlay is visible
   */
  visible: boolean;

  /**
   * If provided, the `style` to provide to the root element.
   * This property is prefixed with `UNSAFE` as its use
   * often results in unintended side effects.
   */
  UNSAFE_style?: StyleProp<ViewStyle> | undefined;
};

/**
 * SpinnerOverlay is a component that displays a Spinner over the content of the screen.
 *
 * ## Usage
 * ```js
 * import {SpinnerOverlay} from '@walmart/gtp-shared-components`;
 *
 * const [isLoading, setLoading] = useState(false);
 *
 * const getData = async () => {
 *   setLoading(true);
 *   try {
 *     const response = await fetch('<Your API URL here>');
 *     const json = await response.json();
 *   } catch (error) {
 *     console.error(error);
 *   } finally {
 *     setLoading(false);
 *   }
 * };
 *
 * useEffect(() => {
 *   getData();
 * }, []);
 *
 * <SpinnerOverlay
 *   visible={isLoading}
 *   darken={true}
 *   spinnerColor={'white'}
 *   transparent={true}
 * />
 * ```
 */
const SpinnerOverlay: React.FC<SpinnerOverlayProps> = (props) => {
  const {
    children,
    spinnerColor,
    spinnerSize,
    darken = false,
    transparent = true,
    UNSAFE_style,
    ...rest
  } = props;
  return (
    <Modal
      {...rest}
      transparent={transparent}
      testID={SpinnerOverlay.displayName}>
      <SafeAreaView
        testID={SpinnerOverlay.displayName + '-container'}
        style={[
          styles.container,
          darken ? styles.darkenedContainer : null,
          UNSAFE_style,
        ]}>
        <View
          testID={SpinnerOverlay.displayName + '-content'}
          style={styles.content}>
          <Spinner color={spinnerColor} size={spinnerSize} />
          {children}
        </View>
      </SafeAreaView>
    </Modal>
  );
};

// ---------------
// StyleSheet
// ---------------
const styles = StyleSheet.create({
  container: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    flexDirection: 'row',
    alignItems: 'center',
  },
  content: {
    flex: 1,
    alignSelf: 'center',
    alignItems: 'center',
  },
  darkenedContainer: {
    backgroundColor: 'rgba(0,0,0,.25)',
  },
});

SpinnerOverlay.displayName = 'SpinnerOverlay';
export {SpinnerOverlay};
