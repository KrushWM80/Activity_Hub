const config = require('../docusaurus.config');

const {baseUrl, customFields} = config;

function renderBadge(annotation) {
  const [annotType, ...annotLabel] = annotation.split(' ');

  // eslint-disable-next-line prettier/prettier
  return `<span class="badge badge-${annotType.replace('@','',)} "><span class="badge-text">${
    annotType.replace('@', '').toUpperCase() + ' - ' + annotLabel.join(' ')}</span></span>`;
}

function generateKnownIssues(componentName) {
  const componentKnownIssues = customFields.knownIssues[componentName];

  if (!componentKnownIssues) {
    return ``;
  }

  const issues = Object.entries(componentKnownIssues)
    .map(([key, value]) => {
      return `
        <li key="${key}">
          <a href="${value}">${key}</a>
        </li>
    `;
    })
    .join('');

  return `
  ## Known Issues

  <details>
    <ul>
      ${issues}
    </ul>
  </details>
  `;
}

function generateMoreExamples(componentName) {
  const componentMoreExamples = customFields.moreExamples[componentName];

  if (!componentMoreExamples) {
    return ``;
  }

  const links = Object.entries(componentMoreExamples)
    .map(([key, value]) => {
      return `
        <li key="${key}">
          <a href="${value}">${key}</a>
        </li>
    `;
    })
    .join('');

  return `
  ## More Examples
  <details>
    <summary>Toggle to grab more examples</summary>
    <ul>
      ${links}
    </ul>
  </details>
  `;
}

function generateScreenshots(componentName, screenshotData) {
  if (!screenshotData) {
    return '';
    // return `#### screenshots coming soon ...`; // Some components don't have screenshots
  }

  return `<ScreenshotTabs screenshotData={${screenshotData}} baseUrl="${baseUrl}"/>`;
}

function generatePropsTable(data, link, extendsAttributes) {
  const ANNOTATION_OPTIONAL = '@optional';
  const ANNOTATION_INTERNAL = '@internal';

  const props = Object.entries(data)
    .map(([prop, value]) => {
      if (!value.description) {
        value.description = '';
      }
      // Remove @optional annotations from descriptions.
      if (value.description.includes(ANNOTATION_OPTIONAL)) {
        value.description = value.description.replace(ANNOTATION_OPTIONAL, '');
      }
      // Hide props with @internal annotations.
      if (value.description.includes(ANNOTATION_INTERNAL)) {
        return;
      }

      let leadingBadge = '';
      let descriptionByLines = value.description?.split('\n');

      // Find leading badge and put it next after prop name.
      if (descriptionByLines?.[0].includes('@')) {
        leadingBadge = descriptionByLines[0];
      }

      return `\n ### ${prop}${value.required ? '(required)' : ''}${leadingBadge && renderBadge(leadingBadge)}\n<PropTable componentLink="${link}" prop="${prop}"/>`;}).join('');

  if (!props) {
    return ``;
  }

  return `## Props\n${props}`;
  // We dont have extended attributes for now. We can add it to above generatePropsTable() later if needed.
  // ${
  //   extendsAttributes.length === 0
  //     ? `<span />`
  //     : `### ${extendsAttributes?.[0]?.name}`
  // }
  // ${extendsAttributes
  //   .map((attr) => {
  //     return `<ExtendsLink name="${attr.name}" link="${attr.link}" />`;
  //   })
  //   .join('')}

}

function generateExtendsAttributes(doc) {
  const ANNOTATION_EXTENDS = '@extends';

  const extendsAttributes = [];
  doc?.description
    .split('\n')
    .filter((line) => {
      if (line.startsWith(ANNOTATION_EXTENDS)) {
        const parts = line.split(' ').slice(1);
        const link = parts.pop();
        extendsAttributes.push({
          name: parts.join(' '),
          link,
        });
        return false;
      }
      return true;
    })
    .join('\n');

  return extendsAttributes;
}

function generatePageMDX(doc, link) {
  const summaryRegex = /([\s\S]*?)## Usage/;

  const description = doc.description
    .replace(/<\/br>/g, '')
    .replace(/style="[a-zA-Z0-9:;.\s()\-,]*"/gi, '')
    .replace(/src="screenshots/g, `src="${baseUrl}screenshots`)
    .replace(/@extends.+$/, '');

  const summary = summaryRegex.exec(description)
    ? summaryRegex.exec(description)[1]
    : '';
  const usage = description.replace(summary, '');

  const screenshotData = JSON.stringify(
    customFields.screenshots[doc.displayName],
  );

  const extendsAttributes = generateExtendsAttributes(doc);

  const mdx = `
---
title: ${doc.displayName}
---

import PropTable from '@site/src/components/PropTable.tsx';
import ScreenshotTabs from '@site/src/components/ScreenshotTabs.tsx';

${summary}
${generateScreenshots(doc.displayName, screenshotData)}
${usage}
${generatePropsTable(doc.props, link, extendsAttributes)}
${generateMoreExamples(doc.displayName)}
${generateKnownIssues(doc.displayName)}
`;

  return mdx.slice(1);
}

module.exports = generatePageMDX;
