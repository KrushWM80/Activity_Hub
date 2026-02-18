export const constructDeprecatedDocBlock = (
  deprecatedComment = "This Living Design token is deprecated.",
) => {
  return `/**
 * @deprecated ${deprecatedComment}
 */
`;
};
