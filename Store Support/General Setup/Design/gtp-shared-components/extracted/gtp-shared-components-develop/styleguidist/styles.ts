import {colors} from '../src/next/utils';
export default {
  Logo: {
    logo: {
      borderBottom: 'none',
      color: colors.white,
    },
  },
  ComponentsList: {
    item: {
      '& a': {
        color: [[colors.white], '!important'],
      },
    },
  },
  Playground: {
    preview: {
      width: 400,
      margin: 'auto',
      overflow: 'auto',
      border: 'none',
      backgroundColor: colors.gray['10'],
      padding: 16,
      borderRadius: 4,
      '&.dark': {
        width: 400,
        margin: 'auto',
        overflow: 'auto',
        border: 'none',
        backgroundColor: colors.gray['100'],
        padding: 16,
        borderRadius: 4,
      },
      '&.light': {
        width: 400,
        margin: 'auto',
        overflow: 'auto',
        border: '1px solid ' + colors.gray[50],
        backgroundColor: colors.white,
        padding: 16,
        borderRadius: 4,
      },
      '& [role=checkbox]': {cursor: 'pointer'},
      '& [role=button]': {cursor: 'pointer'},
      '& [role=radio]': {cursor: 'pointer'},
    },
  },
  StyleGuide: {
    '@global input': {
      outline: 'none',
    },
    '@global textarea': {
      outline: 'none',
    },
  },
};
