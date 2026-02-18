module.exports = {
  component: {
    dataTable: {
      cellInlineEditTextAreaContainer: {
        borderColor: {
          _: {
            value: "{semantic.color.field.border._}",
          },

          hovered: {
            value: "{semantic.color.field.border.hovered}",
          },

          focused: {
            value: "{semantic.color.field.border.focused}",
          },

          pressed: {
            value: "{semantic.color.field.border.focused}",
          },
        },

        borderWidth: {
          _: {
            value: "0px",
          },

          hovered: {
            value: "{semantic.scale.border.width.interactive.hovered}",
          },

          focused: {
            value: "{semantic.scale.border.width.interactive.focused}",
          },

          pressed: {
            value: "{semantic.scale.border.width.interactive.pressed}",
          },
        },

        state: {
          error: {
            backgroundColor: {
              value: "{semantic.color.fill.negative.subtle}",
            },
          },
        },
      },
    },
  },
};
