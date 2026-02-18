module.exports = {
  component: {
    rating: {
      icon: {
        borderColor: {
          value: "{semantic.color.rating.border}",
        },

        size: {
          large: {
            height: {
              value: "{primitive.scale.space.250}",
            },

            width: {
              value: "{primitive.scale.space.250}",
            },
          },

          small: {
            height: {
              value: "{primitive.scale.space.150}",
            },

            width: {
              value: "{primitive.scale.space.150}",
            },
          },
        },

        variant: {
          empty: {
            backgroundColor: {
              value: "{primitive.color.transparentLight.0}",
            },

            size: {
              large: {
                borderWidth: {
                  value: "1.25px",
                },
              },

              small: {
                borderWidth: {
                  value: "0.75px",
                },
              },
            },
          },

          filled: {
            backgroundColor: {
              value: "{semantic.color.rating.fill}",
            },

            size: {
              large: {
                borderWidth: {
                  value: "1.75px",
                },
              },

              small: {
                borderWidth: {
                  value: "1.2px",
                },
              },
            },
          },

          halfFilled: {
            empty: {
              backgroundColor: {
                value: "{primitive.color.transparentLight.0}",
              },
            },

            fill: {
              backgroundColor: {
                value: "{semantic.color.rating.fill}",
              },

              stroke: {
                value: "{primitive.color.transparentLight.0}",
              },
            },

            size: {
              large: {
                borderWidth: {
                  value: "1.75px",
                },
              },

              small: {
                borderWidth: {
                  value: "1.2px",
                },
              },
            },
          },
        },
      },
    },
  },
};
