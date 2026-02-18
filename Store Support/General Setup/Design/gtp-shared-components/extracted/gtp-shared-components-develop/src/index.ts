// Note: for icons we want to ensure backwards compatibility,
// hence the double import
// - the first makes icons still import-able individually,
// - the second, makes icons importable in bulk as Icons object)
export * from '@walmart/gtp-shared-icons/dist/icons';
export {Icons} from '@walmart/gtp-shared-icons';

export {colors, contrastColors, delay} from './next/utils';
export * from './theme/font';

// Refactored/LD3 aligned components
export {Alert} from './next/components/Alert';
export {Badge} from './next/components/Badge';
export {Banner} from './next/components/Banner';
export {Body} from './next/components/Body';
export {BottomSheet} from './next/components/BottomSheet';
export {ButtonGroup} from './next/components/ButtonGroup';
export {Button} from './next/components/Button';
export {Callout} from './next/components/Callout';
export {Caption} from './next/components/Caption';
export {CardActions} from './next/components/CardActions';
export {CardContent} from './next/components/CardContent';
export {CardHeader} from './next/components/CardHeader';
export {CardMedia} from './next/components/CardMedia';
export {Card} from './next/components/Card';
export {Checkbox} from './next/components/Checkbox';
export {ChipGroup} from './next/components/ChipGroup';
export {Chip} from './next/components/Chip';
export {CircularProgressIndicator} from './next/components/CircularProgressIndicator';
export {Collapse} from './next/components/Collapse';
export {DataTableBody} from './next/components/DataTableBody';
export {DataTableBulkActions} from './next/components/DataTableBulkActions';
export {DataTableCellActionsMenuItem} from './next/components/DataTableCellActionsMenuItem';
export {DataTableCellActionsMenu} from './next/components/DataTableCellActionsMenu';
export {DataTableCellActions} from './next/components/DataTableCellActions';
export {DataTableCellSelect} from './next/components/DataTableCellSelect';
export {DataTableCellStatus} from './next/components/DataTableCellStatus';
export {DataTableCell} from './next/components/DataTableCell';
export {DataTableHeaderSelect} from './next/components/DataTableHeaderSelect';
export {DataTableHeader} from './next/components/DataTableHeader';
export {DataTableHead} from './next/components/DataTableHead';
export {DataTableRow} from './next/components/DataTableRow';
export {DataTable} from './next/components/DataTable';
export {DateDropdown} from './next/components/DateDropdown';
export {Display} from './next/components/Display';
export {Divider} from './next/components/Divider';
export {ErrorMessage} from './next/components/ErrorMessage';
export {FormGroup} from './next/components/FormGroup';
export {Heading} from './next/components/Heading';
export {IconButton} from './next/components/IconButton';
export {Link} from './next/components/Link';
export {ListItem} from './next/components/ListItem';
export {List} from './next/components/List';
export {LivingDesignProvider} from './next/components/LivingDesignProvider';
export {MenuItem} from './next/components/MenuItem';
export {Menu} from './next/components/Menu';
export {MetricGroup} from './next/components/MetricGroup';
export {Metric} from './next/components/Metric';
export {Modal} from './next/components/Modal';
export {Nudge} from './next/components/Nudge';
export {Popover} from './next/components/Popover';
export {ProgressIndicator} from './next/components/ProgressIndicator';
export {ProgressTrackerItem} from './next/components/ProgressTrackerItem';
export {ProgressTracker} from './next/components/ProgressTracker';
export {Radio} from './next/components/Radio';
export {Rating} from './next/components/Rating';
export {SeeDetails} from './next/components/SeeDetails';
export {Segmented} from './next/components/Segmented';
export {Segment} from './next/components/Segment';
export {Select} from './next/components/Select';
export {SkeletonText} from './next/components/SkeletonText';
export {Skeleton} from './next/components/Skeleton';
export {Snackbar} from './next/components/Snackbar';
export {SpinnerOverlay} from './next/components/SpinnerOverlay';
export {Spinner} from './next/components/Spinner';
export {SpotIcon} from './next/components/SpotIcon';
export {StyledText} from './next/components/StyledText';
export {Switch} from './next/components/Switch';
export {TabNavigationItem} from './next/components/TabNavigationItem';
export {TabNavigation} from './next/components/TabNavigation';
export {Tag} from './next/components/Tag';
export {TextArea} from './next/components/TextArea';
export {TextField} from './next/components/TextField';
export {Variants} from './next/components/Variants';
export {WizardFooter} from './next/components/WizardFooter';
export {useSnackbar} from './next/utils/useSnackbar';

// Refactored/LD3 aligned types
export type {AlertVariant, AlertProps} from './next/components/Alert';
export type {BadgeColor, BadgeProps} from './next/components/Badge';
export type {BannerProps, BannerVariant} from './next/components/Banner';
export type {BodyProps, BodySize, BodyWeight} from './next/components/Body';
export type {BottomSheetProps} from './next/components/BottomSheet';
export type {ButtonGroupProps} from './next/components/ButtonGroup';
export type {
  ButtonProps,
  ButtonSize,
  ButtonVariant,
} from './next/components/Button';
export type {CalloutPosition, CalloutProps} from './next/components/Callout';
export type {CaptionWeight, CaptionProps} from './next/components/Caption';
export type {CardActionsProps} from './next/components/CardActions';
export type {CardContentProps} from './next/components/CardContent';
export type {CardHeaderProps} from './next/components/CardHeader';
export type {CardMediaProps} from './next/components/CardMedia';
export type {CardSize, CardProps} from './next/components/Card';
export type {CheckboxProps} from './next/components/Checkbox';
export type {ChipGroupProps} from './next/components/ChipGroup';
export type {ChipId, ChipProps, ChipSize} from './next/components/Chip';
export type {
  CircularProgressIndicatorDirection,
  CircularProgressIndicatorOrigin,
  CircularProgressIndicatorProps,
} from './next/components/CircularProgressIndicator';
export type {CollapseProps} from './next/components/Collapse';
export type {ColorsType, TypographyColors} from './next/utils/';
export type {DataTableBodyProps} from './next/components/DataTableBody';
export type {DataTableBulkActionsProps} from './next/components/DataTableBulkActions';
export type {DataTableCellActionsMenuItemProps} from './next/components/DataTableCellActionsMenuItem';
export type {DataTableCellActionsMenuProps} from './next/components/DataTableCellActionsMenu';
export type {
  DataTableCellActionsAlignmentType,
  DataTableCellActionsProps,
} from './next/components/DataTableCellActions';
export type {DataTableCellSelectProps} from './next/components/DataTableCellSelect';
export type {
  DataTableCellSelectStatusAlignmentType,
  DataTableCellSelectStatusProps,
} from './next/components/DataTableCellStatus';
export type {
  DataTableCellProps,
  DataTableCellVariant,
} from './next/components/DataTableCell';
export type {DataTableHeaderSelectProps} from './next/components/DataTableHeaderSelect';
export type {
  DataTableHeaderAlignmentType,
  DataTableHeaderProps,
  DataTableHeaderSortType,
} from './next/components/DataTableHeader';
export type {DataTableHeadProps} from './next/components/DataTableHead';
export type {DataTableRowProps} from './next/components/DataTableRow';
export type {DataTableProps} from './next/components/DataTable';
export type {
  DateDropdownProps,
  DateDropdownState,
} from './next/components/DateDropdown';
export type {
  DisplayProps,
  DisplaySize,
  DisplayWeight,
} from './next/components/Display';
export type {DividerProps} from './next/components/Divider';
export type {ErrorMessageProps} from './next/components/ErrorMessage';
export type {FormGroupProps} from './next/components/FormGroup';
export type {
  HeadingProps,
  HeadingSize,
  HeadingWeight,
} from './next/components/Heading';
export type {
  IconButtonProps,
  IconButtonSize,
} from './next/components/IconButton';
export type {LinkColorType, LinkProps} from './next/components/Link';
export type {ListItemProps} from './next/components/ListItem';
export type {ListProps} from './next/components/List';
export type {LivingDesignProviderProps} from './next/components/LivingDesignProvider';
export type {MenuItemProps} from './next/components/MenuItem';
export type {MenuPosition, MenuProps} from './next/components/Menu';
export type {
  MetricsData,
  MetricGroupProps,
} from './next/components/MetricGroup';
export type {MetricProps, MetricVariant} from './next/components/Metric';
export type {ModalProps, ModalSize} from './next/components/Modal';
export type {NudgeProps} from './next/components/Nudge';
export type {PopoverPosition, PopoverProps} from './next/components/Popover';
export type {
  ProgressIndicatorProps,
  ProgressIndicatorVariant,
} from './next/components/ProgressIndicator';
export type {ProgressTrackerItemProps} from './next/components/ProgressTrackerItem';
export type {
  ProgressTrackerProps,
  ProgressTrackerVariant,
} from './next/components/ProgressTracker';
export type {RadioProps} from './next/components/Radio';
export type {RatingProps, RatingSize} from './next/components/Rating';
export type {SeeDetailsProps} from './next/components/SeeDetails';
export type {SegmentedProps, SegmentSize} from './next/components/Segmented';
export type {SegmentProps} from './next/components/Segment';
export type {
  OSBasedComponentType,
  SelectComponentType,
  Selected,
  SelectionType,
  SelectOptions,
  SelectOption,
  SelectSize,
  SelectProps,
} from './next/components/Select';
export type {SkeletonTextProps} from './next/components/SkeletonText';
export type {SkeletonProps, SkeletonVariant} from './next/components/Skeleton';
export type {SnackbarProps} from './next/components/Snackbar';
export type {SnackProps} from './next/components/SnackbarProvider';
export type {SpinnerOverlayProps} from './next/components/SpinnerOverlay';
export type {
  SpinnerColor,
  SpinnerProps,
  SpinnerSize,
} from './next/components/Spinner';
export type {
  SpotIconColor,
  SpotIconProps,
  SpotIconSize,
} from './next/components/SpotIcon';
export type {
  StyledTextColor,
  StyledTextProps,
  StyledTextSize,
} from './next/components/StyledText';
export type {SwitchProps} from './next/components/Switch';
export type {TabNavigationItemProps} from './next/components/TabNavigationItem';
export type {TabNavigationProps} from './next/components/TabNavigation';
export type {TagColor, TagProps, TagVariant} from './next/components/Tag';
export type {
  TextAreaInputType,
  TextAreaProps,
  TextAreaRef,
  TextAreaSize,
} from './next/components/TextArea';
export type {
  TextFieldInputType,
  TextFieldProps,
  TextFieldRef,
  TextFieldSize,
} from './next/components/TextField';
export type {VariantsProps} from './next/components/Variants';
export type {WizardFooterProps} from './next/components/WizardFooter';

// Legacy components
// (we still provide them for backwards compatibility)
export {default as colorsJson} from './theme/colors.json'; // Dummy import for backwards compatibility of colors.json
export {
  PrimaryButton, // @deprecated
  SecondaryButton, // @deprecated
  TransparentButton, // @deprecated
  DestructiveButton, // @deprecated
  BannerButton, // @deprecated
  POVPrimaryButton, // @deprecated
  POVSecondaryButton, // @deprecated
  LinkButton, // @deprecated
  TertiaryButton, // @deprecated
} from './buttons';
export {default as Chips} from './chips/chips'; // @deprecated
export {
  CountBadge, // @deprecated
  MediaBadge, // @deprecated
  AvailabilityBadge, // @deprecated
  InformationalBadge, // @deprecated
  FilledFlag, // @deprecated
  RollbackFlag, // @deprecated
  Flag, // @deprecated
  PrimaryTag, // @deprecated
  SecondaryTag, // @deprecated
  TertiaryTag, // @deprecated
  SupportiveText, // @deprecated
} from './flags';
export {
  MultilineTextField, // @deprecated
  PasswordField, // @deprecated
  Dropdown, // @deprecated
  // Checkbox // Removed as this is an undocumented legacy export
  CheckboxItem, // @deprecated
  CheckboxItemGroup, // @deprecated
  // Radio, // Removed as this is an undocumented legacy export
  RadioItem, // @deprecated
  RadioItemGroup, // @deprecated
  // Toggle, // Removed as this is an undocumented legacy export
  ToggleItem, // @deprecated
  // Segmented, // Removed as this is an undocumented legacy export
  ToggleItemGroup, // @deprecated
} from './form';
export {
  Scrollbar, // @deprecated
  LinearProgressIndicator, // @deprecated
  Ratings, //@deprecated
} from './indicators';
export {
  // BottomSheet, // Removed in favor of refactored component
  CardOverlay, // @deprecated
  Carousel, // @deprecated
  MediaCard, // @deprecated
  OutlineCard, // @deprecated
  Overlay, // @deprecated
  // Skeleton, // Removed for refactored component
  // SpinnerOverlay, // Removed for refactored component
  SolidCard, // @deprecated
} from './layout';
export {
  AlertInfo, // @deprecated
  AlertInfo2, // @deprecated
  AlertInfo3, // @deprecated
  AlertError, // @deprecated
  Message, // @deprecated
  MessageSuccess, // @deprecated
  MessageWarning, // @deprecated
  MessageError, // @deprecated
  Tooltip, // @deprecated
} from './messaging';
export {
  Tabs, // @deprecated
} from './navigation';
export {
  Body2, // @deprecated
  Caption2, // @deprecated
  Display2, // @deprecated
  Headline, // @deprecated
  Price, // @deprecated
  Subheader, // @deprecated
  Subheader2, // @deprecated
  Title, // @deprecated
  Title2, // @deprecated
  Title3, // @deprecated
} from './typography';
export {default as ThemeProvider} from './theme/theme-provider'; // @deprecated

// Undocumented, internal
export {useSimpleReducer} from './next/utils';
export {useAccessibilityFocus} from './next/utils/useAccessibilityFocus';
export {_KeyboardAvoidingView} from './next/components/_KeyboardAvoidingView';
export {_ColorPalette} from './next/components/_ColorPalette';
