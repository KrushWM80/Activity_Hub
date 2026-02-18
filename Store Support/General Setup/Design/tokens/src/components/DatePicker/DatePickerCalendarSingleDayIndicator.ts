module.exports = {
  component: {
    datePicker: {
      calendarSingleDayIndicator: {
        backgroundColor: {
          _: {
            value: "{semantic.color.fill._}",
          },

          hovered: {
            value: "{semantic.color.fill.hovered}",
          },

          focused: {
            value: "{semantic.color.fill.focused}",
          },

          pressed: {
            value: "{semantic.color.fill.pressed}",
          },

          disabled: {
            value: "{semantic.color.fill.disabled}",
          },
        },

        borderRadius: {
          value: "{primitive.scale.border.radius.round}",
        },

        height: {
          value: "{primitive.scale.space.600}",
        },

        paddingHorizontal: {
          value: "0px",
        },

        paddingVertical: {
          value: "{primitive.scale.space.150}",
        },

        state: {
          isSelected: {
            backgroundColor: {
              _: {
                value: "{semantic.color.fill.activated._}",
              },

              hovered: {
                value: "{semantic.color.fill.activated.hovered}",
              },

              focused: {
                value: "{semantic.color.fill.activated.focused}",
              },

              pressed: {
                value: "{semantic.color.fill.activated.pressed}",
              },

              disabled: {
                value: "{semantic.color.fill.activated.disabled}",
              },
            },
          },

          isToday: {
            borderColor: {
              _: {
                value: "{semantic.color.border.activated}",
              },

              hovered: {
                value: "{semantic.color.border.activated}",
              },

              focused: {
                value: "{semantic.color.border.activated}",
              },

              pressed: {
                value: "{semantic.color.border.activated}",
              },

              disabled: {
                value: "{semantic.color.border.disabled}",
              },
            },

            borderWidth: {
              _: {
                value: "{semantic.scale.border.width.interactive.activated._}",
              },

              hovered: {
                value:
                  "{semantic.scale.border.width.interactive.activated.hovered}",
              },

              focused: {
                value:
                  "{semantic.scale.border.width.interactive.activated.focused}",
              },

              pressed: {
                value:
                  "{semantic.scale.border.width.interactive.activated.pressed}",
              },

              disabled: {
                value: "{semantic.scale.border.width.interactive.activated._}",
              },
            },
          },
        },

        width: {
          value: "{primitive.scale.space.600}",
        },
      },
    },
  },
};
