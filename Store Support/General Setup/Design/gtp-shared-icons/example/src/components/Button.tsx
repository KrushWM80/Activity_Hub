import * as React from 'react';
import {Pressable, PressableProps, StyleSheet, Platform} from 'react-native';

const testID = (id: string) =>
  Platform.OS === 'ios'
    ? {testID: id}
    : {accessible: true, accessibilityLabel: id};

// ---------------
// Props
// ---------------
export type MyComponentProps = PressableProps;

const Button: React.FC<MyComponentProps> = (props: MyComponentProps) => {
  const {children, onPress, style = {}, ...rest} = props;

  // ---------------
  // Rendering
  // ---------------
  return (
    <Pressable
      {...testID(`${Button.displayName}`)}
      onPress={onPress}
      style={[styles.button, style as PressableProps]}
      {...rest}>
      {children}
    </Pressable>
  );
};

// ---------------
// Styles
// ---------------
const styles = StyleSheet.create({
  button: {
    flexShrink: 1,
    justifyContent: 'center',
    alignItems: 'center',
    height: 50,
    borderWidth: 1,
    borderRadius: 30,
    paddingHorizontal: 12,
  },
});

Button.displayName = 'Button';
export {Button};
