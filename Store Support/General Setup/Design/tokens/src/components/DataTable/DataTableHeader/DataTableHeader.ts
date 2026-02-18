module.exports = {
  component: {
    dataTable: {
      header: {
        alignVertical: {
          value: "center",
        },

        alignment: {
          left: {
            alignHorizontal: {
              value: "start",
            },

            textAlign: {
              value: "left",
            },
          },

          right: {
            alignHorizontal: {
              value: "end",
            },

            textAlign: {
              value: "right",
            },
          },
        },

        backgroundColor: {
          value: "{semantic.color.surface.subtle._}",
        },

        padding: {
          value: "{primitive.scale.space.200}",
        },

        state: {
          isSortable: {
            backgroundColor: {
              _: {
                value: "{semantic.color.surface.subtle._}",
              },

              hovered: {
                value: "{semantic.color.surface.subtle.hovered}",
              },

              focused: {
                value: "{semantic.color.surface.subtle.focused}",
              },

              pressed: {
                value: "{semantic.color.surface.subtle.pressed}",
              },
            },
          },
        },
      },
    },
  },
};
