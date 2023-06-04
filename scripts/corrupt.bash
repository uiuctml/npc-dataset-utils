#!/usr/bin/env bash

cd ../src

./corrupt.py gaussian_noise 1;
./corrupt.py gaussian_noise 2;
./corrupt.py gaussian_noise 3;
./corrupt.py gaussian_noise 4;
./corrupt.py gaussian_noise 5;

./corrupt.py shot_noise 1;
./corrupt.py shot_noise 2;
./corrupt.py shot_noise 3;
./corrupt.py shot_noise 4;
./corrupt.py shot_noise 5;

./corrupt.py impulse_noise 1;
./corrupt.py impulse_noise 2;
./corrupt.py impulse_noise 3;
./corrupt.py impulse_noise 4;
./corrupt.py impulse_noise 5;

./corrupt.py defocus_blur 1;
./corrupt.py defocus_blur 2;
./corrupt.py defocus_blur 3;
./corrupt.py defocus_blur 4;
./corrupt.py defocus_blur 5;

./corrupt.py glass_blur 1;
./corrupt.py glass_blur 2;
./corrupt.py glass_blur 3;
./corrupt.py glass_blur 4;
./corrupt.py glass_blur 5;

./corrupt.py motion_blur 1;
./corrupt.py motion_blur 2;
./corrupt.py motion_blur 3;
./corrupt.py motion_blur 4;
./corrupt.py motion_blur 5;

./corrupt.py zoom_blur 1;
./corrupt.py zoom_blur 2;
./corrupt.py zoom_blur 3;
./corrupt.py zoom_blur 4;
./corrupt.py zoom_blur 5;

./corrupt.py snow 1;
./corrupt.py snow 2;
./corrupt.py snow 3;
./corrupt.py snow 4;
./corrupt.py snow 5;

./corrupt.py frost 1;
./corrupt.py frost 2;
./corrupt.py frost 3;
./corrupt.py frost 4;
./corrupt.py frost 5;

./corrupt.py fog 1;
./corrupt.py fog 2;
./corrupt.py fog 3;
./corrupt.py fog 4;
./corrupt.py fog 5;

./corrupt.py brightness 1;
./corrupt.py brightness 2;
./corrupt.py brightness 3;
./corrupt.py brightness 4;
./corrupt.py brightness 5;

./corrupt.py contrast 1;
./corrupt.py contrast 2;
./corrupt.py contrast 3;
./corrupt.py contrast 4;
./corrupt.py contrast 5;

./corrupt.py elastic_transform 1;
./corrupt.py elastic_transform 2;
./corrupt.py elastic_transform 3;
./corrupt.py elastic_transform 4;
./corrupt.py elastic_transform 5;

./corrupt.py pixelate 1;
./corrupt.py pixelate 2;
./corrupt.py pixelate 3;
./corrupt.py pixelate 4;
./corrupt.py pixelate 5;

./corrupt.py jpeg_compression 1;
./corrupt.py jpeg_compression 2;
./corrupt.py jpeg_compression 3;
./corrupt.py jpeg_compression 4;
./corrupt.py jpeg_compression 5;

./corrupt.py speckle_noise 1;
./corrupt.py speckle_noise 2;
./corrupt.py speckle_noise 3;
./corrupt.py speckle_noise 4;
./corrupt.py speckle_noise 5;

./corrupt.py gaussian_blur 1;
./corrupt.py gaussian_blur 2;
./corrupt.py gaussian_blur 3;
./corrupt.py gaussian_blur 4;
./corrupt.py gaussian_blur 5;

./corrupt.py spatter 1;
./corrupt.py spatter 2;
./corrupt.py spatter 3;
./corrupt.py spatter 4;
./corrupt.py spatter 5;

./corrupt.py saturate 1;
./corrupt.py saturate 2;
./corrupt.py saturate 3;
./corrupt.py saturate 4;
./corrupt.py saturate 5;
