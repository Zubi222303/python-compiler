from lexer import tokenize
from parser import Parser
from semantic import SemanticAnalyzer
from interme_code import IntermediateCodeGenerator
import tkinter as tk
from guie import CompilerGUI

def test_compiler(source_code):
    try:
        # Tokenization
        tokens = tokenize(source_code)
        print("Tokens generated successfully:")
        for token in tokens:
            print(f"{token.type}: {token.value} (Line {token.line}, Column {token.column})")
        
        # Parsing
        parser = Parser(tokens)
        parse_tree, ast = parser.parse()
        
        print("\nParse Tree:")
        print(parse_tree)
        
        print("\nAbstract Syntax Tree:")
        print(ast)
        
        # Print any errors
        if parser.errors:
            print("\nParser errors found:")
            for error in parser.errors:
                print(f"Line {error['line']}, Column {error['column']}: {error['message']}")
            return False
        
        # Semantic Analysis
        analyzer = SemanticAnalyzer()
        semantic_errors = analyzer.analyze(ast)
        
        if semantic_errors:
            print("\nSemantic errors found:")
            for error in semantic_errors:
                print(f"Line {error['line']}, Column {error['column']}: {error['message']}")
            return False
        
        # Intermediate Code Generation
        codegen = IntermediateCodeGenerator()
        intermediate_code = codegen.generate(ast)
        print("\nIntermediate Code:")
        print("\n".join(intermediate_code))
        
        return True
        
    except Exception as e:
        print(f"\nCompilation failed: {str(e)}")
        return False

if __name__ == "__main__":
    # Test with sample code
    test_code = """
    Rakho Ginti x = 10;
    Dikhao x;
    """
    
    print("Testing compiler with sample code...")
    success = test_compiler(test_code)
    
    if success:
        print("\nAll compilation stages completed successfully!")
    else:
        print("\nCompilation completed with errors.")
    
    # Then start the GUI
    root = tk.Tk()
    app = CompilerGUI(root)
    root.mainloop()