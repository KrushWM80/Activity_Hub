const fs = require('fs');
const path = require('path');
const docgen = require('react-docgen-typescript');

const generatePageMDX = require('./generatePageMDX');

const pluginName = 'component-docs-plugin';

async function componentsPlugin(_, options) {
  const {
    // Docs Directory - website/docs/*
    ldComponentDocsRootDir,
    axComponentDocsRootDir,
    utilityDocsRootDir,

    // Library Directory - src/next/*
    ldComponentRootDir,
    axComponentRootDir,
    utilsRootDir,

    // Component pages
    ldComponents,
    axComponents,

    // utility pages
    utilities
  } = options;

  function createCategory(label, dir = '.',docsRootDir) {
    const categoryJSON = JSON.stringify({label}, undefined, 2);
    const docsCategoryDir = path.join(docsRootDir, dir);
    if (!fs.existsSync(docsCategoryDir)) {
      fs.mkdirSync(docsCategoryDir);
    }
    fs.writeFileSync(
      path.join(docsCategoryDir, `_category_.json`),
      categoryJSON,
    );
  }

  function createPageForComponent(targetArray, source) {
    const [item, subitem] = targetArray;
    const target = subitem ? `${item}/${subitem}` : item;
    const targetPath = target + '.mdx';
    const sourcePath = source + '.tsx';
    const componentPath = path.join(ldComponentRootDir, sourcePath);
    const tsPath = path.join(
      path.resolve('./tsconfig.json'),
      '..',
      '..',
      'tsconfig.json',
    );

    const {parse} = docgen.withCustomConfig(tsPath, {
      propFilter(prop) {
        // TODO: Temporarily add aria-label and ariaLabel to stop regenerating docs.
        if (
          ['className', 'style', 'aria-label', 'ariaLabel'].includes(prop.name)
        ) {
          return false;
        }

        // Remove props from React-native
        if (
          prop.declarations.some((declaration) => {
            return declaration.fileName.includes('react-native');
          })
        ) {
          return false;
        }

        if (
          prop.declarations.every((declaration) => {
            return (
              declaration.fileName.includes('@types') ||
              declaration.fileName.includes('node_modules/typescript/')
            );
          })
        ) {
          return false;
        }

        return true;
      },

      shouldExtractLiteralValuesFromEnum: true,
    });

    const parsed = parse(componentPath);

    // Create directory for the output mdx file.
    fs.mkdirSync(
      path.join(ldComponentDocsRootDir, targetPath).split('/').slice(0, -1).join('/'),
      {recursive: true},
    );

    const parsedObj = parsed.length > 0 ? parsed[0] : {};
    // TODO: Move this to common function, checking if props are empty
    if (Object.keys(parsedObj.props).length === 0) {
      console.log(`❌❌❌❌❌ WARNING: Props Not Found for component ${parsedObj.displayName} ❌❌❌❌❌`);
      throw new Error('Props Not Found for component ' + parsedObj.displayName);
    }

    const mdxStr =  generatePageMDX(parsedObj, source);
    const mdxStrClean = mdxStr.replace(/\n+$/, '\n');

    fs.rmSync(path.join(ldComponentDocsRootDir, targetPath), {force: true});

    // Generate and write mdx file.
    fs.writeFileSync(
      path.join(ldComponentDocsRootDir, targetPath),
      mdxStrClean,
    );

    return parsedObj;
  }

  function createPageForAXComponent(targetArray, source) {
    const [item, subitem] = targetArray;
    const target = subitem ? `${item}/${subitem}` : item;
    const targetPath = target + '.mdx';
    const sourcePath = source + '.tsx';
    const componentPath = path.join(axComponentRootDir, sourcePath);
    const tsPath = path.join(
      path.resolve('./tsconfig.json'),
      '..',
      '..',
      'tsconfig.json',
    );

    const {parse} = docgen.withCustomConfig(tsPath, {
      propFilter(prop) {
        // TODO: Temporarily add aria-label and ariaLabel to stop regenerating docs.
        if (
          ['className', 'style', 'aria-label', 'ariaLabel'].includes(prop.name)
        ) {
          return false;
        }

        // Remove props from React-native
        if (
          prop.declarations.some((declaration) => {
            return declaration.fileName.includes('react-native');
          })
        ) {
          return false;
        }

        if (
          prop.declarations.every((declaration) => {
            return (
              declaration.fileName.includes('@types') ||
              declaration.fileName.includes('node_modules/typescript/')
            );
          })
        ) {
          return false;
        }

        return true;
      },

      shouldExtractLiteralValuesFromEnum: true,
    });

    const parsed = parse(componentPath);

    // Create directory for the output mdx file.
    fs.mkdirSync(
      path.join(axComponentDocsRootDir, targetPath).split('/').slice(0, -1).join('/'),
      {recursive: true},
    );

    const parsedObj = parsed.length > 0 ? parsed[0] : {};
    // TODO: Move this to common function, checking if props are empty
    if (Object.keys(parsedObj.props).length === 0) {
      console.log(`❌❌❌❌❌ WARNING: Props Not Found for component ${parsedObj.displayName} ❌❌❌❌❌`)
      throw new Error('Props Not Found for component ' + parsedObj.displayName);
    }

    const mdxStr =  generatePageMDX(parsedObj, source);
    const mdxStrClean = mdxStr.replace(/\n+$/, '\n');

    fs.rmSync(path.join(axComponentDocsRootDir, targetPath), {force: true});

    // Generate and write mdx file.
    fs.writeFileSync(
      path.join(axComponentDocsRootDir, targetPath),
      mdxStrClean,
    );

    return parsedObj;
  }

  function createPageForUtility(targetArray, source) {
    const [item, subitem] = targetArray;
    const target = subitem ? `${item}/${subitem}` : item;
    const targetPath = target + '.mdx';
    var sourcePath = '';

    if (fs.existsSync(path.join(utilsRootDir, source + '.tsx'))) {
      sourcePath = source + '.tsx'
    } else if (fs.existsSync(path.join(utilsRootDir, source + '.ts'))) {
      sourcePath = source + '.ts'
    } else {
      return {}
    }
    const utilityPath = path.join(utilsRootDir, sourcePath);

    const tsPath = path.join(
      path.resolve('./tsconfig.json'),
      '..',
      '..',
      'tsconfig.json',
    );

    const {parse} = docgen.withCustomConfig(tsPath, {
      propFilter(prop) {
        // TODO: Temporarily add aria-label and ariaLabel to stop regenerating docs.
        if (
          ['className', 'style', 'aria-label', 'ariaLabel'].includes(prop.name)
        ) {
          return false;
        }

        // Remove props from React-native
        if (
          prop.declarations.some((declaration) => {
            return declaration.fileName.includes('react-native');
          })
        ) {
          return false;
        }

        if (
          prop.declarations.every((declaration) => {
            return (
              declaration.fileName.includes('@types') ||
              declaration.fileName.includes('node_modules/typescript/')
            );
          })
        ) {
          return false;
        }

        return true;
      },

      shouldExtractLiteralValuesFromEnum: true,
    });

    const parsed = parse(utilityPath);

    // Create directory for the output mdx file.
    fs.mkdirSync(
      path.join(utilityDocsRootDir, targetPath).split('/').slice(0, -1).join('/'),
      {recursive: true},
    );

    const parsedObj = parsed.length > 0 ? parsed[0] : {};
    const mdxStr =  generatePageMDX(parsedObj, source);
    const mdxStrClean = mdxStr.replace(/\n+$/, '\n');

    fs.rmSync(path.join(utilityDocsRootDir, targetPath), {force: true});

    // Generate and write mdx file.
    fs.writeFileSync(
      path.join(utilityDocsRootDir, targetPath),
      mdxStrClean,
    );

    return parsedObj;
  }

  return {
    name: pluginName,
    async loadContent() {
      const docs = {};

      // COMPONENT DOC GENERATION
      // Create root components category.
      createCategory('LD Components', '.', ldComponentDocsRootDir);

      // Generate Docs for Components
      for (const item in ldComponents) {
        if (typeof ldComponents[item] === 'string') {
          const doc = createPageForComponent([item], ldComponents[item]);
          docs[ldComponents[item]] = doc;
        } else {
          for (const subitem in ldComponents[item]) {
            const doc = createPageForComponent(
              [item, subitem],
              ldComponents[item][subitem],
            );
            docs[ldComponents[item][subitem]] = doc;
          }
        }
      }

      // AX COMPONENTax DOC GENERATION
      // Create root  components category.
      createCategory('AX Components', '.', axComponentDocsRootDir);

      // Generate Docs for Components
      for (const item in axComponents) {
        if (typeof axComponents[item] === 'string') {
          const doc = createPageForAXComponent([item], axComponents[item]);
          docs[axComponents[item]] = doc;
        } else {
          for (const subitem in axComponents[item]) {
            const doc = createPageForAXComponent(
              [item, subitem],
              axComponents[item][subitem],
            );
            docs[axComponents[item][subitem]] = doc;
          }
        }
      }


      // UTILITIES DOC GENERATION
      // Create root utilities category.
      createCategory('Utilities', '.', utilityDocsRootDir);

      // Generate Docs for Utilities
      for (const item in utilities) {
        if (typeof utilities[item] === 'string') {
          const doc = createPageForUtility([item], utilities[item]);
          docs[utilities[item]] = doc;
        } else {
          for (const subitem in utilities[item]) {
            const doc = createPageForUtility(
              [item, subitem],
              utilities[item][subitem],
            );
            docs[utilities[item][subitem]] = doc;
          }
        }
      }

      return docs;
    },
    async contentLoaded({content: docs, actions}) {
      // Store component docs global data so it can be used in `PropsTable` component.
      actions.setGlobalData({
        docs,
      });
    },
  };
}

module.exports = componentsPlugin;
