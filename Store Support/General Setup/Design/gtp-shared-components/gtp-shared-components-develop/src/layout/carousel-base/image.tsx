import * as React from 'react';
import {Image, ImageProps as RNImageProps} from 'react-native';

export type ImageProps = Omit<RNImageProps, 'source'> & {
  source: string;
  size: number;
};

type ImageState = {
  height: number;
  width: number;
};

export default class ProductImage extends React.Component<
  ImageProps,
  ImageState
> {
  state: ImageState = {
    height: this.props.size,
    width: this.props.size,
  };

  componentDidMount() {
    Image.getSize(
      this.props.source,
      (width, height) => {
        if (width >= height) {
          this.setState({
            width: this.props.size,
            height: height * (this.props.size / width),
          });
        } else {
          this.setState({
            width: width * (this.props.size / height),
            height: this.props.size,
          });
        }
      },
      () => {
        this.setState({height: this.props.size, width: this.props.size});
      },
    );
  }

  render() {
    const {source, style} = this.props;
    return <Image source={{uri: source}} style={[style, {...this.state}]} />;
  }
}
