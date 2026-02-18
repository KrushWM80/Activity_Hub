module.exports = {
  component: {
    panel: {
      header: {
        alignHorizontal: {
          value: "space-between",
        },

        alignVertical: {
          value: "start",
        },

        borderColorBottom: {
          value: "{semantic.color.separator}",
        },

        borderWidthBottom: {
          value: "{primitive.scale.border.width.100}",
        },

        direction: {
          value: "row-reverse",
          comment: "TODO: figure it out",
        },

        gap: {
          value: "{primitive.scale.space.100}",
        },

        paddingEnd: {
          bS: {
            value: "0px",
          },

          bM: {
            value: "{primitive.scale.space.100}",
          },
        },

        paddingStart: {
          bS: {
            value: "{primitive.scale.space.200}",
          },

          bM: {
            value: "{primitive.scale.space.300}",
          },
        },

        paddingVertical: {
          bS: {
            value: "0px",
          },

          bM: {
            value: "{primitive.scale.space.100}",
          },
        },
      },
    },
  },
};
