import * as React from 'react';

type ControllerProps = {
  children: React.ReactElement | Array<React.ReactElement>;
  controlProp: string;
  initialValue: any;
  setValueProp: string;
  onValueChange?: (value: any) => void;
};

type ControllerState = {
  value: any;
};

/** This Controller is used to maintain state for a component (or set of components). */
export default class Controller extends React.Component<
  ControllerProps,
  ControllerState
> {
  static defaultProps: Partial<ControllerProps> = {
    controlProp: 'value',
    setValueProp: 'onChange',
  };
  state: ControllerState = {
    value: this.props.initialValue,
  };
  render() {
    const {children, controlProp, setValueProp, onValueChange, ...props} =
      this.props;
    return React.Children.map(children, (element: React.ReactElement) =>
      React.cloneElement(element, {
        [controlProp]: this.state.value,
        [setValueProp]: (value: any) =>
          this.setState({value}, () => onValueChange?.(value)),
        ...props,
      }),
    );
  }
}
