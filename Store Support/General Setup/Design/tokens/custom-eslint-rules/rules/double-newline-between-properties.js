module.exports = {
  meta: {
    type: "layout",
    docs: {
      description:
        "Enforce double newline between object properties of type object",
      recommended: "error",
    },
    fixable: "code",
    schema: [], // no options
    messages: {
      expectedDoubleNewlines:
        "Expected double newlines between object properties when the next property is an object, found {{linesBetweenProperties}}.",
    },
  },
  create(context) {
    return {
      Property(node) {
        if (
          node.value.type !== "ObjectExpression" ||
          node.parent.type !== "ObjectExpression"
        ) {
          return;
        }

        const parentProperties = node.parent.properties;
        const nodeIndex = parentProperties.indexOf(node);

        // Check if this is the last property
        if (nodeIndex >= parentProperties.length - 1) {
          return;
        }

        // Get next sibling property
        const nextProperty = parentProperties[nodeIndex + 1];

        // If next property is an object
        if (nextProperty.value.type === "ObjectExpression") {
          // If current object expression is on a single line
          if (node.loc.start.line === node.loc.end.line) {
            return;
          }
          const linesBetweenProperties =
            nextProperty.loc.start.line - node.loc.end.line;

          // Check if there are less than 2 or more than 2 lines between the properties
          if (linesBetweenProperties !== 2) {
            context.report({
              node: nextProperty,
              messageId: "expectedDoubleNewlines",
              data: {
                linesBetweenProperties,
              },
              fix(fixer) {
                return fixer.replaceTextRange(
                  [node.range[1] + 1, nextProperty.range[0]],
                  "\n\n" + " ".repeat(node.loc.start.column),
                );
              },
            });
          }
        }
      },
    };
  },
};
