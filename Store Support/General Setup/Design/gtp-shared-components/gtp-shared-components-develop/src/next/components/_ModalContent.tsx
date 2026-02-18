import * as React from 'react';
import {
  FlexStyle,
  LayoutChangeEvent,
  LayoutRectangle,
  ScrollView,
  StyleProp,
  StyleSheet,
  Text,
  TextStyle,
  TouchableHighlight,
  useWindowDimensions,
  View,
  ViewStyle,
} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Modal';

import {getFont} from '../../theme/font';
import {colors} from '../utils';

export type ModalContentProps = {
  children: React.ReactNode;
  headerTitle?: React.ReactNode;
  keyboardShouldPersistTaps: 'never' | 'always' | 'handled';
  componentName: string | undefined;
  actions?: React.ReactNode;
  contentExtraStyle?: StyleProp<ViewStyle>;
  actionsExtraStyle?: StyleProp<ViewStyle>;
  isSelectModal?: boolean;
};

/**
 * @internal
 */
const _ModalContent: React.FC<ModalContentProps> = (props) => {
  const {
    children,
    keyboardShouldPersistTaps,
    componentName,
    actions,
    contentExtraStyle = {},
    actionsExtraStyle = {},
    isSelectModal = false,
  } = props;

  const {height: deviceHeight} = useWindowDimensions();
  let contentPadding = isSelectModal
    ? token.componentModalContentPaddingBottomBS
    : token.componentModalContentPaddingBottomBM;
  const [containerLayout, setContainerLayout] = React.useState<
    LayoutRectangle | undefined
  >();

  const [actionsLayout, setActionsLayout] = React.useState<
    LayoutRectangle | undefined
  >();

  const [containerHeight, setContainerHeight] = React.useState(0);

  React.useEffect(() => {
    const maxHeight = deviceHeight - 150; // Max Height excludes status bar
    let currentHeight = maxHeight; // Start with max height
    const paddingBottom = isSelectModal
      ? token.componentModalContentPaddingBottomBS
      : token.componentModalContentPaddingBottomBM;
    if (actionsLayout) {
      currentHeight -= actionsLayout.height + paddingBottom / 2; // 16 / 2 = 8
    }

    if (containerLayout) {
      // Adjust modal to content size if smaller than max height
      if (containerLayout.height < currentHeight) {
        currentHeight = containerLayout.height + paddingBottom;
      }
      setContainerHeight(currentHeight);
    }
  }, [deviceHeight, actionsLayout, containerLayout, isSelectModal]);

  const renderActions = () => {
    return (
      <View
        onLayout={(event: LayoutChangeEvent) => {
          const layout = event.nativeEvent.layout;
          setActionsLayout(layout);
        }}
        testID={componentName + '-actions'}
        style={[ss(isSelectModal).actions, actionsExtraStyle]}>
        {React.cloneElement(actions as React.ReactElement, {
          UNSAFE_style: {maxWidth: actionsLayout?.width},
        })}
      </View>
    );
  };

  return (
    <>
      <View
        testID={componentName + '-content'}
        style={[
          ss(isSelectModal).content,
          {height: containerHeight, paddingBottom: contentPadding},
          contentExtraStyle,
        ]}>
        <ScrollView
          style={ss(isSelectModal).innerContent}
          showsVerticalScrollIndicator={false}
          keyboardShouldPersistTaps={keyboardShouldPersistTaps}>
          <TouchableHighlight
            accessible={false}
            onLayout={(event: LayoutChangeEvent) => {
              const layout = event.nativeEvent.layout;
              setContainerLayout(layout);
            }}>
            {typeof children === 'string' ? (
              <Text style={ss(isSelectModal).contentText}>{children}</Text>
            ) : (
              children
            )}
          </TouchableHighlight>
        </ScrollView>
      </View>
      {actions && renderActions()}
    </>
  );
};
_ModalContent.displayName = '_ModalContent';

// ---------------
// Styles
// ---------------
const ss = (isSelectModal: boolean) => {
  return StyleSheet.create({
    content: {
      width: token.componentModalLayoutContainerWidth,
      paddingHorizontal: isSelectModal
        ? token.componentModalContentPaddingHorizontalBS
        : token.componentModalContentPaddingHorizontalBM,
      alignItems: token.componentModalLayoutContainerAlignHorizontal as Extract<
        FlexStyle,
        'alignItems'
      >, //'center'
    },
    innerContent: {
      width: '100%',
    },
    scrollableStyle: {
      width: token.componentModalLayoutContainerWidth, // "100%",
      paddingHorizontal: isSelectModal
        ? token.componentModalContentPaddingHorizontalBS
        : token.componentModalContentPaddingHorizontalBM, // 16,
    },
    contentText: {
      ...getFont(),
      lineHeight: 20,
      color: colors.black,
    } as TextStyle,
    actions: {
      width: '100%',
      flexDirection: 'row',
      justifyContent:
        //token.componentModalActionContentAlignHorizontal as Extract  // "end" // Cory, wrong value here
        'flex-end',
      alignItems: 'flex-end',
      borderTopColor: token.componentModalActionContentBorderColorTop,
      borderTopWidth: token.componentModalActionContentBorderWidthTop,
      paddingVertical: isSelectModal
        ? token.componentModalActionContentPaddingBS
        : token.componentModalActionContentPaddingBM,
      paddingHorizontal: isSelectModal
        ? token.componentModalContentPaddingHorizontalBS
        : token.componentModalContentPaddingHorizontalBM,
    },
  });
};

export {_ModalContent};
