module.exports = {
  component: {
    dataTable: {
      cellInlineEditTextAreaIndicatorContainer: {
        alignHorizontal: {
          value: "start",
        },

        alignVertical: {
          value: "start",
        },

        gap: {
          value: "{primitive.scale.space.100}",
        },

        variant: {
          alphanumeric: {
            direction: {
              value: "row",
            },
          },

          numeric: {
            direction: {
              value: "row-reverse",
            },
          },
        },

        visibility: {
          _: {
            value: "hidden",
          },

          hovered: {
            value: "visible",
          },

          focused: {
            value: "visible",
          },

          pressed: {
            value: "visible",
          },
        },
      },
    },
  },
};
