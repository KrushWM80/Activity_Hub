import {Platform} from 'react-native';

import {colors, composeTheme, deepMerge} from '../next/utils';
import {getFont} from '../theme/font';

const textField_Filled = {
  labelContainer: {
    display: 'flex',
    position: 'absolute',
    top: 8,
    left: 0,
    right: 0,
  },
  inputContainer: {
    flex: 1,
    paddingTop: 20,
    paddingBottom: 0,
  },
  inputHitSlop: {
    top: 20,
    left: 0,
    right: 0,
    bottom: 0,
  },
};
const textField_Active = {
  fieldContainer: {
    paddingBottom: 0,
    borderBottomWidth: 2,
    borderBottomColor: colors.black,
  },
  leadingIcon: {
    tintColor: colors.black,
  },
  labelContainer: {
    display: 'flex',
    position: 'absolute',
    top: 8,
    left: 0,
    right: 0,
  },
  label: {
    color: colors.black,
  },
  inputContainer: {
    flex: 1,
    paddingTop: 20,
    paddingBottom: 0,
  },
  inputHitSlop: {
    top: 20,
    left: 0,
    right: 0,
    bottom: 0,
  },
};
const textField_Error = {
  fieldContainer: {
    borderBottomColor: colors.red['100'],
  },
  helper: {
    color: colors.red['100'],
  },
  counter: {
    color: colors.red['100'],
  },
};
const textField_Success = {
  fieldContainer: {
    borderBottomColor: colors.green['100'],
  },
  helper: {
    color: colors.green['100'],
  },
};
const textField_LineHeight = 24;

const textField = {
  static: {
    iconSize: 24,
    helperLines: 1,
    stateIconContainer: {
      marginLeft: 4,
    },
    successIcon: {
      tintColor: colors.green['100'],
    },
    errorIcon: {
      tintColor: colors.red['100'],
    },
    underlayColor: colors.gray['20'],
    lineHeight: textField_LineHeight,
  },
  default: {
    placeholder: colors.gray['100'],
    container: {
      backgroundColor: colors.white,
      marginBottom: 16,
    },
    fieldContainer: {
      flexDirection: 'row',
      paddingBottom: 1,
      borderBottomWidth: 1,
      borderBottomColor: colors.gray['80'],
    },
    leadingIconContainer: {
      marginVertical: 14,
      marginRight: 12,
    },
    leadingIcon: {
      tintColor: colors.gray['80'],
    },
    labelContainer: {
      display: 'none',
      position: 'relative',
      top: 0,
      left: 0,
      right: 0,
    },
    label: {
      color: colors.gray['100'],
      fontSize: 12,
      lineHeight: 16,
    },
    inputContainer: {
      flex: 1,
      paddingTop: 10,
      paddingBottom: 10,
    },
    inputHitSlop: {
      top: 10,
      left: 0,
      right: 0,
      bottom: 10,
    },
    input: {
      ...getFont(),
      color: colors.black,
      textAlignVertical: 'top',
      fontSize: 16,
      lineHeight: textField_LineHeight,
      paddingTop: 0,
      paddingBottom: 0,
      paddingHorizontal: 0,
      marginVertical: 5,
      minHeight: textField_LineHeight,
      ...(Platform.OS === 'android'
        ? {
            height: 'auto',
          }
        : {}),
    },
    trailingIconContainer: {
      alignSelf: 'center',
      marginVertical: 14,
      marginLeft: 12,
      borderRadius: 9999,
    },
    trailingLinkContainer: {
      marginVertical: 14,
      marginLeft: 12,
    },
    trailingLink: {
      paddingVertical: 2,
    },
    helperContainer: {
      marginTop: 4,
      flexDirection: 'row',
      alignItems: 'center',
    },
    helper: {
      color: colors.gray['100'],
      fontSize: 12,
      lineHeight: 16,
    },
    counter: {
      flexGrow: 1,
      textAlign: 'right',
      color: colors.gray['100'],
    },
  },
  disabled: {
    placeholder: colors.gray['50'],
    leadingIcon: {
      tintColor: colors.gray['50'],
    },
    input: {
      color: colors.gray['50'],
    },
    trailingIcon: {
      tintColor: colors.gray['50'],
    },
    helper: {
      color: colors.gray['50'],
    },
  },
  filled: textField_Filled,
  active: textField_Active,
  error: textField_Error,
  success: textField_Success,
  errorFilled: deepMerge(textField_Filled, textField_Error),
  errorActive: deepMerge(textField_Active, textField_Error),
  successFilled: deepMerge(textField_Filled, textField_Success),
  successActive: deepMerge(textField_Active, textField_Success),
};

const checkbox_checked = {
  container: {
    backgroundColor: colors.black,
  },
  icon: {
    tintColor: colors.white,
  },
};
const checkbox_checkedDisabled = deepMerge(checkbox_checked, {
  container: {
    borderColor: colors.gray['50'],
    backgroundColor: colors.gray['50'],
  },
});
const checkbox = {
  static: {
    iconSize: 16,
  },
  default: {
    container: {
      borderRadius: 4,
      borderWidth: 1,
      borderColor: colors.black,
      borderStyle: 'solid',
      backgroundColor: colors.white,
      height: 16,
      width: 16,
    },
    icon: {
      tintColor: colors.black,
      margin: -1,
    },
  },
  disabled: {
    container: {
      borderColor: colors.gray['50'],
    },
  },
  checked: checkbox_checked,
  checkedDisabled: checkbox_checkedDisabled,
  indeterminate: checkbox_checked,
  indeterminateDisabled: checkbox_checkedDisabled,
};

const checkboxItem_checked = {
  label: {
    ...getFont('bold'),
  },
};
const checkboxItem_checkedDisabled = deepMerge(checkboxItem_checked, {
  label: {
    color: colors.gray['50'],
  },
});
const checkboxItem = {
  default: {
    container: {
      paddingVertical: 12,
      paddingHorizontal: 16,
      flexDirection: 'row',
      alignItems: 'flex-start',
    },
    checkbox: {
      marginVertical: 2,
      marginRight: 12,
    },
    label: {
      color: colors.gray['140'],
      flexShrink: 1,
    },
  },
  disabled: {
    label: {
      color: colors.gray['50'],
      fontSize: 14,
      lineHeight: 20,
    },
  },
  checked: checkboxItem_checked,
  checkedDisabled: checkboxItem_checkedDisabled,
  indeterminate: checkboxItem_checked,
  indeterminateDisabled: checkboxItem_checkedDisabled,
};

const radio_checked = {
  indicator: {
    backgroundColor: colors.black,
  },
};
const radio_checkedDisabled = deepMerge(radio_checked, {
  container: {
    borderColor: colors.gray['50'],
    borderStyle: 'solid',
    backgroundColor: colors.white,
  },
  indicator: {
    backgroundColor: colors.gray['50'],
  },
});
const radio = {
  default: {
    container: {
      borderRadius: 9999,
      borderWidth: 1,
      borderColor: colors.black,
      borderStyle: 'solid',
      backgroundColor: colors.white,
      height: 20,
      width: 20,
    },
    indicator: {
      borderRadius: 9999,
      backgroundColor: colors.white,
      height: 12,
      width: 12,
      margin: 3,
    },
  },
  disabled: {
    container: {
      borderColor: colors.gray['50'],
    },
  },
  checked: radio_checked,
  checkedDisabled: radio_checkedDisabled,
};

const segmented = {
  default: {
    container: {
      borderRadius: 4,
      padding: 2,
      backgroundColor: colors.gray['20'],
      flexDirection: 'row',
      alignItems: 'stretch',
    },
  },
  disabled: {},
};

const segmentedSmall = segmented;

const segment = {
  default: {
    container: {
      borderRadius: 4,
      paddingVertical: 8,
      flex: 1,
      alignSelf: 'stretch',
      justifyContent: 'center',
    },
    text: {
      ...getFont(),
      fontSize: 14,
      lineHeight: 20,
      color: colors.black,
      textAlign: 'center',
    },
  },
  disabled: {
    text: {
      color: colors.gray['50'],
    },
  },
  selected: {
    container: {
      backgroundColor: colors.white,
    },
    text: {
      ...getFont('bold'),
    },
  },
  selectedDisabled: {
    container: {
      backgroundColor: colors.white,
    },
    text: {
      ...getFont('bold'),
      color: colors.gray['50'],
    },
  },
};

const segmentSmall = deepMerge(segment, {
  default: {
    container: {
      paddingVertical: 4,
    },
  },
});

const toggle = {
  default: {
    container: {},
    off: {
      tintColor: colors.gray['100'],
      thumbTintColor: colors.white,
    },
    on: {
      tintColor: colors.blue['100'],
      thumbTintColor: colors.blue['100'],
    },
  },
  disabled: {
    off: {
      tintColor: colors.gray['10'],
      thumbTintColor: colors.gray['50'],
      background: colors.gray['100'],
    },
    on: {
      tintColor: colors.gray['10'],
      thumbTintColor: colors.gray['50'],
      background: colors.gray['100'],
    },
  },
};

const toggleItem = {
  default: {
    container: {
      flexDirection: 'row',
      alignItems: 'center',
      paddingVertical: 12,
      paddingHorizontal: 16,
    },
    toggle: {},
    label: {
      ...getFont(),
      fontSize: 16,
      lineHeight: 24,
      color: colors.gray['140'],
      flex: 1,
      paddingRight: 8,
    },
  },
  disabled: {
    label: {
      color: colors.gray['50'],
    },
  },
};

const toggleSmall = deepMerge(toggle, {
  default: {
    container: {
      transform: [{scale: 0.5}],
      marginHorizontal: -12,
    },
  },
});

const toggleItemSmall = deepMerge(toggleItem, {
  default: {
    label: {
      paddingRight: 0,
      paddingLeft: 8,
      flex: 0,
      flexShrink: 1,
      fontSize: 12,
      lineHeight: 16,
    },
  },
});

const picker = {
  static: {
    container: {
      backgroundColor: colors.white,
      marginBottom: -100,
      paddingBottom: 100,
    },
    actionBar: {
      paddingHorizontal: 16,
      borderColor: '#e1e0e0',
      borderWidth: 0,
      borderTopWidth: 1,
      borderBottomWidth: 1,
      borderStyle: 'solid',
      backgroundColor: '#fafaf8',
      alignItems: 'center',
      flexDirection: 'row',
    },
    action: {
      paddingVertical: 9,
      marginRight: 8,
    },
    actionIcon: {
      tintColor: '#007aff',
    },
    actionText: {
      fontSize: 15,
      lineHeight: 24,
      color: '#007aff',
      alignSelf: 'flex-end',
    },
    spacer: {
      flex: 1,
    },
  },
};
const theme = {
  form: {
    textField,
    checkbox,
    checkboxItem,
    radio,
    segmented,
    segment,
    segmentedSmall,
    segmentSmall,
    toggle,
    toggleSmall,
    toggleItem,
    toggleItemSmall,
    picker,
  },
};

export default theme;
export const composed = composeTheme(theme);
