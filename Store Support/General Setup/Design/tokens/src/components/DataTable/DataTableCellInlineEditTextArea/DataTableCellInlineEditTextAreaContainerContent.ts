module.exports = {
  component: {
    dataTable: {
      cellInlineEditTextAreaContainerContent: {
        alignHorizontal: {
          value: "start",
        },

        alignVertical: {
          value: "center",
        },

        gap: {
          value: "{primitive.scale.space.100}",
        },

        paddingBottom: {
          value: "{primitive.scale.space.200}",
        },

        paddingTop: {
          value: "{primitive.scale.space.200}",
        },

        state: {
          error: {
            paddingBottom: {
              value: "{primitive.scale.space.100}",
            },
          },
        },

        variant: {
          alphanumeric: {
            direction: {
              value: "row",
            },

            paddingEnd: {
              value: "{primitive.scale.space.100}",
            },

            paddingStart: {
              value: "{primitive.scale.space.200}",
            },
          },

          numeric: {
            direction: {
              value: "row-reverse",
            },

            paddingEnd: {
              value: "{primitive.scale.space.200}",
            },

            paddingStart: {
              value: "{primitive.scale.space.100}",
            },
          },
        },
      },
    },
  },
};
