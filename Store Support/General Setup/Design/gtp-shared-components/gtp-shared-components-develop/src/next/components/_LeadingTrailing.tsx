import * as React from 'react';
import {ImageStyle} from 'react-native';

import {IconSize} from '@walmart/gtp-shared-icons';

type IconProps = {
  color?: string;
  size?: IconSize;
  UNSAFE_style?: ImageStyle | Array<ImageStyle>;
  testID?: string;
};

type LeadingTrailingProps = {
  node: React.ReactNode;
  iconProps?: IconProps;
  UNSAFE_style?: any;
};

/**
 * @internal
 */
const _LeadingTrailing: React.FC<LeadingTrailingProps> = (props) => {
  const {node, iconProps, UNSAFE_style} = props;
  const {
    color,
    size,
    UNSAFE_style: ICON_UNSAFE_style,
    testID,
  } = iconProps || {};

  if (!node) {
    return <>{null}</>;
  } else if (!React.isValidElement(node)) {
    return <>{node}</>;
  } else if (color || size || ICON_UNSAFE_style || testID) {
    //verifying the iconProps
    // If it's an icon we provide full styling
    return <>{React.cloneElement(node, iconProps)}</>;
  } else {
    // If it's not an icon consumer needs to provide styling
    return <>{React.cloneElement(node, UNSAFE_style)}</>;
  }
};

export {_LeadingTrailing};
