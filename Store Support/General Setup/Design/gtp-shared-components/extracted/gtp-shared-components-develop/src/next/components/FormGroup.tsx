import * as React from 'react';
import {StyleProp, StyleSheet, TextStyle, View, ViewStyle} from 'react-native';

import * as formToken from '@livingdesign/tokens/dist/react-native/light/regular/components/Form';
import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/FormGroup';
import {Icons} from '@walmart/gtp-shared-icons';
import flattenChildren from 'react-keyed-flatten-children';

import {getFont, Weights} from '../../theme/font';
import {CommonViewProps} from '../types/ComponentTypes';
import {a11yRole} from '../utils';

import {Body} from './Body';

// ---------------
// Props
// ---------------

export type FormGroupProps = CommonViewProps & {
  /**
   * The content for the form group.
   */
  children: React.ReactNode;
  /**
   * The error for the form group.
   */
  error?: React.ReactNode;
  /**
   * The helper text for the form group.
   */
  helperText?: React.ReactNode;
  /**
   * The label for the form group.
   */
  label?: React.ReactNode;
  /**
   * If provided, the `style` to provide to the root element. @note This property is prefixed with `UNSAFE` as
   * its use often results in unintended side effects.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
};

/**
 * A Form Group lets you create a list of grouped form elements. The form elements can be radio buttons, checkboxes, text area, etc.
 *
 * ## Usage
 * ```js
 * import {Checkbox, FormGroup} from '@walmart/gtp-shared-components`;
 *
 * <FormGroup label="Lorem Ipsum" helperText="Helper Text">
 *   <Checkbox label="Apple"/>
 *   <Checkbox label="Orange"/>
 * </FormGroup>
 * ```
 */
const FormGroup: React.FC<FormGroupProps> = (props) => {
  const {
    children,
    error,
    helperText,
    label,
    UNSAFE_style = {},
    ...rest
  } = props;

  const kids = flattenChildren(children);
  // ---------------
  // Rendering
  // ---------------
  const renderChild = () => {
    return kids.map((child, index) => {
      return (
        <View key={index} style={ss().childContainer}>
          {React.cloneElement(child as React.ReactElement)}
        </View>
      );
    });
  };
  const renderHelperTextOrError = () => {
    if (error) {
      return (
        <View style={ss().errorContainer}>
          <Icons.ExclamationCircleFillIcon
            color={formToken.componentFormHelperTextIconStateErrorIconColor}
            UNSAFE_style={ss().errorIcon}
          />
          <Body UNSAFE_style={ss().errorText}>{error}</Body>
        </View>
      );
    } else if (helperText) {
      return (
        helperText && <Body UNSAFE_style={ss().helperText}>{helperText}</Body>
      );
    } else {
      return null;
    }
  };
  const renderLegend = () => {
    return (
      <View
        accessibilityRole={a11yRole('text')}
        style={ss().labelGroupContainer}>
        {label && <Body UNSAFE_style={ss().label}>{label}</Body>}
        {renderHelperTextOrError()}
      </View>
    );
  };
  return (
    <View
      testID={FormGroup.displayName}
      style={[ss().container, UNSAFE_style]}
      {...rest}>
      {renderLegend()}
      {renderChild()}
    </View>
  );
};

// ---------------
// Styles
// ---------------
const ss = () => {
  const style = StyleSheet.create({
    container: {
      flexDirection: 'column',
      flex: 1,
    },
    childContainer: {
      marginVertical: token.componentFormGroupItemGap,
    },
    labelGroupContainer: {
      marginBottom: token.componentFormGroupContentMarginTop,
    },
    helperText: {
      ...getFont(),
      paddingTop: token.componentFormGroupHelperTextStateHasLabelPaddingTop,
      color: formToken.componentFormHelperTextTextColor,
    } as TextStyle,
    label: {
      ...getFont(token.componentFormGroupTitleFontWeight.toString() as Weights), //"700"
      fontSize: token.componentFormGroupTitleFontSize, //14
      lineHeight: token.componentFormGroupTitleLineHeight, //20
      color: token.componentFormGroupTitleTextColor, // "#2e2f32"
    } as TextStyle,
    errorContainer: {
      flexDirection: 'row',
    },
    errorIcon: {
      marginTop: 6,
    },
    errorText: {
      color: formToken.componentFormHelperTextStateErrorTextColor,
      marginHorizontal:
        formToken.componentFormHelperTextIconStateErrorMarginEnd, // 4,
    },
  });
  return style;
};

FormGroup.displayName = 'FormGroup';
export {FormGroup};
