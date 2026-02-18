const path = require('path');
const prismThemes = require('prism-react-renderer');

const {screenshots} = require('./src/data/screenshots.js');
// const {version} = require('../package.json');

const title = 'LD React Native Components';

const url = 'https://gecgithub01.walmart.com';

/**
 * There are 2 environments that we want to support:
 * 1. Development - Docs should work on `http://localhost:3000/pages/electrode-mobile-platform/gtp-shared-components/`
 * 2. Production - Docs should work on `https://gecgithub01.walmart.com/pages/electrode-mobile-platform/gtp-shared-components/
 */
const baseUrl = '/pages/electrode-mobile-platform/gtp-shared-components/';

const config = {
  title: title,
  tagline: 'Documentation site for gtp-shared-components repo',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: url,
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: baseUrl,

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'electrode-mobile-platform', // Usually your GitHub org/user name.
  projectName: 'gtp-shared-components', // Usually your repo name.
  deploymentBranch: 'gh-pages',
  trailingSlash: false,

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  plugins: [
    [
      './component-docs-plugin',
      {
        // Docs Directory - website/docs/*
        ldComponentDocsRootDir: path.join(__dirname, 'docs', 'components', 'ld'),
        axComponentDocsRootDir: path.join(__dirname, 'docs', 'components', 'ax'),
        utilityDocsRootDir: path.join(__dirname, 'docs', 'utilities'),

        // Library Directory - src/next/*
        ldComponentRootDir: path.join(__dirname, '..', 'src', 'next', 'components'),
        axComponentRootDir: path.join(__dirname, '..', 'src', 'ax', 'components'),
        utilsRootDir: path.join(__dirname, '..', 'src', 'next', 'utils'),
        axComponents: {
          FilterTag: 'FilterTag',
          FilterToggle: 'FilterToggle',
          FilterTriggerAll: 'FilterTriggerAll',
          FilterTriggerSingle: 'FilterTriggerSingle',
          FilterGroup: 'FilterGroup',
        },
        ldComponents: {
          Alert: 'Alert',
          Badge: 'Badge',
          Button: 'button',
          Banner: 'Banner',
          Body: 'Body',
          BottomSheet: 'BottomSheet',
          ButtonGroup: 'ButtonGroup',
          Callout: 'Callout',
          Caption: 'Caption',
          Card: 'Card',
          CardMedia: 'CardMedia',
          CardHeader: 'CardHeader',
          CardContent: 'CardContent',
          CardActions: 'CardActions',
          Checkbox: 'Checkbox',
          Chip: 'Chip',
          ChipGroup: 'ChipGroup',
          CircularProgressIndicator: 'CircularProgressIndicator',
          Collapse: 'Collapse',
          DataTable: 'DataTable',
          DataTableBody: 'DataTableBody',
          DataTableBulkActions: 'DataTableBulkActions',
          DataTableCell: 'DataTableCell',
          DataTableCellActions: 'DataTableCellActions',
          DataTableCellActionsMenu: 'DataTableCellActionsMenu',
          DataTableCellActionsMenuItem: 'DataTableCellActionsMenuItem',
          DataTableCellSelect: 'DataTableCellSelect',
          DataTableCellStatus: 'DataTableCellStatus',
          DataTableHead: 'DataTableHead',
          DataTableHeader: 'DataTableHeader',
          DataTableHeaderSelect: 'DataTableHeaderSelect',
          DataTableRow: 'DataTableRow',
          DateDropdown: 'DateDropdown',
          Display: 'Display',
          Divider: 'Divider',
          ErrorMessage: 'ErrorMessage',
          FormGroup: 'FormGroup',
          Heading: 'Heading',
          IconButton: 'IconButton',
          Link: 'Link',
          List: 'List',
          ListItem: 'ListItem',
          LivingDesignProvider: 'LivingDesignProvider',
          Menu: 'Menu',
          MenuItem: 'MenuItem',
          Metric: 'Metric',
          MetricGroup: 'MetricGroup',
          Modal: 'Modal',
          Nudge: 'Nudge',
          Popover: 'Popover',
          ProgressIndicator: 'ProgressIndicator',
          ProgressTracker: 'ProgressTracker',
          ProgressTrackerItem: 'ProgressTrackerItem',
          Radio: 'Radio',
          Rating: 'Rating',
          Select: 'Select',
          Segmented: 'Segmented',
          Segment: 'Segment',
          SeeDetails: 'SeeDetails',
          Skeleton: 'Skeleton',
          SkeletonText: 'SkeletonText',
          Spinner: 'Spinner',
          SpinnerOverlay: 'SpinnerOverlay',
          SpotIcon: 'SpotIcon',
          StyledText: 'StyledText',
          Switch: 'Switch',
          TabNavigation: 'TabNavigation',
          TabNavigationItem: 'TabNavigationItem',
          Tag: 'Tag',
          TextArea: 'TextArea',
          TextField: 'TextField',
          Variants: 'Variants',
          WizardFooter: 'WizardFooter',
        },
        utilities: {
          useSnackBar: 'useSnackBar',
          useAccessibilityFocus: 'useAccessibilityFocus',
        }
      },
    ],
    require('./plugins/docusaurus-react-native-plugin'),
  ],

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      {
        docs: {
          routeBasePath: '/',
          sidebarPath: './sidebars.ts',
          remarkPlugins: [
            [require('@docusaurus/remark-plugin-npm2yarn'), {sync: true}],
          ],
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      },
    ],
  ],

  themes: [
    // ... Your other themes.
    [
      "@easyops-cn/docusaurus-search-local",
      /** @type {import("@easyops-cn/docusaurus-search-local").PluginOptions} */
      ({
        // `hashed` is recommended as long-term-cache of index file is possible.
        hashed: true,
        indexBlog: false,
        docsRouteBasePath: '/',
        indexPages: false,
        language: ["en"],
      }),
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/docusaurus-social-card.jpg',
    navbar: {
      logo: {
        alt: 'Living Design React Native',
        src: 'img/ld-react-native.svg',
        srcDark: 'img/ld-react-native-dark.svg',
      },
      items: [
        {
          type: 'doc',
          docId: 'introduction/introduction',
          position: 'left',
          label: 'Introduction',
        },
        {
          type: 'doc',
          docId: 'components/ld/Alert',
          position: 'left',
          label: 'Components',
        },
        {
          type: 'doc',
          docId: 'utilities/useSnackBar',
          position: 'left',
          label: 'Utilities',
        },
        // TODO: Add support for different versions of docs depending on version of library
        // {
        //   position: 'right',
        //   label: version,
        //   href: 'https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components',
        // },
        {
          href: 'https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components',
          className: 'nav-link nav-github-link',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Community',
          items: [
            {
              label: 'Support: #ld-support-reactnative',
              href: 'https://walmart.slack.com/archives/C01LDQF7SRZ',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'GitHub',
              href: 'https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/',
            },
            {
              label: 'Releases',
              href: 'https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/releases',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Walmart, Inc. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  },
  customFields: {
    moreExamples: {
      // Use - Will be able to add moreExamples for specific components
      // Snackbar: {
      //   'Snackbar rendered regardless of the parent positioning':
      //     'https://snack.expo.dev/@react-native-paper/more-examples---snackbar-rendered-regardless-of-the-parent-positioning',
      // },
    },
    knownIssues: {
      // Use - Will be able to add Known issues to specific components.
      // TextInput: {
      //   'Outline overlaps label':
      //     'Reference Link here',
      //   'Long text wraps to a second line':
      //     'Reference Link here',
      // },
    },
    screenshots,
  },
};

module.exports = config;
