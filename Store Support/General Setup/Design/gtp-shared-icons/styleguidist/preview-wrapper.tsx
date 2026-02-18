import * as React from 'react';
import {View, ViewStyle} from 'react-native';

export type PreviewWrapperProps = {
  style: ViewStyle;
  children: React.ReactNode;
};
export default class PreviewWrapper extends React.Component<PreviewWrapperProps> {
  render() {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const {style, children, ...props} = this.props;
    return <View {...props}>{children}</View>;
  }
}
