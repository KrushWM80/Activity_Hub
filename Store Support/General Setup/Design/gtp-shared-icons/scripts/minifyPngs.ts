/* eslint-disable no-console */
/* eslint-env node */
import imagemin from 'imagemin';
import imageminOptipng from 'imagemin-optipng';
import path from 'path';

imagemin([path.resolve(__dirname, '../.tmp/new_pngs/*.png')], {
  destination: path.resolve(__dirname, '../assets/images/icons'),
  plugins: [
    imageminOptipng({
      optimizationLevel: 5,
    }),
  ],
})
  .then(
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    (files) => console.log('PNGs minification complete'),
    // console.log(
    //   `PNGs minified: ${files
    //     .reduce((memo, {destinationPath: p}) => memo.concat(p), [])
    //     .join('\n')} `,
    // ),
  )
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
