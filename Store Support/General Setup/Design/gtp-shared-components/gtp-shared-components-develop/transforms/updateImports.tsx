/*
  TRANSFORM NAME - updateImports
  This transform is meant to be run only on consumer app:
  It needs to be run by devs manually using npx runCodemods <transform> <path>.
  It performs the following:
    - All imports have been simplified so that now you can import from root instead of `dist`.
    - This transform will run on consumer code to find old imports from dist and modify from root.
  Example:
    BEFORE - >  import colors from '@walmart/gtp-shared-components/dist/theme/colors.json';
                import IconButton from '@walmart/gtp-shared-components/dist/buttons/icon-button';

    AFTER - >   import {colors, IconButton} from '@walmart/gtp-shared-components';
*/

import {API, FileInfo, ImportSpecifier, Options} from 'jscodeshift';
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
    Stores all import specifiers
    eg: import {colors, Icons} from '@walmart/gtp-shared-components'
    specifiers = colors, Icons
  */
  let specifiers: any[] = [];

  /*
    Remove all imports with @walmart/gtp-shared-components/dist and store the specifiers.
  */
  //@ts-ignore
  const removeImport = (path) => {
    specifiers.push(
      //@ts-ignore
      ...path.node.specifiers.map((specifier) => {
        if (specifier?.imported?.name) {
          return specifier.imported.name === specifier.local.name
            ? specifier.local.name
            : specifier.imported.name + ' as ' + specifier.local.name;
        } else {
          return specifier.local.name;
        }
      }),
    );

    // Replace with empty line.
    path.replace();
  };

  /*
    Create new import from @walmart/gtp-shared-components with stored specifiers.
  */
  const createNewImport = (importSpecifier: ImportSpecifier) => {
    return j.importDeclaration(
      [importSpecifier],
      j.stringLiteral('@walmart/gtp-shared-components'),
    );
  };

  /* Get all GTP New imports from dist */
  const gtpNewImports = root
    .find(j.ImportDeclaration)
    .filter(
      (path) => path.node.source.value === '@walmart/gtp-shared-components',
    );

  /* Get all GTP Old imports from dist */
  const gtpOldImports = root.find(j.ImportDeclaration).filter((path) => {
    return (
      // @ts-ignore
      path.node.source.value.startsWith('@walmart/gtp-shared-components/dist')
    );
  });

  /* Remove and Store specifiers */
  gtpOldImports.forEach(removeImport);
  gtpNewImports.forEach(removeImport);

  /*
    Sort all the specifiers.
    Convert specifiers from string to importSpecifier.
  */
  specifiers.sort((a, b) => a.localeCompare(b));
  specifiers.map((specifier) => {
    return j.importSpecifier(j.identifier(specifier));
  });

  /* Create a New GTP Import with specifiers updated if only Old imports are present*/
  if (gtpOldImports.length) {
    const newGTPImportSpecifiers = j.importSpecifier(
      j.identifier(specifiers.join(', ')),
    );

    /*
    Get all Imports from File.
    Insert the New Import after all imports.
    */
    const allImportsInFile = root.find(j.ImportDeclaration);
    const allImportsLength = allImportsInFile.length;
    const newCreatedGTPImport = createNewImport(newGTPImportSpecifiers);
    if (allImportsInFile.length) {
      j(allImportsInFile.at(allImportsLength - 1).get()).insertAfter(
        newCreatedGTPImport,
      );
    } else {
      root.get().node.program.body.unshift(newCreatedGTPImport);
    }
  } else {
    /*
      No Changes Needed if there are No Old GTP Imports.
      Return Original Source
     */
    return j(file.source).toSource();
  }

  return root.toSource(printOptions);
}
