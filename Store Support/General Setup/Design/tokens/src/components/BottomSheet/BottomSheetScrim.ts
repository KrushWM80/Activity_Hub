module.exports = {
  component: {
    bottomSheet: {
      scrim: {
        aliasName: {
          value: "component.overlay.scrim",
        },

        state: {
          enterActive: {
            transitionDuration: {
              value: "{primitive.duration.300}",
            },
          },

          exitActive: {
            transitionDelay: {
              value: "{primitive.duration.400}",
            },

            transitionDuration: {
              value: "{primitive.duration.500}",
            },
          },
        },
      },
    },
  },
};
