import * as React from 'react';
import {KeyboardAvoidingView, Platform, StyleSheet} from 'react-native';

type _KeyboardAvoidingViewProps = {
  children: React.ReactNode;
};

/**
 * @internal
 */
const _KeyboardAvoidingView = ({children}: _KeyboardAvoidingViewProps) => {
  return Platform.OS === 'android' ? (
    <>{children}</>
  ) : (
    <KeyboardAvoidingView
      style={styles.wrapper}
      behavior="padding"
      keyboardVerticalOffset={80}>
      {children}
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  wrapper: {
    flex: 1,
  },
});

_KeyboardAvoidingView.displayName = '_KeyboardAvoidingView';
export {_KeyboardAvoidingView};
