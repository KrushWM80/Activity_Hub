import * as React from 'react';
import {
  FlexStyle,
  StyleProp,
  StyleSheet,
  TextStyle,
  View,
  ViewStyle,
} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/ErrorMessage';
import flattenChildren from 'react-keyed-flatten-children';

import {getFont} from '../../theme/font';
import type {CommonViewProps} from '../types/ComponentTypes';
import {a11yRole} from '../utils';

import {Body, BodySize} from './Body';
import {Heading, HeadingSize, HeadingWeight} from './Heading';

// ---------------
// Props
// ---------------

export type ErrorMessageProps = CommonViewProps & {
  /**
   * The content for the error message.
   */
  children: React.ReactNode;
  /**
   * The media for the error message.
   * Typically an image above the title
   */
  media?: React.ReactNode;
  /**
   * The title for the error message.
   */
  title: React.ReactNode;
  /**
   * The actions for the error message.
   */
  actions?: React.ReactNode;
  /**
   * If provided, the `style` to provide to the root element. @note This property is prefixed with
   * `UNSAFE` as its use often results in unintended side effects.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
};

/**
 * Error Messages communicate system errors in a consistent and expected way.
 *
 * ## Usage
 * ```js
 * import {ErrorMessage} from '@walmart/gtp-shared-components`;
 *
 * <ErrorMessage
 *   title={'No internet connection'}>
 *   Make sure you’re connected to WiFi or data and try again.
 * </ErrorMessage>
 * ```
 */
const ErrorMessage: React.FC<ErrorMessageProps> = (props) => {
  const {children, media, title, actions, UNSAFE_style = {}, ...rest} = props;

  // ---------------
  // Rendering
  // ---------------

  const renderTitle = () => {
    return title ? (
      <Heading
        testID={ErrorMessage.displayName + '-title'}
        weight={
          `${token.componentErrorMessageTitleAliasOptionsWeight}` as HeadingWeight //"700"
        }
        size={token.componentErrorMessageTitleAliasOptionsSize as HeadingSize} // "large"
        UNSAFE_style={ss.titleContainer}>
        {title}
      </Heading>
    ) : null;
  };

  const renderMedia = () => {
    return (
      media &&
      React.cloneElement(media as React.ReactElement, {
        style: ss.mediaContainer,
        testID: ErrorMessage.displayName + '-media',
      })
    );
  };

  const renderActions = () => {
    const kids = flattenChildren(actions);
    return (
      actions && (
        <View
          style={ss.actionsContainer}
          testID={ErrorMessage.displayName + '-actions'}
          {...rest}>
          {kids.map((child, index) => (
            <React.Fragment key={index}>{child}</React.Fragment>
          ))}
        </View>
      )
    );
  };

  const renderMessage = () => {
    return (
      <Body
        testID={ErrorMessage.displayName + '-content'}
        size={
          `${token.componentErrorMessageTextLabelAliasOptionsSize}` as BodySize //"medium"
        }
        UNSAFE_style={ss.messageText}>
        {children}
      </Body>
    );
  };

  return (
    <View
      accessibilityRole={a11yRole('alert')}
      testID={ErrorMessage.displayName}
      style={[ss.container, UNSAFE_style]}>
      {renderMedia()}
      {renderTitle()}
      {renderMessage()}
      {renderActions()}
    </View>
  );
};

// ---------------
// Styles
// ---------------
const ss = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: token.componentErrorMessageContainerAlignHorizontal as Extract<
      FlexStyle,
      'alignItems'
    >, //'center',
  },
  mediaContainer: {
    maxWidth: 200,
    maxHeight: 200,
    marginBottom: token.componentErrorMessageMediaMarginBottom, //32
  },
  messageText: {
    ...getFont(),
    color: token.componentErrorMessageTextLabelTextColor, //"#74767c"
  } as TextStyle,
  titleContainer: {
    marginBottom: token.componentErrorMessageTitleMarginBottom, //8
  },
  actionsContainer: {
    marginTop: token.componentErrorMessageActionContentMarginTop, //24
  },
});

ErrorMessage.displayName = 'ErrorMessage';
export {ErrorMessage};
