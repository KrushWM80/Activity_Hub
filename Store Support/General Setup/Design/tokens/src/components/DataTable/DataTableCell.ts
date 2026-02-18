module.exports = {
  component: {
    dataTable: {
      cell: {
        aliasName: {
          value: "text.body",
        },

        aliasOptions: {
          size: {
            value: "medium",
          },
        },

        padding: {
          value: "{primitive.scale.space.200}",
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
