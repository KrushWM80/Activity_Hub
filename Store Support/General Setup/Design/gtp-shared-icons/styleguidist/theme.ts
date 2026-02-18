import colors from '../src/theme/colors.json';

export default {
  sidebarWidth: 300,
  fontFamily: {
    base: '"Bogle"',
    monospace: ['Consolas', '"Liberation Mono"', 'Menlo', 'monospace'],
  },
  color: {
    preview: colors.white,
    border: colors.gray['150'],
    base: colors.gray['150'],
    sidebarBackground: colors.gray['150'],
    linkHover: colors.blue['100'],
  },
};
