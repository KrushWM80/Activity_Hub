module.exports = {
  component: {
    dataTable: {
      cellBulkEditTextAreaValue: {
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
              state: {
                isMonospace: {
                  value: true,
                },
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
