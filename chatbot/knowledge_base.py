"""
Knowledge base for the Gaussian filter chatbot.
Contains information about the codebase, concepts, and functionality.
"""

KNOWLEDGE_BASE = {
    "project": {
        "name": "Gaussian Filter",
        "description": "A simple C++ application that applies a Gaussian blur filter to images using OpenCV.",
        "repository": "ashandrin/test_cpp",
        "files": ["gaussian_filter.cpp", "Makefile"]
    },
    
    "code_structure": {
        "gaussian_filter.cpp": "Main source file containing the Gaussian kernel generation function and main application logic.",
        "Makefile": "Build configuration that compiles the application using g++ and links against OpenCV."
    },
    
    "functions": {
        "createGaussianKernel": {
            "purpose": "Creates a 2D Gaussian kernel for image blurring",
            "parameters": [
                {"name": "rows", "type": "int", "description": "Number of rows in the kernel"},
                {"name": "cols", "type": "int", "description": "Number of columns in the kernel"},
                {"name": "sigmaX", "type": "double", "description": "Standard deviation in X direction"},
                {"name": "sigmaY", "type": "double", "description": "Standard deviation in Y direction"}
            ],
            "return": {"type": "cv::Mat", "description": "Normalized Gaussian kernel"},
            "algorithm": "Creates a matrix of values representing a 2D Gaussian distribution. Each position (x,y) is calculated using the formula: exp(-(x^2/(2*sigmaX^2) + y^2/(2*sigmaY^2))). The kernel is then normalized so all values sum to 1."
        },
        "main": {
            "purpose": "Entry point that processes an image with the Gaussian filter",
            "parameters": [
                {"name": "argc", "type": "int", "description": "Number of command-line arguments"},
                {"name": "argv", "type": "char**", "description": "Array of command-line arguments"}
            ],
            "return": {"type": "int", "description": "Exit code (0 for success, -1 for error)"},
            "algorithm": "Parses command-line arguments, loads an input image, creates a Gaussian kernel, applies it to the image using OpenCV's filter2D function, and saves the result."
        }
    },
    
    "concepts": {
        "gaussian_filter": "A filter that uses a Gaussian function to blur an image. It reduces noise and detail by applying a weighted average where nearby pixels have more influence than distant ones.",
        "kernel": "A small matrix used in convolution operations. For image processing, a kernel is applied to each pixel and its neighborhood to produce a new value.",
        "sigma": "Controls the 'spread' of the Gaussian distribution. Larger sigma values create a wider bell curve, resulting in more blurring.",
        "convolution": "A mathematical operation that combines the kernel with the image. It multiplies each kernel value with the corresponding pixel value in the neighborhood, then sums these products.",
        "filter2D": "An OpenCV function that applies a convolution operation using a specified kernel.",
        "normalization": "Process of adjusting values to ensure they sum to 1, maintaining image brightness after filtering."
    },
    
    "usage": {
        "compilation": "Run 'make' in the repository directory to compile the application.",
        "execution": "Run './gaussian_filter [input_path] [output_path]' to process an image.",
        "command_line_args": [
            {"name": "input_path", "description": "Path to the input image (optional, defaults to hardcoded path)"},
            {"name": "output_path", "description": "Path for the output image (optional, defaults to 'output.jpg' in the current directory)"}
        ],
        "examples": [
            {"command": "./gaussian_filter", "description": "Process the default image"},
            {"command": "./gaussian_filter input.jpg", "description": "Process input.jpg with default output path"},
            {"command": "./gaussian_filter input.jpg blurred.jpg", "description": "Process input.jpg and save as blurred.jpg"}
        ]
    },
    
    "dependencies": {
        "opencv": {
            "name": "OpenCV",
            "description": "Open Source Computer Vision Library, used for image processing operations",
            "version": "4.x (as specified in the Makefile)",
            "components_used": [
                {"name": "imread", "purpose": "Read image files"},
                {"name": "imwrite", "purpose": "Write image files"},
                {"name": "filter2D", "purpose": "Apply convolution filter"}
            ]
        }
    }
}

DETAILED_EXPLANATIONS = {
    "gaussian_kernel_algorithm": """
The createGaussianKernel function generates a 2D Gaussian kernel using these steps:
1. Create an empty matrix of the specified dimensions
2. Calculate the center point of the kernel
3. For each position (i,j) in the kernel:
   a. Calculate the distance from the center (x,y)
   b. Apply the 2D Gaussian formula: exp(-(x^2/(2*σ_x^2) + y^2/(2*σ_y^2)))
   c. Store the result in the kernel
4. Sum all values in the kernel
5. Normalize the kernel by dividing all values by the sum
6. Return the normalized kernel

This creates a bell-shaped distribution where the center has the highest value and 
values decrease as you move away from the center.
    """,
    
    "image_processing_pipeline": """
The main function implements this image processing pipeline:
1. Parse command-line arguments to get input and output paths
2. Load the input image using OpenCV's imread
3. Check if the image was loaded successfully
4. Create a Gaussian kernel (8x8 with σ=1.5)
5. Convert the kernel to the appropriate format (CV_32F)
6. Apply the kernel to the image using filter2D
7. Save the result to the output path
8. Report success or failure to the user

The filter2D function performs convolution by:
- Centering the kernel on each pixel
- Multiplying each kernel value with the corresponding pixel value
- Summing these products to get the new pixel value
- Repeating for all pixels in the image
    """
}
