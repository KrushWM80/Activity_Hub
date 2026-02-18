const {getDefaultConfig, mergeConfig} = require('@react-native/metro-config');

/**
 * Metro configuration
 * https://facebook.github.io/metro/docs/configuration
 *
 * @type {import('metro-config').MetroConfig}
 */

const path = require('path');
const escape = require('escape-string-regexp');
const exclusionList = require('metro-config/src/defaults/exclusionList');

const root = path.resolve(__dirname, '..');
const modules = Object.keys({
  ...require(path.join(root, 'package.json')).peerDependencies,
});
const escapeModule = m => escape(path.join(root, 'node_modules', m));

const config = {
  watchFolders: [root],
  resolver: {
    enableGlobalPackages: true,
    blockList: exclusionList(
      modules.map(m => new RegExp(`^${escapeModule(m)}\\/.*$`)),
    ),
    extraNodeModules: modules.reduce((acc, name) => {
      acc[name] = path.join(__dirname, 'node_modules', name);
      return acc;
    }, {}),
  },
};

module.exports = mergeConfig(getDefaultConfig(__dirname), config);
