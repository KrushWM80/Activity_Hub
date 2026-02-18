import {LayoutRectangle, ViewStyle} from 'react-native';

import {PopoverPosition} from '../components/Popover';

const resolveNubbinAlignmentStyle = (position: PopoverPosition): ViewStyle => {
  switch (position) {
    case 'bottomRight':
      return {
        alignItems: 'flex-start',
      };
    case 'bottomCenter':
      return {
        alignItems: 'center',
      };
    case 'bottomLeft':
      return {
        alignItems: 'flex-end',
      };
    case 'right':
      return {
        flexDirection: 'row',
        alignItems: 'center',
      };
    case 'left':
      return {
        flexDirection: 'row-reverse',
        alignItems: 'center',
      };
    case 'topRight':
      return {
        flexDirection: 'column-reverse',
        alignItems: 'flex-start',
      };
    case 'topCenter':
      return {
        flexDirection: 'column-reverse',
        alignItems: 'center',
      };
    case 'topLeft':
      return {
        flexDirection: 'column-reverse',
        alignItems: 'flex-end',
      };
    default:
      return {};
  }
};

const resolvePopUpPositionStyle = (
  position: PopoverPosition,
  pageX: number,
  pageY: number,
  triggerWidth: number,
  triggerHeight: number,
  overlayWidth: number,
  overlayHeight: number,
  containerOffset: number,
  nubbinOffset?: number,
  nubbinWidth?: number,
  hasSpotlight?: boolean,
) => {
  let left = 0;
  let top = 0;

  // Calculate the Y position
  if (position.startsWith('top')) {
    top = hasSpotlight
      ? pageY - overlayHeight + triggerHeight
      : pageY - (overlayHeight + containerOffset);
  } else if (position.startsWith('bottom')) {
    top = hasSpotlight
      ? pageY + triggerHeight - triggerHeight
      : pageY + (triggerHeight + containerOffset);
  } else {
    // right + left
    top = pageY - (overlayHeight - triggerHeight) / 2;
  }

  // Calculate the X position
  if (position === 'left') {
    // Align both left edges, then move left by width of overlay
    left = hasSpotlight
      ? pageX - overlayWidth + triggerWidth
      : pageX - overlayWidth - containerOffset;
  } else if (position === 'right') {
    // Move right by width of the target
    left = hasSpotlight
      ? pageX + triggerWidth - triggerWidth
      : pageX + triggerWidth + containerOffset;
  } else if (position === 'bottomLeft' || position === 'topLeft') {
    // Align right of overlay to center of trigger + distance to nubbin + half of nubbin width
    left =
      nubbinOffset && nubbinWidth
        ? pageX -
          overlayWidth +
          triggerWidth / 2 +
          nubbinOffset +
          nubbinWidth / 2
        : pageX - overlayWidth + triggerWidth / 2;
  } else if (position === 'bottomRight' || position === 'topRight') {
    // Align left of overlay to center of trigger - distance to nubbin - half of nubbin
    left =
      nubbinOffset && nubbinWidth
        ? pageX + triggerWidth / 2 - nubbinOffset - nubbinWidth / 2
        : pageX + triggerWidth / 2;
  } else {
    // bottomCenter + topCenter
    left = pageX - overlayWidth / 2 + triggerWidth / 2;
  }

  return {left, top};
};

const resolveSpotlightContainerStyle = (
  position: string,
  childrenLayout: LayoutRectangle | undefined,
  nubbinWidth: number,
  nubbinOffset: number,
) => {
  if (
    !childrenLayout ||
    !childrenLayout.width ||
    !nubbinWidth ||
    !nubbinOffset
  ) {
    return {};
  }

  const {width} = childrenLayout;
  const resolvedStyle = {
    marginLeft: 0,
    marginRight: 0,
    marginBottom: 0,
    marginTop: 0,
  };

  switch (position) {
    case 'bottomRight':
      resolvedStyle.marginLeft = Math.abs(
        width / 2 - nubbinWidth / 2 - nubbinOffset,
      );
      resolvedStyle.marginBottom = 4;
      break;
    case 'bottomCenter':
      resolvedStyle.marginBottom = 4;
      break;
    case 'bottomLeft':
      resolvedStyle.marginRight = Math.abs(
        width / 2 - nubbinWidth / 2 - nubbinOffset,
      );
      resolvedStyle.marginBottom = 4;
      break;
    case 'right':
      resolvedStyle.marginRight = 4;
      break;
    case 'left':
      resolvedStyle.marginLeft = 4;
      break;
    case 'topRight':
      resolvedStyle.marginLeft = Math.abs(
        width / 2 - nubbinWidth / 2 - nubbinOffset,
      );
      resolvedStyle.marginTop = 4;
      break;
    case 'topCenter':
      resolvedStyle.marginTop = 4;
      break;
    case 'topLeft':
      resolvedStyle.marginRight = Math.abs(
        width / 2 - nubbinWidth / 2 - nubbinOffset,
      );
      resolvedStyle.marginTop = 4;
      break;
  }

  return resolvedStyle;
};

const calculateMenuPosition = (
  screenWidth: number,
  screenHeight: number,
  pageX: number,
  pageY: number,
) => {
  if (screenWidth / 2 < screenWidth - pageX) {
    if (screenHeight / 4 > screenHeight - pageY) {
      return 'topRight';
    } else {
      return 'bottomRight';
    }
  } else if (screenHeight / 4 > screenHeight - pageY) {
    return 'topLeft';
  } else {
    return 'bottomLeft';
  }
};
const calculateCellWidth = (
  width: number | string | undefined,
  numberOfColumns: number | undefined,
) => {
  //screen width divide into equal parts
  const minWidth = numberOfColumns ? Math.round(100 / numberOfColumns) : 25;
  return width
    ? width
    : minWidth > 25 || numberOfColumns! >= 5
    ? `${minWidth}%`
    : '25%';
};

export {
  resolveNubbinAlignmentStyle,
  resolvePopUpPositionStyle,
  resolveSpotlightContainerStyle,
  calculateMenuPosition,
  calculateCellWidth,
};
