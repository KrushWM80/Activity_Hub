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
      if (file.substring(0, 3) === 'use') {
        return `${res}${file}`;
      }
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
    '@walmart/gtp-shared-components/assets/images': path.resolve(
      __dirname,
      'assets/images',
    ),
    '@walmart/gtp-shared-components/dist/next/utils': path.resolve(
      __dirname,
      'src/next/utils',
    ),
    '@walmart/gtp-shared-components': path.resolve(__dirname, 'src'),
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
    },
    {
      name: 'Components',
      content: 'styleguidist/components.md',
      components: [
        'src/next/components/Alert.tsx',
        'src/next/components/Badge.tsx',
        'src/next/components/Banner.tsx',
        'src/next/components/Body.tsx',
        'src/next/components/BottomSheet.tsx',
        'src/next/components/Button.tsx',
        'src/next/components/ButtonGroup.tsx',
        'src/next/components/Callout.tsx',
        'src/next/components/Caption.tsx',
        'src/next/components/Card.tsx',
        'src/next/components/CardMedia.tsx',
        'src/next/components/CardHeader.tsx',
        'src/next/components/CardContent.tsx',
        'src/next/components/CardActions.tsx',
        'src/next/components/Checkbox.tsx',
        'src/next/components/Chip.tsx',
        'src/next/components/ChipGroup.tsx',
        'src/next/components/CircularProgressIndicator.tsx',
        'src/next/components/Collapse.tsx',
        'src/next/components/DataTable.tsx',
        'src/next/components/DataTableBody.tsx',
        'src/next/components/DataTableBulkActions.tsx',
        'src/next/components/DataTableCell.tsx',
        'src/next/components/DataTableCellActions.tsx',
        'src/next/components/DataTableCellActionsMenu.tsx',
        'src/next/components/DataTableCellActionsMenuItem.tsx',
        'src/next/components/DataTableCellSelect.tsx',
        'src/next/components/DataTableCellStatus.tsx',
        'src/next/components/DataTableHead.tsx',
        'src/next/components/DataTableHeader.tsx',
        'src/next/components/DataTableHeaderSelect.tsx',
        'src/next/components/DataTableRow.tsx',
        'src/next/components/DateDropdown.tsx',
        'src/next/components/Display.tsx',
        'src/next/components/Divider.tsx',
        'src/next/components/ErrorMessage.tsx',
        'src/next/components/FormGroup.tsx',
        'src/next/components/Heading.tsx',
        'src/next/components/IconButton.tsx',
        'src/next/components/Link.tsx',
        'src/next/components/List.tsx',
        'src/next/components/ListItem.tsx',
        'src/next/components/LivingDesignProvider.tsx',
        'src/next/components/Menu.tsx',
        'src/next/components/MenuItem.tsx',
        'src/next/components/Metric.tsx',
        'src/next/components/MetricGroup.tsx',
        'src/next/components/Modal.tsx',
        'src/next/components/Nudge.tsx',
        'src/next/components/Popover.tsx',
        'src/next/components/ProgressIndicator.tsx',
        'src/next/components/ProgressTracker.tsx',
        'src/next/components/ProgressTrackerItem.tsx',
        'src/next/components/Radio.tsx',
        'src/next/components/Rating.tsx',
        'src/next/components/Select.tsx',
        'src/next/components/Segmented.tsx',
        'src/next/components/Segment.tsx',
        'src/next/components/SeeDetails.tsx',
        'src/next/components/Skeleton.tsx',
        'src/next/components/SkeletonText.tsx',
        'src/next/components/Spinner.tsx',
        'src/next/components/SpinnerOverlay.tsx',
        'src/next/components/SpotIcon.tsx',
        'src/next/components/StyledText.tsx',
        'src/next/components/Switch.tsx',
        'src/next/components/TabNavigation.tsx',
        'src/next/components/TabNavigationItem.tsx',
        'src/next/components/Tag.tsx',
        'src/next/components/TextArea.tsx',
        'src/next/components/TextField.tsx',
        'src/next/utils/useSnackbar.ts',
        'src/next/components/Variants.tsx',
        'src/next/components/WizardFooter.tsx',
      ],
      ignore: ['**/*.stories.tsx'],
    },
    {
      name: 'Components - LEGACY',
      content: 'styleguidist/legacy.md',
    },
    {
      name: 'Typography',
      components: [
        'src/typography/body-*.tsx',
        'src/typography/caption-*.tsx',
        'src/typography/display-*.tsx',
        'src/typography/headline.tsx',
        'src/typography/price.tsx',
        'src/typography/subheader.tsx',
        'src/typography/subheader-*.tsx',
        'src/typography/title.tsx',
        'src/typography/title-*.tsx',
      ],
      ignore: ['**/*.stories.tsx'],
    },
    {
      name: 'Buttons',
      content: 'styleguidist/buttons.md',
      components: [
        'src/buttons/primary-button.tsx',
        'src/buttons/secondary-button.tsx',
        'src/buttons/transparent-button.tsx',
        'src/buttons/destructive-button.tsx',
        'src/buttons/TertiaryButton.tsx',
        'src/buttons/banner-button.tsx',
        'src/buttons/link-button.tsx',
        'src/buttons/pov-primary-button.tsx',
        'src/buttons/pov-secondary-button.tsx',
      ],
      ignore: ['**/*.test.tsx', '**/*.stories.tsx'],
    },
    {
      name: 'Flags, Badges, Tags, and Supportive Text',
      sections: [
        {
          name: 'Flags',
          content: 'styleguidist/flags.md',
          components: 'src/flags/flags/*.tsx',
          ignore: ['**/*.stories.tsx'],
        },
        {
          name: 'Badges',
          content: 'styleguidist/badges.md',
          components: 'src/flags/badges/*.tsx',
          ignore: ['**/*.stories.tsx'],
        },
        {
          name: 'Tags',
          content: 'styleguidist/tags.md',
          components: 'src/flags/tags/*.tsx',
          ignore: ['**/*.stories.tsx'],
        },
      ],
      components: 'src/flags/supportive-text.tsx',
      ignore: ['**/*.stories.tsx'],
    },
    {
      name: 'Indicators',
      content: 'styleguidist/indicators.md',
      components: [
        'src/indicators/circular.tsx',
        'src/indicators/linear.tsx',
        'src/indicators/progress-tracker.tsx',
        'src/indicators/ratings.tsx',
        'src/indicators/scrollbar.tsx',
        'src/indicators/variants.tsx',
      ],
      ignore: ['**/*.stories.tsx'],
    },
    {
      name: 'Layout',
      content: 'styleguidist/layout.md',
      sections: [
        {
          name: 'Cards',
          components: [
            'src/layout/solid-card.tsx',
            'src/layout/outline-card.tsx',
            'src/layout/media-card.tsx',
          ],
        },
        {
          name: 'Overlays',
          components: ['src/layout/overlay.tsx', 'src/layout/card-overlay.tsx'],
        },
        {
          name: 'Collapsable',
          components: ['src/layout/collapse.tsx', 'src/layout/see-details.tsx'],
        },
      ],
      components: [
        'src/layout/carousel.tsx',
        'src/layout/skeleton.tsx',
        'src/layout/list.tsx',
      ],
      ignore: ['**/*.stories.tsx'],
    },
    {
      name: 'Messaging',
      content: 'styleguidist/messaging.md',
      sections: [
        {
          name: 'Alerts',
          content: 'styleguidist/alerts.md',
          components: [
            'src/messaging/alert/alert.tsx',
            'src/messaging/alert/alert-info.tsx',
            'src/messaging/alert/alert-info-2.tsx',
            'src/messaging/alert/alert-info-3.tsx',
            'src/messaging/alert/alert-error.tsx',
          ],
        },
        {
          name: 'Messages',
          content: 'styleguidist/messages.md',
          components: [
            'src/messaging/message/message.tsx',
            'src/messaging/message/message-success.tsx',
            'src/messaging/message/message-warning.tsx',
            'src/messaging/message/message-error.tsx',
          ],
        },
      ],
      components: 'src/messaging/*.tsx',
      ignore: ['**/*.stories.tsx'],
    },
    {
      name: 'Navigation',
      content: 'styleguidist/navigation.md',
      components: 'src/navigation/tabs.tsx',
      ignore: ['**/*.stories.tsx'],
    },
    {
      name: 'Forms',
      content: 'styleguidist/forms.md',
      sections: [
        {
          name: 'Text Fields',
          components: [
            'src/form/text-fields/multiline-textfield.tsx',
            'src/form/text-fields/text-area.tsx',
            'src/form/text-fields/passwordfield.tsx',
          ],
          ignore: ['**/*.stories.tsx'],
        },
        {
          name: 'Dropdowns',
          components: [
            'src/form/dropdowns/dropdown.tsx',
            'src/form/dropdowns/date-dropdown.tsx',
          ],
          ignore: ['**/*.stories.tsx'],
        },
        {
          name: 'Toggleable',
          components: [
            'src/form/toggleable/*-item.tsx',
            'src/form/toggleable/*-item-group.tsx',
          ],
          ignore: ['**/*.stories.tsx'],
        },
      ],
    },
    {
      name: 'Theme Provider',
      components: ['src/theme/theme-provider.tsx'],
    },
  ],
  ignore: ['src/**/index.tsx'],
  webpackConfig: {
    resolve: {
      alias: {
        // To let alias like 'react-native/Libraries/Components/TextInput/TextInputState'
        // take effect, must set it before alias 'react-native'
        'react-native/Libraries/Components/TextInput/TextInputState': path.join(
          __dirname,
          '/styleguidist/styleguidist-mock.js',
        ),
        'react-native': 'react-native-web',
        '@react-native-picker/picker': path.join(
          __dirname,
          '/styleguidist/styleguidist-mock.js',
        ),
      },
      // Resolve to iOS-specific components
      extensions: ['.ios.ts', '.android.ts', '.ts', '.json'],
    },
    module: {
      rules: [
        {
          test: /\.(js|ts)(x?)$/,
          loader: 'babel-loader',
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
      new webpack.NamedModulesPlugin(),
    ],
  },
  styleguideDir: path.join(__dirname, 'docs'),
  styleguideComponents: {
    Wrapper: path.join(__dirname, 'styleguidist/Wrapper'),
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
