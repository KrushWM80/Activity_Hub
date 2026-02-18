// @ts-ignore
// eslint-disable-next-line import/no-unresolved
import {usePluginData} from '@docusaurus/useGlobalData';

const pluginName = 'component-docs-plugin';

export interface ComponentDocsPluginData {
  docs: {[key in string]: PageDoc};
}

export interface PageDoc {
  tags: Tags;
  filePath: string;
  description: string;
  displayName: string;
  methods: any[];
  props: Props;
}

export interface Tags {}

export interface Props {
  defaultValue: Value;
  description: string;
  name: string;
  declarations: Declaration[];
  required: boolean;
  type: VariantType;
}

export interface Declaration {
  fileName: string;
  name: string;
}

export interface Value {
  value: string;
}

export interface VariantType {
  name: string;
  raw: string;
  value: Value[];
}

function useDoc(withPath: string) {
  const pluginData = usePluginData(pluginName) as ComponentDocsPluginData;
  return pluginData?.docs?.[withPath];
}

export default useDoc;
