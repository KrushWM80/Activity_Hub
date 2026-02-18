module.exports = {
  component: {
    tabNavigation: {
      itemIndicator: {
        backgroundColor: {
          _: {
            value: "{semantic.color.pageNav.indicator._}",
          },

          hovered: {
            value: "{semantic.color.pageNav.indicator.hovered}",
          },

          focused: {
            value: "{semantic.color.pageNav.indicator.focused}",
          },

          pressed: {
            value: "{semantic.color.pageNav.indicator.pressed}",
          },
        },

        height: {
          value: "{primitive.scale.space.50}",
        },

        borderRadiusTopEnd: {
          value: "{primitive.scale.border.radius.25}",
        },

        borderRadiusTopStart: {
          value: "{primitive.scale.border.radius.25}",
        },

        offsetEnd: {
          value: "{primitive.scale.space.50}",
        },

        offsetStart: {
          value: "{primitive.scale.space.50}",
        },

        offsetBottom: {
          value: "1px",
        },

        state: {
          activated: {
            backgroundColor: {
              _: {
                value: "{semantic.color.pageNav.indicator.activated._}",
              },

              hovered: {
                value: "{semantic.color.pageNav.indicator.activated.hovered}",
              },

              focused: {
                value: "{semantic.color.pageNav.indicator.activated.focused}",
              },

              pressed: {
                value: "{semantic.color.pageNav.indicator.activated.pressed}",
              },
            },
          },
        },
      },
    },
  },
};
