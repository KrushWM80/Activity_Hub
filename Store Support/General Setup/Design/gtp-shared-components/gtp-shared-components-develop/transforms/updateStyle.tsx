/*
  TRANSFORM NAME - updateStyle
  This transform is meant to be run only on consumer app:
  It needs to be run by devs manually using npx runCodemods <transform> <path>.
  It performs the following:
    - We are omitting style from the allowed props in all components and use UNSAFE_style.
    - This transform will run on consumer code to find the components using style and modify to UNSAFE_style.
  Example:
    BEFORE - >  <Body style={styles.normal}>something</Body>

    AFTER  - >  <Body UNSAFE_style={styles.normal}>something</Body>
*/

import {namedTypes} from 'ast-types';
import {API, FileInfo, Options} from 'jscodeshift';
import {Collection} from 'jscodeshift/src/Collection';
export default function transformer(
  file: FileInfo,
  api: API,
  options: Options,
) {
  /* jscodeshift api to parse and update the identifiers*/
  const j = api.jscodeshift;

  /* File root to parse AST. */
  const root = j(file.source);

  /* File Output Print Options */
  const printOptions = options.printOptions || {
    quote: 'single',
    trailingComma: true,
    flowObjectCommas: true,
    arrowParensAlways: true,
    arrayBracketSpacing: false,
    objectCurlySpacing: false,
  };

  /*
    Find and store all import specifiers from gtp-shared-components
    eg: import {colors, Icons} from '@walmart/gtp-shared-components'
    specifiers = colors, Icons
  */
  var specifiers: any[] = [];

  /*
    Find and store all props in JSXSpreadAttribute outside of the component.
    eg:
    const captionProps = {
      weight: '400'
      style: styles.caption
    }
  */
  var propsInjected: string[] = [];

  /* Get ld Component Names from next Directory  */
  // eslint-disable-next-line no-path-concat
  const DIRECTORY_PATH = __dirname + '/../src/next/components';
  const fs = require('fs');
  const folderEntries = fs.readdirSync(DIRECTORY_PATH, {withFileTypes: true});
  var lDComponentNames = folderEntries
    .filter(
      (entry: {name: any; isFile: () => any}) =>
        entry.isFile() &&
        !entry.name.startsWith('_') && // Don't get component names starting with _. Example _Gap.
        entry.name.endsWith('tsx'),
    )
    .map((entry: {name: any}) => entry.name.replace('.tsx', '')); // remove .tsx in filename

  /* Get all GTP imports */
  const gtpImports = root
    .find(j.ImportDeclaration)
    .filter((path: {node: {source: {value: string}}}) => {
      return path.node.source.value.startsWith(
        '@walmart/gtp-shared-components',
      );
    });

  /*
    Check all components from @walmart/gtp-shared-components in current file and
    only update those components with UNSAFE_style.
  */
  const storeSpecifiers = (path: {
    node: {specifiers: {imported: {name: string}; local: {name: string}}[]};
  }) => {
    specifiers.push(
      ...path.node.specifiers
        .map((specifier: {imported: {name: string}; local: {name: string}}) => {
          // Only update the Style for LD Components
          // Special case - Check Default Import name and Return local name instead of imported name.
          // Because if the consumer is using alias for specifier.
          // Example: import {Body as structure} from @walmart/gtp-shared-components.
          // Then check Body with LD Components and update structure style with UNSAFE_style.
          if (
            !lDComponentNames.includes(specifier.local.name) &&
            !lDComponentNames.includes(specifier.imported.name)
          ) {
            return;
          }
          return specifier.local.name;
        })
        .filter(Boolean),
    );
  };

  /* Find all our LD Components in Code with Component name */
  const findLDComponent = (name: string) =>
    root
      .find(j.JSXElement)
      .filter(
        (path: {value: {openingElement: {name: {name: string}}}}) =>
          path.value.openingElement.name.name === name,
      );

  /* Replace all the LD Components style with UNSAFE_style */
  const updateStyleProp = (
    component: Collection<namedTypes.JSXElement>,
    componentName: string,
  ) => {
    /* Scenario 1: Update Style Prop declared outside for a component using JSXSpreadAttributes.*/
    component
      .find(j.JSXSpreadAttribute)
      .forEach((path: {value: {argument: {name: any}}}) => {
        propsInjected.push(path.value.argument.name);
      });

    propsInjected.forEach((prop: any) => {
      root
        .findVariableDeclarators(prop)
        .forEach((entry: {value: {init: {properties: any}}}) => {
          if (entry.value.init) {
            const properties = entry.value.init.properties;
            properties.forEach((element: {key: {name: string}}) => {
              if (element.key.name === 'style') {
                element.key.name = 'UNSAFE_style';
              }
            });
          }
        });
    });

    /* Scenario 2: Update Style Prop declared directly under component tag.*/
    component
      .find(j.JSXAttribute)
      .filter(
        (attribute: {
          node: {name: {name: string}};
          parent: {node: {name: {name: string}}};
        }) => {
          // Check if the immediate parent JSX Element is our Component.
          // This condition is to not update the nested styles in a component.
          if (
            attribute.node.name.name === 'style' &&
            attribute.parent.node.name.name === componentName
          ) {
            attribute.node.name.name = 'UNSAFE_style';
          }
        },
      );
  };

  gtpImports.forEach(storeSpecifiers);

  specifiers.forEach((lDComponentName: string) => {
    updateStyleProp(findLDComponent(lDComponentName), lDComponentName);
  });

  return root.toSource(printOptions);
}
