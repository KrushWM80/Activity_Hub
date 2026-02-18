module.exports = {
  component: {
    skeleton: {
      container: {
        animation: {
          _: {
            direction: { value: "alternate" },
            duration: {
              attributes: {
                category: "time",
              },
              value: 750,
            },

            iterationCount: { value: "infinite" },
            timing: { value: "{primitive.timing.linear.100}" },

            keyframes: {
              from: {
                backgroundColor: { value: "{semantic.color.loading.subtlest}" },
              },

              to: {
                backgroundColor: { value: "{semantic.color.loading.subtle}" },
              },
            },
          },

          magic: {
            direction: { value: "normal" },
            duration: {
              attributes: {
                category: "time",
              },
              value: 1600,
            },

            iterationCount: { value: "infinite" },
            timing: { value: "{primitive.timing.easeOut.100}" },

            keyframes: {
              start: {
                backgroundColor: {
                  value: "{semantic.color.loading.magic.subtle}",
                },
              },

              middle: {
                backgroundColor: {
                  value: "{semantic.color.loading.magic._}",
                },
              },

              end: {
                backgroundColor: {
                  value: "{semantic.color.loading.magic.subtle}",
                },
              },
            },
          },
        },

        backgroundColor: {
          value: "{semantic.color.loading.subtlest}",
        },

        height: {
          value: "{primitive.scale.space.400}",
        },

        variant: {
          rectangle: {
            borderRadius: {
              value: "{primitive.scale.border.radius.50}",
            },
          },

          rounded: {
            borderRadius: {
              value: "{primitive.scale.border.radius.round}",
            },
          },
        },

        width: {
          value: "fill-parent",
        },
      },
    },
  },
};
