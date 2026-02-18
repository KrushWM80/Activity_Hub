module.exports = {
  component: {
    progressTracker: {
      itemTextLabel: {
        aliasName: {
          value: "text.caption",
        },

        paddingBottom: {
          value: "0px",
        },

        paddingEnd: {
          value: "{primitive.scale.space.50}",
        },

        paddingStart: {
          value: "{primitive.scale.space.50}",
        },

        paddingTop: {
          value: "{primitive.scale.space.50}",
        },

        state: {
          activated: {
            textColor: {
              value: "{semantic.color.text._}",
            },
          },

          isFirst: {
            paddingStart: {
              value: "0px",
            },

            textAlign: {
              value: "left",
            },
          },

          isLast: {
            paddingEnd: {
              value: "0px",
            },

            textAlign: {
              value: "right",
            },
          },
        },

        textAlign: {
          value: "center",
        },

        textColor: {
          value: "{semantic.color.text.subtlest}",
        },
      },
    },
  },
};
