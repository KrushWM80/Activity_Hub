module.exports = {
  component: {
    bottomSheet: {
      header: {
        alignVertical: {
          value: "start",
        },

        direction: {
          value: "row-reverse",
        },

        gap: {
          value: "{primitive.scale.space.200}",
        },

        paddingEnd: {
          bS: {
            value: "{primitive.scale.space.100}",
          },

          bM: {
            value: "{primitive.scale.space.200}",
          },
        },

        paddingStart: {
          bS: {
            comment:
              "Add bottomSheet.header.paddingEnd.bS and bottomSheet.closeButton's width such that the bottomSheet.title appears centered.",
            value: "48px",
          },

          bM: {
            comment:
              "Add bottomSheet.header.paddingEnd.bM and bottomSheet.closeButton's width such that the bottomSheet.title appears centered.",
            value: "56px",
          },
        },

        paddingVertical: {
          bS: {
            value: "{primitive.scale.space.100}",
          },

          bM: {
            value: "{primitive.scale.space.200}",
          },
        },
      },
    },
  },
};
