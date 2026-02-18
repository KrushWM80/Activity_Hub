module.exports = {
  component: {
    dataTable: {
      cellInlineEditTextAreaTextLabel: {
        aliasName: {
          value: "text.body",
        },

        aliasOptions: {
          size: {
            value: "medium",
          },
        },

        textColor: {
          value: "{semantic.color.text._}",
        },

        variant: {
          alphanumeric: {
            textAlign: {
              value: "left",
            },
          },

          numeric: {
            aliasOptions: {
              isMonospace: {
                value: true,
              },
            },

            textAlign: {
              value: "right",
            },
          },
        },
      },
    },
  },
};
