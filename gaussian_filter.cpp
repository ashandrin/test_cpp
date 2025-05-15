#include <opencv2/opencv.hpp>
#include <iostream>
#include <string>
#include <cmath>

cv::Mat createGaussianKernel(int rows, int cols, double sigmaX, double sigmaY) {
    cv::Mat kernel(rows, cols, CV_64F);
    double centerX = cols / 2.0;
    double centerY = rows / 2.0;
    double sum = 0.0;
    
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            double x = j - centerX;
            double y = i - centerY;
            double value = exp(-(x*x/(2*sigmaX*sigmaX) + y*y/(2*sigmaY*sigmaY)));
            kernel.at<double>(i, j) = value;
            sum += value;
        }
    }
    
    kernel /= sum;
    return kernel;
}

int main(int argc, char** argv) {
    std::string inputPath = "/home/ubuntu/attachments/9711dbab-0842-41d0-91a3-3810358b2cc4/input.jpg";
    std::string outputPath = "/home/ubuntu/repos/test_cpp/output.jpg";
    
    if (argc > 1) {
        inputPath = argv[1];
    }
    if (argc > 2) {
        outputPath = argv[2];
    }
    
    cv::Mat inputImage = cv::imread(inputPath, cv::IMREAD_COLOR);
    
    if (inputImage.empty()) {
        std::cerr << "Error: Could not read the image: " << inputPath << std::endl;
        return -1;
    }
    
    cv::Mat outputImage;
    
    double sigma = 1.5; // Adjust sigma as needed for desired blur effect
    cv::Mat gaussianKernel = createGaussianKernel(8, 8, sigma, sigma);
    
    cv::Mat kernel;
    gaussianKernel.convertTo(kernel, CV_32F);
    
    cv::filter2D(inputImage, outputImage, -1, kernel);
    
    bool success = cv::imwrite(outputPath, outputImage);
    if (!success) {
        std::cerr << "Error: Could not write the output image: " << outputPath << std::endl;
        return -1;
    }
    
    std::cout << "Successfully applied 8x8 Gaussian filter to " << inputPath << std::endl;
    std::cout << "Output saved to " << outputPath << std::endl;
    
    return 0;
}
