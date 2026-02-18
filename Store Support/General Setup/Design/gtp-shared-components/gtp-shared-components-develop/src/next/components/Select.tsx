/* c8 ignore start */
import * as React from 'react';
import {
  AccessibilityInfo,
  findNodeHandle,
  LayoutAnimation,
  LayoutChangeEvent,
  LayoutRectangle,
  NativeSyntheticEvent,
  PixelRatio,
  Platform,
  Pressable,
  StyleProp,
  StyleSheet,
  TargetedEvent,
  Text,
  TextStyle,
  UIManager,
  useWindowDimensions,
  View,
  ViewProps,
  ViewStyle,
} from 'react-native';

import * as overlayToken from '@livingdesign/tokens/dist/react-native/light/regular/components/Menu';
import * as modalToken from '@livingdesign/tokens/dist/react-native/light/regular/components/Modal';
import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Select';
import * as taToken from '@livingdesign/tokens/dist/react-native/light/regular/components/TextArea';
import {Icons, IconSize} from '@walmart/gtp-shared-icons';
import _ from 'lodash';
import DeviceInfo from 'react-native-device-info';
import RNModal from 'react-native-modal';

import {getFont, Weights} from '../../theme/font';
import {
  CommonPressableProps,
  CommonRNModalBaseProps,
} from '../types/ComponentTypes';
import {
  a11yRole,
  calculateMenuPosition,
  delay,
  useSimpleReducer,
} from '../utils';

import {_LeadingTrailing as _Leading} from './_LeadingTrailing';
import {_Option, OptionSize} from './_Option';
import {BottomSheet} from './BottomSheet';
import {Button} from './Button';
import {ButtonGroup} from './ButtonGroup';
import {Checkbox} from './Checkbox';
import {IconButton, IconButtonSize} from './IconButton';
import {List} from './List';
import {Modal} from './Modal';
import {PopoverPosition} from './Popover';
import {Radio} from './Radio';

// ---------------
// Props
// ---------------
export type SelectSize = 'small' | 'medium' | 'large';
export type SelectionType = 'multi' | 'single' | 'default';
export type SelectOption = {
  text: string;
  selected?: boolean;
  disabled?: boolean;
  extraContent?: React.ReactNode;
};

export type SelectComponentType =
  | 'InlineView'
  | 'BottomSheet'
  | 'Modal'
  | 'Overlay';

export type OSBasedComponentType = {
  ios: SelectComponentType;
  android: SelectComponentType;
};

export type SelectOptions = Array<SelectOption>;
export type SelectProps = CommonPressableProps &
  ViewProps & {
    /**
     * The content for the select.
     * An array of options of type SelectOptions
     *
     * ```
     * export type SelectOptions = Array<{
     *  text: string;
     *  selected?: boolean; // default: false
     *  disabled?: boolean; // default: false
     *  extraContent?: React.ReactNode // default: null. Use this if you need
     *                                 // to trigger the rendering of extra
     *                                 // content under the option (e.g. TextField)
     *                                 // This only applies to selectionType 'multi'
     * }>;
     * ```
     *
     *  Example:
     *
     * ```
     * const selectOptions = [
     *  {text: 'Mug'},
     *  {text: 'Shirt', selected: true},
     *  {text: 'Sticker'},
     *  {text: 'Hat', disabled: true},
     *  {text: 'Hoodie'},
     *  {text: 'Pins', extraContent: <TextField ... />},
     * ];
     * // In the above example, 'Shirt' will be preselected, 'Hat' will be disabled
     * ```
     */
    selectOptions?: SelectOptions;
    /**
     * Whether the Select is disabled.
     *
     * @default false
     */
    disabled?: boolean;
    /**
     * The error message for the Select
     * Displayed under the trigger button.
     */
    error?: React.ReactNode;
    /**
     * The helper text for the Select
     * Displayed under the trigger button.
     */
    helperText?: React.ReactNode;
    /**
     * The label for the Select.
     * Displayed above the trigger button.
     */
    label?: React.ReactNode;
    /**
     * The leading icon for the Select.
     */
    leading?: React.ReactNode;
    /**
     * The placeholder for the Select.
     */
    placeholder: string;
    /**
     * The callback fired when user makes a selection.
     */
    onChange?: (selected: Array<Selected>) => void;
    /**
     * The size for the select.
     *
     * Valid values: 'small' | 'large
     *
     * @default "large"
     */
    size?: SelectSize;
    /**
     * If provided, the <strong>style</strong> to provide to the container.
     * This property is prefixed with <strong>UNSAFE</strong> as its use
     * often results in <strong>unintended side effects</strong>.
     */
    UNSAFE_style?: StyleProp<ViewStyle>;

    //****** NON LD PROPS ******/
    /**
     * Type of component you want rendered.
     * Valid values: any of these combinations are supported:
     * ```
     * {
     *   ios: 'InliveView' | 'BottomSheet' | 'Modal' | 'Overlay',
     *   android: 'InlineView '| 'BottomSheet' | 'Modal | 'Overlay'
     * }
     * ```
     *
     * @default { ios: 'InlineView', android: 'InlineView }
     */
    componentType?: OSBasedComponentType;
    /**
     * The type of selection desired
     * Valid values:
     *
     * 'default' use checkmark single option. (as per LD specs)
     * 'single': use radio single option.
     * 'multi':  use checkbox multiple options.
     *
     * @default 'default'
     */
    selectionType?: SelectionType;
    /**
     * The title for when using a BottomSheet or Modal.
     */
    title?: string;
    /**
     * isInsideModal for when using select inside BottomSheet/Modal.
     * @default false
     */
    isInsideModal?: boolean;
    //*******Required when selectionType is `multi`*******/
    /**
     * The title of the BottomSheet or Modal Done Button for multi choice.
     * Note: the ButtonGroup with Cancel and Done only gets displayed when
     * componentType is 'BottomSheet' or 'Modal' and
     * selectionType is 'multi
     *
     * @default 'Done'
     */
    doneButtonTitle?: string;
    /**
     * The title of the BottomSheet or Modal Cancel Button for multi choice.
     * Note: the ButtonGroup with Cancel and Done only gets displayed when
     * componentType is 'BottomSheet' or 'Modal' and
     * selectionType is 'multi'
     *
     * @default 'Cancel'
     */
    cancelButtonTitle?: string;
    /*
     * The props to pass to the Select when the selections are rendered in a Modal or Overlay.
     */
    modalProps?: CommonRNModalBaseProps;
    /*
     * The props to pass to the Select when the selections are rendered in a BottomSheet.
     */
    bottomSheetProps?: CommonRNModalBaseProps;
    /**
     * The accessible label for the Select.
     */
    accessibilityLabel?: string;

    /**
     * A custom React node to replace the default trigger button.
     * When provided, this custom element will be rendered instead of the default Select button.
     * The custom trigger will maintain the same functionality as the default trigger,
     * including showing/hiding the select options when clicked.
     *
     * @example
     * <Select
     *   trigger={<CustomButton title="Select an option" />}
     *   selectOptions={options}
     *   placeholder="Choose..."
     * />
     *
     * @description
     * The trigger element should be a button or a pressable element.
     * It will receive the necessary props to handle the select's functionality.
     *
     * @note
     * If you're using a custom trigger, make sure to handle the accessibility
     * attributes correctly. You can use the `accessibilityRole` prop to specify
     * the role of the trigger element.
     */
    trigger?: React.ReactNode;
  };

export type Selected = {
  index: number;
  text: string;
};

export type SelectState = {
  value: string | undefined;
  isExpanded: boolean;
  buttonContainerBorderColor: string;
  buttonContainerBorderWidth: number;
  buttonContainerPaddingVertical: number;
  buttonContainerTopBorderRadius: number;
  buttonContainerBottomBorderRadius: number;
  textColor: string;
  labelTextColor: string;
  helperTextColor: string;
};

if (
  Platform.OS === 'android' &&
  UIManager.setLayoutAnimationEnabledExperimental
) {
  UIManager.setLayoutAnimationEnabledExperimental(true);
}
/*
  const selectOptions: SelectOptions = [
    {text: 'Mug'},
    {text: 'Shirt'},
    {
      text: 'Sticker',
    },
    {text: 'Hat - not available', disabled: true},
    {text: 'Hoodie'},
  ];
            <Select
            selectOptions={selectOptions}
            placeholder="Select your swag..."
            label="Swag"
            helperText="Helper text"
            onChange={handleOnChange}
          />
*/

/**
 * Select gives users the ability to select from a
 * number of predefined options. It is usually found in forms.
 *
 * ## Usage
 * ```js
 * import {Select} from '@walmart/gtp-shared-components`;
 *
 * const selectOptions = [
 *   {text: 'Mug'},
 *   {text: 'Shirt'},
 *   {text: 'Sticker'},
 *   {text: 'Hat - not available', disabled: true},
 *   {text: 'Hoodie'},
 * ];
 *
 * const handleOnChange = (selected: Array<Selected>) => {
 *   console.log('---- Picked:', selected);
 * };
 *
 * <Select
 *   selectOptions={selectOptions}
 *   placeholder="Select your swag..."
 *   label="Swag"
 *   helperText="Helper text"
 *   onChange={handleOnChange}
 * />
 * ```
 */
const Select: React.FC<SelectProps> = (props) => {
  const {height: screenHeight, width: screenWidth} = useWindowDimensions();
  const {
    selectOptions = [],
    disabled = false,
    error,
    helperText,
    label,
    placeholder,
    leading,
    onChange,
    componentType = {ios: 'InlineView', android: 'InlineView'},
    size = 'large',
    title,
    doneButtonTitle = 'Done',
    cancelButtonTitle = 'Cancel',
    selectionType = 'default',
    isInsideModal = false,
    modalProps,
    bottomSheetProps,
    UNSAFE_style,
    children,
    accessibilityLabel,
    trigger,
    ...rest
  } = props;

  const errorRef = React.useRef(null);
  React.useEffect(() => {
    if (errorRef && errorRef.current) {
      const reactTag = findNodeHandle(errorRef.current);
      if (reactTag) {
        setTimeout(() => {
          // Due to screen lifecycle, we need to put a minor delay.
          AccessibilityInfo.setAccessibilityFocus(reactTag);
        }, 300);
      }
    }
  }, [errorRef]);

  const [position, setPosition] =
    React.useState<PopoverPosition>('bottomCenter');

  const isSelectedPopulated = React.useCallback(
    (_selected: Array<Selected>) => {
      if (_selected?.length > 0) {
        return true;
      } else {
        return false;
      }
    },
    [],
  );

  const isSelectedInRange = React.useCallback(
    (selected: Array<Selected>, options: SelectOptions) =>
      selected.every(
        (currentSelected) => currentSelected.index < options.length,
      ),
    [],
  );

  const resolveValue = React.useCallback(
    (_selected: Array<Selected>): string => {
      let value = placeholder;
      if (
        isSelectedPopulated(_selected) &&
        isSelectedInRange(_selected, selectOptions)
      ) {
        //to support multi language options text
        const selectedOptions = _selected.map(({index}: Selected) => {
          return {index, text: selectOptions[index].text};
        });
        value = selectedOptions.reduce((accum, curr, idx) => {
          return idx === 0 ? accum : `${accum}, ${curr.text}`;
        }, selectedOptions[0].text);
      }
      return value;
    },
    [isSelectedPopulated, isSelectedInRange, placeholder, selectOptions],
  );

  const initialState: SelectState = {
    value: resolveValue(initialSelectedOptions(selectOptions)),
    isExpanded: false,
    buttonContainerBorderColor: disabled
      ? token.componentSelectContainerBorderColorDisabled
      : token.componentSelectContainerBorderColorDefault, // "#909196"
    buttonContainerBorderWidth: disabled
      ? token.componentSelectContainerBorderWidthDisabled
      : token.componentSelectContainerBorderWidthDefault,
    buttonContainerPaddingVertical:
      (size === 'large'
        ? token.componentSelectContainerSizeLargePaddingVertical
        : token.componentSelectContainerSizeSmallPaddingVertical) -
      token.componentSelectContainerBorderWidthDefault,
    buttonContainerTopBorderRadius: token.componentSelectContainerBorderRadius, // 4;
    buttonContainerBottomBorderRadius:
      token.componentSelectContainerBorderRadius, // 4;
    textColor: disabled
      ? token.componentSelectValueTextColorDisabled
      : token.componentSelectValueTextColorDefault, // "#2e2f32"
    labelTextColor: disabled
      ? token.componentSelectValueTextColorDisabled
      : token.componentSelectValueTextColorDefault,
    helperTextColor: disabled
      ? token.componentSelectValueTextColorDisabled
      : token.componentSelectValueTextColorDefault, // "#2e2f32" // @cory token missing
  };

  const [state, setState] = useSimpleReducer<SelectState>(initialState);
  const [selected, setSelected] = React.useState<Array<Selected>>(
    initialSelectedOptions(selectOptions),
  );

  // This effect synchronizes the selected options when the selectOptions prop changes
  // It performs a deep comparison between the current selected state and the new options
  // to avoid unnecessary re-renders when the options reference changes but values remain the same
  React.useEffect(() => {
    const selectedVal = initialSelectedOptions(selectOptions);
    if (!_.isEqual(selectedVal, selected)) {
      setSelected(selectedVal);
    }
  }, [selectOptions]); // eslint-disable-line react-hooks/exhaustive-deps

  React.useLayoutEffect(() => {
    setState('value', resolveValue(selected));

    if (state.isExpanded) {
      setState(
        'buttonContainerBorderColor',
        error
          ? token.componentSelectContainerStateErrorBorderColorFocus // "#de1c24"
          : token.componentSelectContainerBorderColorFocus, // "#000"
      );
      setState(
        'buttonContainerBorderWidth',
        token.componentSelectContainerBorderWidthFocus,
      );
      setState(
        'buttonContainerPaddingVertical',
        (size === 'large'
          ? token.componentSelectContainerSizeLargePaddingVertical
          : token.componentSelectContainerSizeSmallPaddingVertical) -
          (state.buttonContainerBorderWidth as number),
      );
      setState(
        'buttonContainerTopBorderRadius',
        position.startsWith('bottom')
          ? token.componentSelectContainerBorderRadius
          : 0,
      );
      setState(
        'buttonContainerBottomBorderRadius',
        position.startsWith('top')
          ? token.componentSelectContainerBorderRadius
          : 0,
      );
    } else {
      let borderColor: string = disabled
        ? token.componentSelectContainerBorderColorDisabled
        : token.componentSelectContainerBorderColorDefault; // "#909196"
      borderColor = error
        ? token.componentSelectContainerStateErrorBorderColorDefault // "#de1c24"
        : borderColor;
      setState('buttonContainerBorderColor', borderColor);
      setState(
        'buttonContainerBorderWidth',
        token.componentSelectContainerBorderWidthDefault,
      );
      setState(
        'buttonContainerPaddingVertical',
        (size === 'large'
          ? token.componentSelectContainerSizeLargePaddingVertical
          : token.componentSelectContainerSizeSmallPaddingVertical) -
          (state.buttonContainerBorderWidth as number),
      );
      setState(
        'buttonContainerTopBorderRadius',
        token.componentSelectContainerBorderRadius,
      );
      setState(
        'buttonContainerBottomBorderRadius',
        token.componentSelectContainerBorderRadius,
      );
    }
  }, [
    error,
    disabled,
    resolveValue,
    selected,
    setState,
    size,
    position,
    state.buttonContainerBorderWidth,
    state.isExpanded,
  ]);

  const [multiSelectInProgress, setMultiSelectInProgress] = React.useState<
    boolean | undefined
  >(undefined);
  const [
    allowExtraContentForSingleOption,
    setAllowExtraContentForSingleOption,
  ] = React.useState<boolean>(false);

  React.useEffect(() => {
    if (
      multiSelectInProgress !== undefined &&
      multiSelectInProgress === false
    ) {
      if (selected?.length) {
        onChange?.(selected);
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [multiSelectInProgress, selected]);

  const handleOnBlur = (args: NativeSyntheticEvent<TargetedEvent>) => {
    rest?.onBlur?.(args);
    showHideSelectComponent();
  };

  const handleOnPressOption = async (
    idx: number,
    txt: string,
    extraContent?: React.ReactNode,
  ) => {
    if (selectionType === 'multi') {
      // if index exists in selected, remove it
      if (isIndexInSelected(idx)) {
        setSelected(
          selected.filter((item) => {
            return item.index !== idx;
          }),
        );
      } else {
        // if index is not in selected, add it
        setSelected([...selected, {index: idx, text: txt}]);
      }
      setMultiSelectInProgress(true);
    } else {
      // if selectionType is 'default' or 'single' replace selected
      setSelected([{index: idx, text: txt}]);
      setMultiSelectInProgress(false);
      if (!extraContent) {
        await delay(200); // skip a beat, to allow the checkmark to show
        showHideSelectComponent();
      }
    }
  };

  // For 'multi', we store the previous selected structure, so if the user
  // taps on Cancel, we can restore it
  const [previousMulti, setPreviousMulti] = React.useState<Array<Selected>>(
    initialSelectedOptions(selectOptions),
  );

  const handleMultiDone = async () => {
    setPreviousMulti(selected);
    setMultiSelectInProgress(false);
    await delay(200); // skip a beat, to allow the checkmark to show
    showHideSelectComponent();
  };

  const handleMultiCancel = async () => {
    setSelected(previousMulti);
    setMultiSelectInProgress(undefined);
    await delay(200); // skip a beat, to allow the checkmark to show
    showHideSelectComponent();
  };

  const handleSingleDone = async () => {
    setAllowExtraContentForSingleOption(false);
    await delay(200); // skip a beat, to allow the checkmark to show
    showHideSelectComponent();
  };

  const handleSingleCancel = async () => {
    await delay(200); // skip a beat, to allow the checkmark to show
    showHideSelectComponent();
  };

  const resolveComponentType = React.useCallback(() => {
    return componentType[Platform.OS as 'ios' | 'android'];
  }, [componentType]);

  const showHideSelectComponent = () => {
    const _componentType = resolveComponentType();
    setState('isExpanded', !state.isExpanded);
    if (_componentType === 'InlineView') {
      LayoutAnimation.configureNext(LayoutAnimation.Presets.easeInEaseOut);
    }
  };

  const isIndexInSelected = (idx: number): boolean => {
    let isIn = false;
    isIn = selected.some((item) => {
      if (item.index === idx) {
        return true;
      }
    });
    return isIn;
  };

  // ---------------
  // Rendering
  // ---------------
  let triggerRef = React.useRef<View | null>(null).current;

  const [overlayLayout, setOverlayLayout] = React.useState<
    LayoutRectangle | undefined
  >();

  const [modalPositionStyle, setModalPositionStyle] = React.useState<
    ViewStyle | undefined
  >();

  const hideIfModalPositionNotReady = (): ViewStyle => {
    if (!modalPositionStyle) {
      return {opacity: 0};
    } else {
      return {};
    }
  };

  React.useEffect(() => {
    if (state.isExpanded || resolveComponentType() === 'Overlay') {
      triggerRef?.measure(async (_x, _y, width, height, pageX, pageY) => {
        if (overlayLayout) {
          setPosition(
            calculateMenuPosition(screenWidth, screenHeight, pageX, pageY),
          );
          let adjustedMenuStyle;
          if (position.startsWith('bottom')) {
            adjustedMenuStyle = {
              width: width,
              left: pageX,
              top: await distanceBottomY(isInsideModal, pageY, height),
            };
          } else if (position.startsWith('top')) {
            adjustedMenuStyle = {
              width: width,
              left: pageX,
              top: await distanceTopY(
                isInsideModal,
                pageY,
                overlayLayout.height,
              ),
            };
          }
          setModalPositionStyle(adjustedMenuStyle);
        }
      });
    }
  }, [
    position,
    triggerRef,
    overlayLayout,
    screenHeight,
    screenWidth,
    state.isExpanded,
    isInsideModal,
    resolveComponentType,
  ]);

  const _renderExtraContent = (
    extraContent: React.ReactNode = null,
    _isIndexSelected: boolean = false,
  ) => {
    if (!extraContent || !_isIndexSelected) {
      return null;
    }

    if (!allowExtraContentForSingleOption) {
      setAllowExtraContentForSingleOption(true);
    }

    return (
      <>
        {extraContent}
        {renderButtonGroup([
          ss(size).buttonGroupContainer,
          ss(size).singleButtonMarginTop,
        ] as ViewStyle)}
      </>
    );
  };
  const renderRadioOption = (item: SelectOption, index: number) => {
    const {text, disabled: _disabled = false, extraContent = null} = item;
    const _isIndexSelected = isIndexInSelected(index);
    return (
      <View
        key={`Radio-${index}`}
        testID={`${Select.displayName}-RadioItem-${index}`}>
        <Radio
          key={index}
          UNSAFE_style={ss(size).optionsContainer}
          label={text}
          testID={`${Select.displayName}-radio_${index}`}
          disabled={_disabled}
          checked={_isIndexSelected}
          onPress={() => handleOnPressOption(index, text, extraContent)}
        />
        {_renderExtraContent(extraContent, _isIndexSelected)}
      </View>
    );
  };

  // For 'multi' we are also rendering extraContent after an option, if provided
  // in the selectOptions prop
  const renderCheckBoxOption = (item: SelectOption, index: number) => {
    const {text, disabled: _disabled = false, extraContent = null} = item;
    return (
      <View
        key={`Checkbox-${index}`}
        testID={`${Select.displayName}-CheckboxItem-${index}`}>
        <Checkbox
          UNSAFE_style={ss(size).optionsContainer}
          label={text}
          testID={`${Select.displayName}-checkbox_${index}`}
          disabled={_disabled}
          checked={isIndexInSelected(index)}
          onPress={() => handleOnPressOption(index, text)}
        />
        {isIndexInSelected(index) && extraContent}
      </View>
    );
  };

  const renderDefaultOption = (item: SelectOption, index: number) => {
    const {text, disabled: _disabled = false, extraContent = null} = item;
    const _isIndexSelected = isIndexInSelected(index);

    return (
      <View
        key={`_Option-${index}`}
        testID={`${Select.displayName}-OptionItem-${index}`}>
        <_Option
          key={index}
          size={size as OptionSize}
          index={index}
          text={text}
          testID={`_Option-${index}`}
          isSelected={_isIndexSelected}
          disabled={_disabled}
          onPress={() => handleOnPressOption(index, text)}
        />
        {_renderExtraContent(extraContent, _isIndexSelected)}
      </View>
    );
  };

  const renderButtonGroup = (extraStyle?: ViewStyle) => (
    <ButtonGroup UNSAFE_style={extraStyle}>
      <Button
        variant="tertiary"
        onPress={
          selectionType === 'multi' ? handleMultiCancel : handleSingleCancel
        }>
        {cancelButtonTitle}
      </Button>
      <Button
        variant="primary"
        onPress={
          selectionType === 'multi' ? handleMultiDone : handleSingleDone
        }>
        {doneButtonTitle}
      </Button>
    </ButtonGroup>
  );

  const renderOptionsList = () => {
    return selectionType === 'default' ? (
      <>
        {selectOptions.map((item, index) => {
          return renderDefaultOption(item, index);
        })}
      </>
    ) : (
      <>
        {selectOptions.map((item, index) => {
          return selectionType === 'multi'
            ? renderCheckBoxOption(item, index)
            : renderRadioOption(item, index);
        })}
      </>
    );
  };

  const renderBottomSheet = () => {
    return (
      <BottomSheet
        testID={`${Select.displayName}-bottomSheet`}
        title={title}
        isOpen={state.isExpanded as boolean}
        hideCloseIcon={
          selectionType === 'multi' && isSelectedPopulated(selected)
        }
        onClose={() => setState('isExpanded', false)}
        onBackButtonPress={() => setState('isExpanded', false)}
        actions={
          selectionType === 'multi' && isSelectedPopulated(selected)
            ? renderButtonGroup()
            : null
        }
        {...bottomSheetProps}>
        {renderOptionsList()}
      </BottomSheet>
    );
  };

  const renderModal = () => {
    return (
      <Modal
        testID={`${Select.displayName}-modal`}
        title={title}
        isSelectModal={true}
        isOpen={state.isExpanded as boolean}
        hideCloseIcon={
          selectionType === 'multi' && isSelectedPopulated(selected)
        }
        onClose={() => setState('isExpanded', false)}
        UNSAFE_style={ss(size).modalContainer}
        actions={
          selectionType === 'multi' && isSelectedPopulated(selected)
            ? renderButtonGroup()
            : null
        }
        {...modalProps}>
        {renderOptionsList()}
      </Modal>
    );
  };
  const renderOverlay = () => {
    return (
      <RNModal
        testID={`${Select.displayName}`}
        onLayout={(event: LayoutChangeEvent) => {
          const layout = event.nativeEvent.layout;
          setOverlayLayout(layout);
        }}
        style={[
          ss(size).layoutContainer,
          {paddingBottom: state.buttonContainerPaddingVertical as number},
          modalPositionStyle,
          UNSAFE_style,
        ]}
        // isVisible={state.isOverlayOpen as boolean}
        isVisible={state.isExpanded as boolean}
        onBackdropPress={() =>
          state.isExpanded &&
          resolveComponentType() === 'Overlay' &&
          showHideSelectComponent()
        }
        backdropColor="transparent"
        animationIn="fadeIn"
        animationInTiming={500} // @cory no LD token for animation timing in/out
        animationOut="fadeOut"
        animationOutTiming={500} // @cory no LD token for animation timing in/out
        useNativeDriver={true}
        hideModalContentWhileAnimating={true} // Fixes flicker bug when useNativeDriver: https://github.com/react-native-modal/react-native-modal/issues/268#issuecomment-494768894
        {...rest}
        {...modalProps}>
        <View
          testID={`${Select.displayName}_container`}
          style={[
            ss(size).overlayContentContainer,
            dropdownPositionBasedStyle(position, size),
            hideIfModalPositionNotReady(),
          ]}>
          <List separator={false} UNSAFE_style={ss(size).overlayListContainer}>
            {renderOptionsList()}
          </List>
          {selectionType === 'multi' && isSelectedPopulated(selected)
            ? renderButtonGroup(ss(size).buttonGroupContainer)
            : null}
        </View>
      </RNModal>
    );
  };

  const renderSelectComponent = () => {
    const _componentType = resolveComponentType();
    let _component;
    if (_componentType === 'InlineView' && state.isExpanded) {
      _component = (
        <View style={ss(size).dropdownContainer}>
          <List
            separator={false}
            UNSAFE_style={[ss(size).overlayListContainer]}>
            {renderOptionsList()}
          </List>
          {selectionType === 'multi' && isSelectedPopulated(selected)
            ? renderButtonGroup(ss(size).buttonGroupContainer)
            : null}
        </View>
      );
    } else if (_componentType === 'BottomSheet') {
      _component = renderBottomSheet();
    } else if (_componentType === 'Modal') {
      _component = renderModal();
    } else if (_componentType === 'Overlay') {
      _component = renderOverlay();
    }
    return _component;
  };

  const getAccessibilityLabel = () => {
    if (accessibilityLabel) {
      if (!accessibilityLabel.includes('combobox')) {
        // If the accessibilityLabel does not include 'combobox', append it
        // to ensure it is accessible as a combobox.
        return `${accessibilityLabel} ${a11yRole('combobox')}`;
      }
      return accessibilityLabel;
    }
    if (state.value) {
      return `${state.value} ${a11yRole('combobox')}`;
    }
    return placeholder;
  };

  return (
    <View>
      <View
        accessible={true}
        accessibilityState={{expanded: state.isExpanded as boolean}}
        accessibilityLabel={getAccessibilityLabel()}
        testID={Select.displayName}
        style={[ss(size).container, UNSAFE_style]}>
        {renderLabel(size, state as SelectState, label)}
        {trigger ? (
          <Pressable onPress={showHideSelectComponent}>{trigger}</Pressable>
        ) : (
          <View
            testID={Select.displayName + '-button-container'}
            ref={(element) => (triggerRef = element)}
            style={[
              ss(size).buttonContainer,
              {
                color: state.textColor,
                borderWidth: state.buttonContainerBorderWidth as number,
                borderColor: state.buttonContainerBorderColor,
                borderBottomLeftRadius: state.buttonContainerBottomBorderRadius,
                borderBottomRightRadius:
                  state.buttonContainerBottomBorderRadius,
                borderTopLeftRadius: state.buttonContainerTopBorderRadius,
                borderTopRightRadius: state.buttonContainerTopBorderRadius,
              } as TextStyle,
            ]}>
            <Pressable
              accessibilityElementsHidden={true}
              importantForAccessibility="no"
              testID={Select.displayName + '-button'}
              disabled={disabled}
              style={[
                ss(size).button,
                {
                  marginVertical:
                    state.buttonContainerPaddingVertical as number,
                },
              ]}
              onPress={showHideSelectComponent}
              onBlur={handleOnBlur}>
              {leading
                ? renderLeading(leading, state as SelectState, disabled, size)
                : null}
              {renderValue(state.value as string, state as SelectState, size)}
            </Pressable>
            {renderChevron(
              state as SelectState,
              disabled,
              showHideSelectComponent,
            )}
          </View>
        )}
      </View>
      {state.isExpanded && resolveComponentType() === 'InlineView'
        ? null
        : renderHelperTextAndError(
            size,
            state as SelectState,
            error,
            helperText,
            errorRef,
          )}
      {renderSelectComponent()}
    </View>
  );
};

// ---------------
// Styles
// ---------------
const ss = (size: SelectSize) => {
  return StyleSheet.create({
    layoutContainer: {
      width: '100%',
      maxHeight: 300,
      position: 'absolute',
      padding: 0,
      margin: 0, // Removes default margin on react-native-modal
      zIndex: parseInt(overlayToken.componentMenuLayoutContainerZIndex, 10), // @cory should be number instead of string // 300
    },
    container: {
      alignItems: 'flex-start',
    },
    modalContainer: {
      alignItems: 'flex-start',
    },
    optionsContainer: {
      justifyContent: 'flex-start',
      alignItems: 'center',
      backgroundColor: token.componentSelectContainerBackgroundColor, // "#fff"
      paddingVertical: 4,
    },
    buttonContainer: {
      ...getFont(),
      justifyContent: 'space-between',
      backgroundColor: token.componentSelectContainerBackgroundColor, // "#fff"
      flexDirection: 'row',
      alignItems: 'center',
      borderRadius: token.componentSelectContainerBorderRadius, // 4 (see CEEMP-2802)
    },
    button: {
      flex: 1,
      height: '100%',
      flexDirection: 'row',
      justifyContent: 'flex-start',
      alignItems: 'center',
      marginLeft:
        size === 'large'
          ? token.componentSelectLeadingIconSizeLargeOffsetStart // 16,
          : token.componentSelectLeadingIconSizeSmallOffsetStart, // 12,
      paddingRight: 8,
    },
    value: {
      ...getFont(token.componentSelectValueFontWeight.toString() as Weights), // "400"
      fontSize:
        size === 'large'
          ? token.componentSelectValueSizeLargeFontSize // 16
          : token.componentSelectValueSizeSmallFontSize, // 14
      lineHeight:
        size === 'large'
          ? token.componentSelectValueSizeLargeLineHeight // 24
          : token.componentSelectValueSizeSmallLineHeight, // 24
    } as TextStyle,
    labelContainer: {
      marginBottom: token.componentSelectTextLabelMarginBottom, // 4
    },
    label: {
      ...getFont('bold'), // @cory token missing
      fontSize: size === 'small' ? 12 : 14, // @cory Label FontSize is missing,
      lineHeight: size === 'small' ? 16 : 20, // @cory Label line hight is missing,
    } as TextStyle,
    helperTextAndErrorContainer: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      alignItems: 'center',
    },
    errorContainer: {
      flex: 1,
      flexDirection: 'row',
      justifyContent: 'flex-start',
      alignItems: 'center',
    },
    helperText: {
      // @cory I had to pull the helper text font tokens from TextArea
      ...getFont(
        taToken.componentTextAreaMaxLengthFontWeight.toString() as Weights,
      ), // "400" // @cory token missing
      fontSize: taToken.componentTextAreaMaxLengthFontSize, // 12 // @cory token missing
      lineHeight: taToken.componentTextAreaMaxLengthLineHeight, // 16, // @cory token missing
      marginTop: token.componentSelectHelperTextMarginTop, // 4
    } as TextStyle,

    errorText: {
      // @cory I had to pull the error font tokens from TextArea
      ...getFont(
        taToken.componentTextAreaMaxLengthFontWeight.toString() as Weights,
      ), // "400"
      fontSize: taToken.componentTextAreaMaxLengthFontSize, // 12 // Cory, token missing
      color: token.componentSelectContainerStateErrorBorderColorDefault, // "#de1c24" // Cory, token missing
      marginTop: token.componentSelectHelperTextMarginTop, // 4
    } as TextStyle,
    leading: {
      marginRight: size === 'large' ? 12 : 8, // Cory, token missing
    },
    chevronContainer: {
      marginRight: size === 'large' ? 16 : 12, // Cory, token missing
    },
    dropdownContainer: {
      maxHeight: 300,
      paddingBottom: 5,
      borderBottomLeftRadius: modalToken.componentModalContainerBorderRadius,
      borderBottomRightRadius: modalToken.componentModalContainerBorderRadius,
      backgroundColor: modalToken.componentModalContainerBackgroundColor,
      borderBottomWidth: token.componentSelectContainerBorderWidthDefault, // 1
      borderLeftWidth: token.componentSelectContainerBorderWidthDefault, // 1
      borderRightWidth: token.componentSelectContainerBorderWidthDefault, // 1
      borderColor: token.componentSelectContainerBorderColorDisabled, // "#babbbe"
    },
    topDropdownContainer: {
      paddingTop: 5,
      borderTopLeftRadius: modalToken.componentModalContainerBorderRadius,
      borderTopRightRadius: modalToken.componentModalContainerBorderRadius,
      backgroundColor: modalToken.componentModalContainerBackgroundColor,
      borderTopWidth: token.componentSelectContainerBorderWidthDefault, // 1
      borderLeftWidth: token.componentSelectContainerBorderWidthDefault, // 1
      borderRightWidth: token.componentSelectContainerBorderWidthDefault, // 1
      borderColor: token.componentSelectContainerBorderColorDisabled, // "#babbbe"
    },
    overlayContentContainer: {
      maxHeight: 300,
      backgroundColor: overlayToken.componentMenuContainerBackgroundColor,
    },
    overlayListContainer: {
      maxHeight: 250,
    },
    buttonGroupContainer: {
      width: '100%',
      maxHeight: 42,
      justifyContent: 'flex-end',
      paddingBottom: 4,
    },
    singleButtonMarginTop: {
      marginTop: 8,
    },
  });
};

Select.displayName = 'Select';
export {Select};

// ---------------
// Render helpers
// (extracted and exported separately to facilitate testing)
// ---------------
export const renderLabel = (
  _size: SelectSize,
  _state: SelectState,
  _label: React.ReactNode,
) => {
  return (
    <View
      accessibilityRole={a11yRole('text')}
      testID={Select.displayName + '-label-container'}
      style={ss(_size).labelContainer}>
      {typeof _label === 'string' ? (
        <Text
          style={[ss(_size).label, {color: _state.labelTextColor} as TextStyle]}
          nativeID={`${Select.displayName}-label`}>
          {_label}
        </Text>
      ) : (
        <>{_label}</>
      )}
    </View>
  );
};

const renderError = (
  _error: React.ReactNode,
  style: any,
  _errorRef: React.MutableRefObject<null>,
) => {
  return (
    <View style={style.errorContainer}>
      <Icons.ExclamationCircleFillIcon color="red" />
      {typeof _error === 'string' ? (
        <Text
          ref={_errorRef}
          accessibilityRole={a11yRole('text')}
          style={style.errorText as TextStyle}>
          {_error}
        </Text>
      ) : (
        <>{_error}</>
      )}
    </View>
  );
};

const renderHelperText = (
  _helperText: React.ReactNode,
  style: any,
  _helperTextColor: string,
) => {
  return _helperText ? (
    typeof _helperText === 'string' ? (
      <Text
        accessibilityRole={a11yRole('text')}
        style={[style.helperText, {color: _helperTextColor} as TextStyle]}>
        {_helperText}
      </Text>
    ) : (
      <>{_helperText}</>
    )
  ) : null;
};

export const renderHelperTextAndError = (
  _size: SelectSize,
  _state: SelectState,
  _error: React.ReactNode,
  _helperText: React.ReactNode,
  _errorRef: React.MutableRefObject<null>,
) => {
  return (
    <>
      <View style={ss(_size).helperTextAndErrorContainer}>
        {_error
          ? renderError(_error, ss(_size), _errorRef)
          : renderHelperText(_helperText, ss(_size), _state.helperTextColor)}
      </View>
    </>
  );
};

//Test purpose only exporting
export const dropdownPositionBasedStyle = (
  position: PopoverPosition,
  size: SelectSize,
): ViewStyle => {
  const style = ss(size);
  return position.startsWith('top')
    ? style.topDropdownContainer
    : style.dropdownContainer;
};

export const renderLeading = (
  node: React.ReactNode,
  _state: SelectState,
  disabled: boolean,
  size: SelectSize,
) => {
  let leadIconColor: string = _state.isExpanded
    ? token.componentSelectIconIconColorFocus
    : token.componentSelectLeadingIconIconColor;
  leadIconColor = disabled
    ? token.componentSelectLeadingIconStateDisabledIconColor
    : leadIconColor;
  return (
    <_Leading
      node={node}
      iconProps={{
        UNSAFE_style: ss(size).leading,
        color: leadIconColor,
        size: token.componentSelectIconIconSize as IconSize, // "medium"
      }}
    />
  );
};

export const renderChevron = (
  _state: SelectState,
  disabled: boolean,
  showHideSelectComponent: () => void,
) => {
  let chevronIconColor: string = _state.isExpanded
    ? token.componentSelectIconIconColorFocus // "#000"
    : token.componentSelectIconIconColorDefault; // "#000"
  chevronIconColor = disabled
    ? token.componentSelectIconIconColorDisabled
    : chevronIconColor;

  const iconProps = {
    color: chevronIconColor,
  };

  return (
    <IconButton
      accessibilityElementsHidden={true}
      importantForAccessibility="no"
      disabled={disabled}
      size={token.componentSelectIconIconSize as IconButtonSize} // "medium"
      onPress={showHideSelectComponent}>
      {_state.isExpanded ? (
        <Icons.CaretUpIcon {...iconProps} />
      ) : (
        <Icons.CaretDownIcon {...iconProps} />
      )}
    </IconButton>
  );
};

export const renderValue = (
  _value: string,
  _state: SelectState,
  size: SelectSize,
) => {
  return (
    <Text
      testID={`${Select.displayName}-value`}
      style={[ss(size).value, {color: _state.textColor} as TextStyle]}>
      {_value}
    </Text>
  );
};

//Test purpose only exporting
export const initialSelectedOptions = (
  selectOptions: Array<SelectOption>,
): Array<Selected> => {
  const indexedItems = selectOptions.map((item: SelectOption, index) => {
    return {index, text: item.text, selected: item.selected};
  });
  const selectedItems = indexedItems.filter(
    (item: SelectOption) => item.selected,
  );
  return selectedItems as Array<Selected>;
};
//when we use inside modal/BottomSheet we need to calculate the gap from the parent screen
//real Device 47 Android only
//emulator 38 Android only
//triggers when the overlay position is on bottom of the trigger
export const distanceBottomY = async (
  isInsideModal: boolean,
  pageY: number,
  triggerHeight: number,
) => {
  let distanceFromY = pageY + triggerHeight;
  if (Platform.OS === 'android' && isInsideModal) {
    const isInEmulator = await DeviceInfo.isEmulator();
    if (isInEmulator) {
      distanceFromY = distanceFromY - triggerHeight / 2 + 4;
    } else {
      distanceFromY = distanceFromY - triggerHeight / 2 - 6.5;
    }
  }

  return PixelRatio.roundToNearestPixel(distanceFromY);
};

//real Device -3 Android only
//emulator 6 Android only
//triggers when the overlay position is on top of the trigger
export const distanceTopY = async (
  isInsideModal: boolean,
  pageY: number,
  overlayLayoutHeight: number,
) => {
  let distanceFromTopY = pageY - overlayLayoutHeight;
  if (isInsideModal) {
    if (Platform.OS === 'android') {
      const isInEmulator = await DeviceInfo.isEmulator();
      if (isInEmulator) {
        distanceFromTopY = distanceFromTopY - 10;
      } else {
        distanceFromTopY = distanceFromTopY - 20.5;
      }
    } else {
      distanceFromTopY = distanceFromTopY + 14;
    }
  } else {
    distanceFromTopY = distanceFromTopY + 13.5;
  }

  return PixelRatio.roundToNearestPixel(distanceFromTopY);
};
/* c8 ignore stop */
