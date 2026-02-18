/* eslint-disable @typescript-eslint/no-require-imports */

const rule = require("../../rules/double-newline-between-properties");
const { RuleTester } = require("eslint");
const ruleTester = new RuleTester();

ruleTester.run("double-newline-between-properties", rule, {
  valid: [
    {
      code: `console.log({
        "bar": {
          "baz": {
            "abc": true,
          },

          "buz": {
            "def": true,
          },

          "biz": {
            "ghi": true,
          },
        }
      });`,
    },
    {
      code: `console.log({
        "bar": {
          "baz": false,
          "buz": true, 
          "biz": {
            "ghi": true,
          },
        }
      });`,
    },
    {
      code: `console.log({
        "bar": {
          "baz": {"abc": false},
          "buz": {"def": true}, 
          "biz": { "ghi": true },
        }
      });`,
    },
  ],
  invalid: [
    {
      code: `console.log({
        "bar": {
          "baz": {
            "abc": true,
          },
          "buz": {
            "def": true,
          }
        }
      });`,
      errors: [
        {
          message:
            "Expected double newlines between object properties when the next property is an object, found 1.",
        },
      ],
      output: `console.log({
        "bar": {
          "baz": {
            "abc": true,
          },

          "buz": {
            "def": true,
          }
        }
      });`,
    },
    {
      code: `console.log({
        "bar": {
          "baz": {
            "abc": true,
          },"buz": {
            "def": true,
          }
        }
      });`,
      errors: [
        {
          message:
            "Expected double newlines between object properties when the next property is an object, found 0.",
        },
      ],
      output: `console.log({
        "bar": {
          "baz": {
            "abc": true,
          },

          "buz": {
            "def": true,
          }
        }
      });`,
    },
    {
      code: `console.log({
        "bar": {
          "baz": {
            "abc": true,
          },


          "buz": {
            "def": true,
          }
        }
      });`,
      errors: [
        {
          message:
            "Expected double newlines between object properties when the next property is an object, found 3.",
        },
      ],
      output: `console.log({
        "bar": {
          "baz": {
            "abc": true,
          },

          "buz": {
            "def": true,
          }
        }
      });`,
    },
  ],
});
