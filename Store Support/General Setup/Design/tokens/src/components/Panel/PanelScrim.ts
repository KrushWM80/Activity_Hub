module.exports = {
  component: {
    panel: {
      scrim: {
        aliasName: {
          value: "component.overlay.scrim",
        },

        state: {
          enterActive: {
            transitionDuration: {
              value: "{primitive.duration.200}",
            },
          },

          exitActive: {
            transitionDelay: {
              value: "{primitive.duration.200}",
            },

            transitionDuration: {
              value: "{primitive.duration.300}",
            },
          },
        },
      },
    },
  },
};
