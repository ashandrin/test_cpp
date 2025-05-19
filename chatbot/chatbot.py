#!/usr/bin/env python3
"""
A chatbot that explains the Gaussian filter implementation in the test_cpp repository.
"""

import re
import sys
from knowledge_base import KNOWLEDGE_BASE, DETAILED_EXPLANATIONS

class GaussianFilterChatbot:
    def __init__(self):
        self.knowledge_base = KNOWLEDGE_BASE
        self.detailed_explanations = DETAILED_EXPLANATIONS
        self.greeting_shown = False
        
    def show_greeting(self):
        """Display the initial greeting message."""
        print("="*80)
        print("Gaussian Filter Chatbot")
        print("="*80)
        print("Welcome! I can help you understand the Gaussian filter implementation")
        print("in the test_cpp repository. You can ask me about:")
        print("- The project structure and files")
        print("- How the Gaussian filter works")
        print("- The code implementation details")
        print("- How to compile and use the software")
        print("- Specific concepts like kernels, convolution, etc.")
        print("\nType 'exit', 'quit', or 'bye' to end the conversation.")
        print("Type 'help' to see this message again.")
        print("="*80)
        self.greeting_shown = True
    
    def get_response(self, user_input):
        """Process user input and generate a response."""
        user_input = user_input.lower().strip()
        
        if user_input in ['exit', 'quit', 'bye']:
            return "Goodbye! I hope I helped you understand the Gaussian filter implementation."
        
        if user_input in ['help', '?']:
            self.show_greeting()
            return ""
        
        if re.search(r'what is|about|purpose|project|repository', user_input):
            return self._get_project_info()
        
        if re.search(r'code|structure|files|file|organization', user_input):
            return self._get_code_structure()
        
        if re.search(r'kernel|function|creategaussiankernel|create|gaussian function', user_input):
            return self._get_kernel_function_info()
        
        if re.search(r'main|entry|program flow|execution', user_input):
            return self._get_main_function_info()
        
        if re.search(r'concept|gaussian|blur|sigma|convolution|filter|normalize|normalization', user_input):
            return self._get_concept_info(user_input)
        
        if re.search(r'use|usage|how to|run|compile|build|execute|command|argument', user_input):
            return self._get_usage_info()
        
        if re.search(r'depend|opencv|library|libraries|requirement', user_input):
            return self._get_dependency_info()
        
        if re.search(r'algorithm|detail|explain|how does|pipeline|process', user_input):
            if 'kernel' in user_input or 'gaussian' in user_input:
                return self.detailed_explanations['gaussian_kernel_algorithm']
            if 'pipeline' in user_input or 'process' in user_input or 'image' in user_input:
                return self.detailed_explanations['image_processing_pipeline']
        
        return ("I'm not sure how to answer that. You can ask me about the project, "
                "code structure, Gaussian kernel function, main function, concepts, "
                "usage, or dependencies. Type 'help' for more information.")
    
    def _get_project_info(self):
        """Get information about the project."""
        project = self.knowledge_base['project']
        return (f"Project: {project['name']}\n\n"
                f"Description: {project['description']}\n\n"
                f"Repository: {project['repository']}\n\n"
                f"Main Files: {', '.join(project['files'])}")
    
    def _get_code_structure(self):
        """Get information about the code structure."""
        structure = self.knowledge_base['code_structure']
        result = "Code Structure:\n\n"
        for file, description in structure.items():
            result += f"• {file}: {description}\n"
        return result
    
    def _get_kernel_function_info(self):
        """Get information about the Gaussian kernel function."""
        func = self.knowledge_base['functions']['createGaussianKernel']
        
        result = f"Function: createGaussianKernel\n\n"
        result += f"Purpose: {func['purpose']}\n\n"
        
        result += "Parameters:\n"
        for param in func['parameters']:
            result += f"• {param['name']} ({param['type']}): {param['description']}\n"
        
        result += f"\nReturn: {func['return']['type']} - {func['return']['description']}\n\n"
        result += f"Algorithm: {func['algorithm']}\n\n"
        result += f"For more details, ask about the 'gaussian kernel algorithm'."
        
        return result
    
    def _get_main_function_info(self):
        """Get information about the main function."""
        func = self.knowledge_base['functions']['main']
        
        result = f"Function: main\n\n"
        result += f"Purpose: {func['purpose']}\n\n"
        
        result += "Parameters:\n"
        for param in func['parameters']:
            result += f"• {param['name']} ({param['type']}): {param['description']}\n"
        
        result += f"\nReturn: {func['return']['type']} - {func['return']['description']}\n\n"
        result += f"Algorithm: {func['algorithm']}\n\n"
        result += f"For more details, ask about the 'image processing pipeline'."
        
        return result
    
    def _get_concept_info(self, user_input):
        """Get information about concepts."""
        concepts = self.knowledge_base['concepts']
        
        for concept, description in concepts.items():
            if concept.replace('_', ' ') in user_input:
                return f"{concept.replace('_', ' ').title()}: {description}"
        
        result = "Concepts in Gaussian Image Filtering:\n\n"
        for concept, description in concepts.items():
            result += f"• {concept.replace('_', ' ').title()}: {description}\n\n"
        
        return result
    
    def _get_usage_info(self):
        """Get information about usage."""
        usage = self.knowledge_base['usage']
        
        result = "How to Use the Gaussian Filter:\n\n"
        result += f"Compilation: {usage['compilation']}\n\n"
        result += f"Execution: {usage['execution']}\n\n"
        
        result += "Command-line Arguments:\n"
        for arg in usage['command_line_args']:
            result += f"• {arg['name']}: {arg['description']}\n"
        
        result += "\nExamples:\n"
        for example in usage['examples']:
            result += f"• {example['command']}\n  {example['description']}\n"
        
        return result
    
    def _get_dependency_info(self):
        """Get information about dependencies."""
        deps = self.knowledge_base['dependencies']
        
        result = "Dependencies:\n\n"
        for _, dep in deps.items():
            result += f"{dep['name']}: {dep['description']}\n"
            result += f"Version: {dep['version']}\n\n"
            
            result += "Components Used:\n"
            for comp in dep['components_used']:
                result += f"• {comp['name']}: {comp['purpose']}\n"
        
        return result
    
    def run(self):
        """Run the chatbot in interactive mode."""
        self.show_greeting()
        
        try:
            while True:
                user_input = input("\nYou: ").strip()
                if not user_input:
                    continue
                
                response = self.get_response(user_input)
                if response:
                    print(f"\nChatbot: {response}")
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    break
        except KeyboardInterrupt:
            print("\n\nGoodbye! I hope I helped you understand the Gaussian filter implementation.")
        except Exception as e:
            print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    chatbot = GaussianFilterChatbot()
    chatbot.run()
