import * as React from 'react';
import {
  ImageStyle,
  LayoutAnimation,
  Pressable,
  StyleSheet,
  TextStyle,
  View,
} from 'react-native';

import {Icons} from '@walmart/gtp-shared-icons';

import {getFont} from '../../theme/font';

import {Body} from './Body';
import {CollapseProps} from './Collapse';
import {Divider} from './Divider';
// ---------------
// Props
// ---------------

export type SeeDetailsProps = Omit<
  CollapseProps,
  'title' | 'subtitle' | 'icon'
> & {
  /**
   * Title text for this SeeDetails while hiding content.  If not set, "See Details" will be used.
   * @default 'See Details'
   */
  showText?: string;
  /**
   * Title text for this SeeDetails while showing content  If not set, "Hide Details" will be used.
   * @default 'Hide Details'
   */
  hideText?: string;
};

/**
 * The SeeDetails component is used to put long sections of information under a block that users can expand or collapse.
 *
 * ## Usage
 * ```js
 * import {SeeDetails} from '@walmart/gtp-shared-components`;
 *
 * const [expanded, setExpanded] = React.useState(false);
 *
 * <SeeDetails
 *   title="Single Line Collapse"
 *   onToggle={() => setExpanded(!expanded)}
 * >
 *   <Body>Collapse content appears underneath the toggle area.</Body>
 * </SeeDetails>
 * ```
 */
const SeeDetails: React.FC<SeeDetailsProps> = (props) => {
  const {
    expanded = false,
    children,
    dividerTop = false,
    dividerBottom = false,
    onToggle,
    touchableProps,
    icon_style,
    hideText = 'Hide Details',
    showText = 'See Details',
    title_style,
    size = 24,
    UNSAFE_style,
    ...rest
  } = props;

  // ---------------
  // Rendering
  // ---------------
  const renderDetails = () => {
    if (!expanded) {
      return null;
    }
    return (
      <View style={ss.details} testID={`${SeeDetails.displayName}-details`}>
        {children}
      </View>
    );
  };

  const chevron = React.useMemo(() => {
    if (expanded) {
      return (
        <Icons.ChevronUpIcon
          size={size}
          UNSAFE_style={[ss.chevron, icon_style]}
        />
      );
    }

    return (
      <Icons.ChevronDownIcon
        size={size}
        UNSAFE_style={[ss.chevron, icon_style]}
      />
    );
  }, [expanded, icon_style, size]);
  const showHideSeeDetailsComponent = () => {
    onToggle(!expanded);
    LayoutAnimation.configureNext(LayoutAnimation.Presets.easeInEaseOut);
  };

  return (
    <View
      style={[ss.container, UNSAFE_style]}
      testID={SeeDetails.displayName}
      {...rest}>
      {dividerTop && (
        <Divider testID={`${SeeDetails.displayName}-dividerTop`} />
      )}
      {renderDetails()}
      <Pressable
        accessibilityRole={!process.env.STYLEGUIDIST_ENV ? 'button' : undefined}
        accessibilityState={{expanded}}
        testID={`${SeeDetails.displayName}-trigger`}
        onPress={() => {
          showHideSeeDetailsComponent();
        }}
        {...touchableProps}
        style={[ss.touchable, touchableProps?.style]}>
        <Body
          UNSAFE_style={[ss.title, title_style]}
          testID={`${SeeDetails.displayName}-title`}>
          {expanded ? hideText : showText}
        </Body>
        {chevron}
      </Pressable>
      {dividerBottom && (
        <Divider testID={`${SeeDetails.displayName}-dividerBottom`} />
      )}
    </View>
  );
};

// ---------------
// Styles
// ---------------

const ss = StyleSheet.create({
  container: {
    flex: 1,
  },
  touchable: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
  },
  title: {
    ...getFont('bold'),
    fontSize: 16,
    lineHeight: 24,
  } as TextStyle,
  chevron: {
    marginLeft: 8,
  } as ImageStyle,
  details: {
    paddingTop: 16,
    paddingBottom: 0,
    paddingHorizontal: 16,
  },
});

SeeDetails.displayName = 'SeeDetails';
export {SeeDetails};
