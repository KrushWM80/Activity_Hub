module.exports = {
  component: {
    dataTable: {
      cellBulkEditTextAreaContainer: {
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
        },

        borderWidth: {
          _: {
            value: "{semantic.scale.border.width.interactive._}",
          },

          hovered: {
            value: "{semantic.scale.border.width.interactive.hovered}",
          },

          focused: {
            value: "{semantic.scale.border.width.interactive.focused}",
          },
        },

        gap: {
          value: "{primitive.scale.space.100}",
        },

        padding: {
          value: "{primitive.scale.space.200}",
        },

        state: {
          edited: {
            backgroundColor: {
              value: "{semantic.color.fill.edited.subtle}",
            },
          },

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
