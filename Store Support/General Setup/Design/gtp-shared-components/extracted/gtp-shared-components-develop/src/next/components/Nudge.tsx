import * as React from 'react';
import {StyleProp, StyleSheet, View, ViewProps, ViewStyle} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Nudge';
import {Icons} from '@walmart/gtp-shared-icons';
import flattenChildren from 'react-keyed-flatten-children';

import {_LeadingTrailing as _Leading} from './_LeadingTrailing';
import {Body, BodySize, BodyWeight} from './Body';
import {IconButton, IconButtonProps, IconButtonSize} from './IconButton';

// ---------------
// Props
// ---------------
export type NudgeProps = ViewProps & {
  /**
   * The actions for the nudge.
   */
  actions?: React.ReactNode;
  /**
   * The content for the nudge.
   */
  children: React.ReactNode;
  /**
   * The props spread to the nudge's close button.
   */
  closeButtonProps?: IconButtonProps;
  /**
   * The leading content for the nudge.
   */
  leading?: React.ReactNode;
  /**
   * The callback fired when the nudge requests to close.
   */
  onClose?: (() => void) | undefined;
  /**
   * The title for the nudge.
   */
  title: React.ReactNode;
  /**
   * If provided, the `style` to provide to the root element. @note This property is prefixed with `UNSAFE` as
   * its use often results in unintended side effects.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
};

/**
 * Nudges provide supplemental information to support users on their current journey.
 *
 * ## Usage
 * ```js
 * import {Nudge, Link, Icons} from '@walmart/gtp-shared-components';
 *
 * <Nudge
 *   title={'The years start coming'}
 *   onClose={() => {}}
 *   leading={<Icons.EyeIcon size={24} />}
 *   actions={
 *     <Link color="default" onPress={() =>
 *               displayPopupAlert('Action', 'Action1 button pressed')}>
 *       Look away
 *     </Link>
 *   }>
 *   And they don't stop coming. Fed to the rules and I hit the ground running. Didn't make sense not to:
 * </Nudge>
 * ```
 */
const Nudge: React.FC<NudgeProps> = (props) => {
  const {
    UNSAFE_style = {},
    title,
    children,
    actions,
    leading,
    onClose,
    closeButtonProps,
    ...rest
  } = props;
  const hasCloseButton = onClose ? true : false;
  // ---------------
  // Rendering
  // ---------------
  const _renderTitle = () => {
    return (
      <Body
        testID={Nudge.displayName + '-title'}
        size={token.componentNudgeTitleAliasOptionsSize as BodySize}
        weight={`${token.componentNudgeTitleAliasOptionsWeight}` as BodyWeight}>
        {title}
      </Body>
    );
  };

  const _renderContent = () => {
    return (
      children && (
        <Body
          testID={Nudge.displayName + '-content'}
          size={token.componentNudgeContentAliasOptionsSize as BodySize}
          UNSAFE_style={ss(hasCloseButton).contentTextContainer}>
          {children}
        </Body>
      )
    );
  };

  const _renderLeading = (node: React.ReactNode) => {
    return (
      <_Leading
        node={node}
        iconProps={{
          UNSAFE_style: {marginRight: token.componentNudgeLeadingMarginRight},
          testID: Nudge.displayName + '-leading',
        }}
      />
    );
  };

  const renderCloseButton = () => {
    return (
      onClose && (
        <IconButton
          testID={Nudge.displayName + '-close'}
          children={<Icons.CloseIcon />}
          color={token.componentNudgeCloseButtonIconColor}
          size={token.componentNudgeCloseButtonIconSize as IconButtonSize}
          UNSAFE_style={ss(hasCloseButton).closeButton}
          onPress={onClose}
          {...closeButtonProps}
        />
      )
    );
  };

  const _renderActions = () => {
    const kids = flattenChildren(actions);
    return (
      actions && (
        <View
          style={ss(hasCloseButton).actions}
          testID={Nudge.displayName + '-actions'}>
          {kids.map((child, index) => (
            <React.Fragment key={index}>{child}</React.Fragment>
          ))}
        </View>
      )
    );
  };

  return (
    <View
      testID={Nudge.displayName}
      style={[ss(hasCloseButton).root, UNSAFE_style]}
      {...rest}>
      <View style={ss(hasCloseButton).container}>
        {leading ? _renderLeading(leading) : null}
        <View style={ss(hasCloseButton).contentContainer}>
          {_renderTitle()}
          {_renderContent()}
          {_renderActions()}
        </View>
      </View>
      {renderCloseButton()}
    </View>
  );
};

// ---------------
// Styles
// ---------------
const ss = (hasCloseButton: boolean) => {
  return StyleSheet.create({
    root: {
      flexDirection: 'row',
      backgroundColor: token.componentNudgeContainerBackgroundColor,
      borderRadius: token.componentNudgeContainerBorderRadius,
    },
    container: {
      flex: 1,
      flexDirection: 'row',
      paddingVertical: token.componentNudgeContainerPaddingVertical,
      paddingHorizontal: token.componentNudgeContainerPaddingHorizontal,
      paddingRight: hasCloseButton
        ? token.componentNudgeContainerStateHasCloseButtonPaddingEnd
        : token.componentNudgeContainerPaddingHorizontal,
    },
    contentContainer: {
      flex: 1,
    },
    contentTextContainer: {
      marginTop: token.componentNudgeContentMarginTop,
    },
    closeButton: {
      width: token.componentNudgeCloseButtonWidth,
      height: token.componentNudgeCloseButtonHeight,
      tintColor: token.componentNudgeCloseButtonIconColor,
      margin: token.componentNudgeCloseButtonMargin,
    },
    leading: {
      marginRight: token.componentNudgeLeadingMarginEnd,
    },
    actions: {
      flexDirection: 'row',
      flexWrap: 'wrap',
      justifyContent: 'space-between',
      marginTop: token.componentNudgeActionContentMarginTop,
    },
  });
};
Nudge.displayName = 'Nudge';
export {Nudge};
