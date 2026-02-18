module.exports = {
  component: {
    dataTable: {
      row: {
        backgroundColor: {
          _: {
            value: "{semantic.color.fill._}",
          },

          hovered: {
            value: "{semantic.color.fill.hovered}",
          },
        },

        borderBottomColor: {
          value: "{semantic.color.separator}",
        },

        borderWidthBottom: {
          value: "{primitive.scale.border.width.100}",
        },

        state: {
          activated: {
            backgroundColor: {
              _: {
                value: "{semantic.color.fill.activated.subtle._}",
              },

              hovered: {
                value: "{semantic.color.fill.activated.subtle.hovered}",
              },
            },
          },
        },
      },
    },
  },
};
