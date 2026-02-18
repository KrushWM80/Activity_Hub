import fs from "fs/promises";
import path from "path";
import globby from "globby";

const jsonFilenames = globby.sync(path.join(__dirname, "../dist/**/*.json"));
const sassFilenames = globby.sync(path.join(__dirname, "../dist/**/*.scss"));

describe("Build formats", () => {
  test.each(sassFilenames)(
    "Sass file should be valid: %s",
    async (filename: string) => {
      expect(await fs.readFile(filename, "utf-8")).not.toMatch(
        "[object Object]",
      );
    },
  );

  test.each(jsonFilenames)(
    "JSON file should be valid: %s",
    async (filename: string) => {
      expect(JSON.parse(await fs.readFile(filename, "utf-8"))).toBeTruthy();
    },
  );
});
