const path = require('path');

module.exports = function () {
  return {
    name: 'docusaurus-react-native-plugin',
    configureWebpack() {
      return {
        mergeStrategy: {'resolve.extensions': 'prepend'},
        resolve: {
          alias: {
            react: path.resolve('node_modules/react'),
            'react-native$': 'react-native-web',
          },
          extensions: ['.web.js'],
        },
      };
    },
  };
};
