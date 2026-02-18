/* global __dirname */
const pkg = require('./package.json');
const fs = require('fs');
const isDev = process.env.NODE_ENV === 'development';
const path = require('path');
const webpack = require('webpack');

const nameResolver = (tags = [], fileName) => {
  const tagged = {
    class: (tags.find((tag) => tag.name === 'class') || {}).text,
    component: (tags.find((tag) => tag.name === 'component') || {}).text,
  };
  const componentFromFile = path
    .basename(fileName)
    .split('.')[0]
    .split('-')
    .reduce((res, word, i) => {
      const file = word.replace(/[^A-Z0-9]*/gi, '');
      return `${res}${file.charAt(0).toUpperCase()}${file.substr(1)}`;
    }, '')
    .replace(/^[^A-Z]*/gi, '');

  return tagged.class || tagged.component || componentFromFile;
};

const allowParent = ['SwitchProps'];

module.exports = {
  require: ['./styleguidist/setup.js'],
  propsParser: require('react-docgen-typescript').withDefaultConfig({
    shouldRemoveUndefinedFromOptional: true,
    componentNameResolver: (exp, source) =>
      nameResolver(exp.getJsDocTags(), source.fileName),
    propFilter: (prop, component) => {
      if (prop.parent) {
        return (
          !prop.parent.fileName.includes('node_modules') ||
          allowParent.includes(prop.parent.name)
        );
      }
      return true;
    },
  }).parse,
  moduleAliases: {
    '@walmart/gtp-shared-icons': path.resolve(__dirname, 'src'),
  },
  pagePerSection: true,
  sections: [
    {
      name: 'Introduction',
      content: 'styleguidist/introduction.md',
    },
    {
      name: 'Colors',
      content: 'src/theme/colors.md',
    },
    {
      name: 'Icons',
      content: 'styleguidist/icons.md',
      components: 'src/icons/*.tsx',
    },
  ],
  ignore: ['src/**/index.tsx'],
  webpackConfig: {
    resolve: {
      alias: {
        'react-native': 'react-native-web',
      },
      // Resolve to iOS-specific components
      extensions: ['.ios.ts', '.android.ts', '.ts', '.json'],
    },
    module: {
      rules: [
        {
          test: /\.(js|ts)(x?)$/,
          loader: 'babel-loader',
          exclude: [/node_modules/],
          options: {
            plugins: [
              '@babel/proposal-class-properties',
              '@babel/proposal-object-rest-spread',
            ],
            presets: [
              '@babel/preset-env',
              'module:metro-react-native-babel-preset',
            ],
            babelrc: false,
          },
        },
        {
          test: /\.(gif|jpe?g|png|svg)$/,
          use: {
            loader: 'url-loader',
            options: {
              name: '[name].[ext]',
            },
          },
        },
        {
          test: /\.css$/,
          use: ['style-loader', 'css-loader'],
        },
      ],
    },
    plugins: [
      new webpack.DefinePlugin({
        'process.env.NODE_ENV': JSON.stringify(
          process.env.NODE_ENV || 'development',
        ),
        'process.env.__REACT_NATIVE_DEBUG_ENABLED__': isDev,
      }),

      /**
       * react-native automatically resolves images with `@2x`, `@3x`, etc.
       * suffixes depending on native screen resolution. Just resolve to `@2x` via
       * Webpack's module replacement plugin.
       *
       * {@link https://facebook.github.io/react-native/docs/images.html#static-image-resources}
       * {@link https://webpack.js.org/plugins/normal-module-replacement-plugin/}
       */
      new webpack.NormalModuleReplacementPlugin(/(.*)\.png$/, (resource) => {
        const highRes = resource.request.replace('.png', '@2x.png');

        if (fs.existsSync(path.resolve(resource.context, highRes))) {
          resource.request = highRes;
        }
      }),
    ],
  },
  styleguideDir: path.join(__dirname, 'docs'),
  styleguideComponents: {
    Wrapper: path.join(__dirname, 'styleguidist/preview-wrapper'),
  },
  title: pkg.name,
  getExampleFilename(componentPath) {
    const ret = componentPath
      .replace(/\.(js|ts)x?$/, '.md')
      .replace(/next\/components/, 'next/components/docs');
    return ret;
  },
  theme: path.join(__dirname, 'styleguidist/theme.ts'),
  styles: path.join(__dirname, 'styleguidist/styles.ts'),
};
