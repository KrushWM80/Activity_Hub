module.exports = {
  component: {
    sideNavigation: {
      itemContainer: {
        backgroundColor: {
          _: {
            value: "{semantic.color.pageNav.fill._}",
          },

          hovered: {
            value: "{semantic.color.pageNav.fill.hovered}",
          },

          focused: {
            value: "{semantic.color.pageNav.fill.focused}",
          },

          pressed: {
            value: "{semantic.color.pageNav.fill.pressed}",
          },
        },

        paddingEnd: {
          value: "{primitive.scale.space.200}",
        },

        paddingStart: {
          value: "{primitive.scale.space.300}",
        },

        paddingVertical: {
          value: "{primitive.scale.space.100}",
        },

        state: {
          activated: {
            backgroundColor: {
              _: {
                value: "{semantic.color.pageNav.fill.activated._}",
              },

              hovered: {
                value: "{semantic.color.pageNav.fill.activated.hovered}",
              },

              focused: {
                value: "{semantic.color.pageNav.fill.activated.focused}",
              },

              pressed: {
                value: "{semantic.color.pageNav.fill.activated.pressed}",
              },
            },
          },
        },
      },
    },
  },
};
