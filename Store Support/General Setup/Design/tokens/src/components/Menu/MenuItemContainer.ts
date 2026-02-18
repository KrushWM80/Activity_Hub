module.exports = {
  component: {
    menu: {
      itemContainer: {
        alignVertical: {
          value: "center",
        },

        backgroundColor: {
          _: {
            value: "{semantic.color.action.fill.transparent._}",
          },

          hovered: {
            value: "{semantic.color.action.fill.transparent.hovered}",
          },

          focused: {
            value: "{semantic.color.action.fill.transparent.focused}",
          },

          pressed: {
            value: "{semantic.color.action.fill.transparent.pressed}",
          },

          disabled: {
            value: "{semantic.color.action.fill.transparent.disabled}",
          },
        },

        paddingHorizontal: {
          value: "{primitive.scale.space.200}",
        },

        paddingVertical: {
          value: "{primitive.scale.space.100}",
        },
      },
    },
  },
};
