module.exports = {
  component: {
    tabNavigation: {
      item: {
        alignHorizontal: {
          value: "center",
        },

        alignVertical: {
          value: "center",
        },

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

        borderColorBottom: {
          value: "{semantic.color.separator}",
        },

        borderWidthBottom: {
          value: "{primitive.scale.border.width.100}",
        },

        height: {
          value: "{primitive.scale.space.600}",
        },

        paddingHorizontal: {
          value: "{primitive.scale.space.200}",
        },

        textWrap: {
          value: false,
        },
      },
    },
  },
};
