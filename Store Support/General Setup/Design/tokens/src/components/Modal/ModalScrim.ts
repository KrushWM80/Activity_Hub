module.exports = {
  component: {
    modal: {
      scrim: {
        aliasName: {
          value: "component.overlay.scrim",
        },

        state: {
          enterActive: {
            transitionDuration: {
              value: "{primitive.duration.500}",
            },
          },

          exitActive: {
            transitionDuration: {
              value: "{primitive.duration.500}",
            },
          },
        },
      },
    },
  },
};
