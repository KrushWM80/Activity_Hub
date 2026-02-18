import {colors, composeTheme, deepMerge} from '../next/utils';
import {getFont} from '../theme/font';

const scrollbarSegment = {
  borderColor: 'transparent',
  backgroundColor: 'transparent',
  borderRadius: 9999,
  borderWidth: 0,
  borderStyle: 'solid',
  maxWidth: 60,
};

const scrollbar = {
  default: {
    container: {
      paddingHorizontal: 16,
      paddingVertical: 16,
    },
    line: {
      backgroundColor: colors.gray['20'],
      borderWidth: 0,
      borderStyle: 'solid',
      borderRadius: 9999,
      height: 2,
      width: '100%',
      maxWidth: 240,
      flexDirection: 'row',
      alignSelf: 'center',
      justifyContent: 'space-between',
    },
    segment: scrollbarSegment,
    selected: deepMerge(scrollbarSegment, {
      borderColor: colors.black,
      borderStyle: 'solid',
      backgroundColor: colors.black,
    }),
  },
  block: {
    container: {
      paddingHorizontal: 0,
    },
  },
};

const circular = {
  static: {
    radius: 38,
    ringWidth: 8,
  },
  default: {
    container: {
      alignItems: 'center',
      justifyContent: 'center',
      position: 'relative',
      overflow: 'hidden',
    },
    indicator: {
      backgroundColor: colors.gray['20'],
      color: colors.gray['80'],
    },
    innerCircle: {
      backgroundColor: colors.white,
    },
    text: {
      ...getFont('bold'),
      fontSize: 18,
      lineHeight: 24,
      position: 'relative',
      textAlign: 'center',
      zIndex: 2,
    },
    label: {
      ...getFont(),
      fontSize: 12,
      lineHeight: 16,
      textAlign: 'center',
      zIndex: 2,
    },
  },
};

const linear = {
  default: {
    container: {
      borderRadius: 9999,
      height: 6,
      overflow: 'hidden',
      position: 'relative',
      backgroundColor: colors.gray['20'],
    },
    indicator: {
      borderBottomLeftRadius: 9999,
      borderTopLeftRadius: 9999,
      left: 0,
      position: 'absolute',
      top: 0,
      bottom: 0,
      backgroundColor: colors.gray['80'],
    },
  },
  small: {
    container: {
      height: 3,
    },
  },
};

const ratings = {
  default: {
    container: {
      marginRight: 24,
      height: 24,
      alignItems: 'center',
      flexDirection: 'row',
    },
    text: {
      marginLeft: 4,
      lineHeight: 24,
    },
    link: {
      marginLeft: 8,
      lineHeight: 24,
    },
  },
};

const spinner = {
  default: {
    container: {
      height: 48,
      width: 48,
      alignSelf: 'center',
    },
    leaf: {
      position: 'absolute',
      tintColor: colors.gray['100'],
    },
  },
  small: {
    container: {
      height: 24,
      width: 24,
    },
  },
};

const progressTrackerDot = {
  height: 8,
  width: 8,
  backgroundColor: colors.gray['30'],
  borderRadius: 99999,
};
const progressTracker = {
  default: {
    container: {
      padding: 16,
    },
    header: {
      marginBottom: 16,
    },
    headerContainer: {
      flexDirection: 'row',
      alignItems: 'center',
    },
    title: {
      ...getFont('bold'),
      fontSize: 16,
      lineHeight: 24,
      flex: 1,
    },
    button: {
      marginVertical: -4,
    },
    subtitle: {
      ...getFont(),
      fontSize: 14,
      lineHeight: 20,
      color: colors.gray['100'],
    },
    progress: {
      margin: 3,
      height: 2,
      backgroundColor: colors.gray['30'],
    },
    complete: {
      height: 2,
      backgroundColor: colors.blue['100'],
    },
    dotContainer: {
      position: 'absolute',
      top: -3,
      marginLeft: -3,
      height: 8,
      width: 8,
      borderRadius: 8,
    },
    dotContainerComplete: {
      position: 'absolute',
      top: -7,
      marginLeft: -7,
      height: 16,
      width: 16,
      backgroundColor: colors.white,
      borderWidth: 2,
      borderColor: colors.blue['100'],
      padding: 2,
      borderRadius: 16,
    },
    dot: progressTrackerDot,
    dotComplete: deepMerge(progressTrackerDot, {
      backgroundColor: colors.blue['100'],
    }),
    labels: {
      flexDirection: 'row',
      height: 16,
      marginTop: 4,
    },
    label: {
      ...getFont(),
      fontSize: 12,
      lineHeight: 16,
      position: 'absolute',
      textAlign: 'center',
      width: 200,
      marginLeft: -100,
      color: colors.gray[100],
    },
    labelFirst: {
      marginLeft: 0,
      textAlign: 'left',
    },
    labelLast: {
      marginLeft: -200,
      textAlign: 'right',
    },
    labelCurrent: {
      color: colors.gray[160],
    },
    link: {
      alignSelf: 'flex-start',
      marginTop: 16,
    },
  },
  active: {},
  delayed: {
    dotContainerComplete: {
      borderColor: colors.orange['100'],
    },
    complete: {
      backgroundColor: colors.orange['100'],
    },
    dotComplete: {
      backgroundColor: colors.orange['100'],
    },
  },
  delivered: {
    dotContainerComplete: {
      borderColor: colors.green['100'],
    },
    complete: {
      backgroundColor: colors.green['100'],
    },
    dotComplete: {
      backgroundColor: colors.green['100'],
    },
  },
};

const variants = {
  default: {
    container: {
      alignSelf: 'center',
      display: 'flex',
      flexDirection: 'row',
      alignItems: 'center',
    },
    pip: {
      height: 8,
      width: 8,
      marginVertical: 4,
      marginRight: 8,
      borderRadius: 99999,
      backgroundColor: colors.black,
    },
    lastPip: {
      marginRight: 0,
    },
    caption: {
      ...getFont(),
      fontSize: 12,
      lineHeight: 16,
      color: colors.gray['100'],
    },
  },
};

const theme = {
  indicator: {
    scrollbar,
    circular,
    linear,
    ratings,
    spinner,
    progressTracker,
    variants,
  },
};

export default theme;
export const composed = composeTheme(theme);
