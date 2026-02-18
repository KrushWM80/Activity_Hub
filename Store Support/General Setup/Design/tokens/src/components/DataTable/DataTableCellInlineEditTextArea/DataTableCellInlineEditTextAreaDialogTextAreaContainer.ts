module.exports = {
  component: {
    dataTable: {
      cellInlineEditTextAreaDialogTextAreaContainer: {
        backgroundColor: {
          _: {
            value: "{semantic.color.field.fill._}",
          },

          hovered: {
            value: "{semantic.color.field.fill.hovered}",
          },

          focused: {
            value: "{semantic.color.field.fill.focused}",
          },
        },

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

        borderRadius: {
          value: "{primitive.scale.border.radius.50}",
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

        paddingVertical: {
          value: "{primitive.scale.space.150}",
        },

        state: {
          error: {
            backgroundColor: {
              _: {
                value: "{semantic.color.field.fill.negative._}",
              },

              hovered: {
                value: "{semantic.color.field.fill.negative.hovered}",
              },

              focused: {
                value: "{semantic.color.field.fill.negative.focused}",
              },

              disabled: {
                value: "{semantic.color.field.fill.negative.disabled}",
              },
            },

            borderColor: {
              _: {
                value: "{semantic.color.field.border.negative._}",
              },

              hovered: {
                value: "{semantic.color.field.border.negative.hovered}",
              },

              focused: {
                value: "{semantic.color.field.border.negative.focused}",
              },

              disabled: {
                value: "{semantic.color.field.border.negative.disabled}",
              },
            },
          },
        },

        variant: {
          alphanumeric: {
            paddingEnd: {
              value: "52px",
            },

            paddingStart: {
              value: "{primitive.scale.space.150}",
            },
          },

          numeric: {
            paddingEnd: {
              value: "{primitive.scale.space.150}",
            },

            paddingStart: {
              value: "52px",
            },
          },
        },
      },
    },
  },
};
