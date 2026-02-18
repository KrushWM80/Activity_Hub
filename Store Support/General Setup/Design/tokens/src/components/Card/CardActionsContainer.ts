module.exports = {
  component: {
    card: {
      actionsContainer: {
        alignHorizontal: {
          value: "end",
        },

        borderColorTop: {
          value: "{semantic.color.separator}",
        },

        borderWidthTop: {
          value: "{primitive.scale.border.width.100}",
        },

        size: {
          small: {
            marginVertical: {
              value: "{primitive.scale.space.200}",
            },

            paddingHorizontal: {
              value: "{primitive.scale.space.200}",
            },
          },

          large: {
            marginVertical: {
              value: "{primitive.scale.space.300}",
            },

            paddingHorizontal: {
              value: "{primitive.scale.space.300}",
            },
          },
        },
      },
    },
  },
};
