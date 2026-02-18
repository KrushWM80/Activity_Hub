import * as _ from "lodash";

const toPascalCase = (value: string | undefined) => {
  const camelCaseValue = _.camelCase(value);

  return camelCaseValue[0].toUpperCase() + camelCaseValue.slice(1);
};

export default toPascalCase;
