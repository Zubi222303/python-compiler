# import tkinter as tk
# from tkinter import ttk, scrolledtext, filedialog, messagebox
# from lexer import tokenize, Token
# from parser import Parser, ParseTreeNode
# from semantic import SemanticAnalyzer
# from tac import ThreeAddressCodeGenerator
# from target import TargetCodeGenerator

# class CompilerGUI:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("HindiPython Compiler")
#         self.root.geometry("1200x800")
#         self.create_widgets()
    
#     def create_widgets(self):
#         # Create main frames
#         self.create_source_frame()
#         self.create_button_frame()
#         self.create_notebook()
    
#     def create_source_frame(self):
#         # Source code frame
#         self.source_frame = ttk.LabelFrame(self.root, text="Source Code", padding=10)
#         self.source_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
#         self.source_text = scrolledtext.ScrolledText(
#             self.source_frame, wrap=tk.WORD, width=80, height=15, 
#             font=('Consolas', 11))
#         self.source_text.pack(fill=tk.BOTH, expand=True)
        
#         # Add sample code
#         self.source_text.insert(tk.END, """# Sample HindiPython Code
# Rakho Ginti x = 10;
# Rakho Ginti y = 20;
# Rakho Ginti z = x + y;

# Dikhao z;

# Kaam jod(Ginti a, Ginti b) Wapis Ginti {
#     Rakho Ginti hasil = a + b;
#     Wapis hasil;
# }

# Dikhao jod(5, 7);""")
    
#     def create_button_frame(self):
#         # Button frame
#         self.button_frame = ttk.Frame(self.root)
#         self.button_frame.pack(fill=tk.X, padx=10, pady=5)
        
#         # Create buttons
#         buttons = [
#             ("Load File", self.load_file),
#             ("Tokenize", self.tokenize),
#             ("Parse", self.parse),
#             ("Semantic", self.semantic_analysis),
#             ("Generate TAC", self.generate_tac),
#             ("Generate Target", self.generate_target),
#             ("Run", self.run_code)
#         ]
        
#         for text, command in buttons:
#             btn = ttk.Button(self.button_frame, text=text, command=command)
#             btn.pack(side=tk.LEFT, padx=5)
    
#     def create_notebook(self):
#         # Notebook for different views
#         self.notebook = ttk.Notebook(self.root)
#         self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
#         # Create tabs
#         tabs = [
#             ("Tokens", self.create_tokens_tab),
#             ("Parse Tree", self.create_parse_tree_tab),
#             ("AST", self.create_ast_tab),
#             ("Semantic", self.create_semantic_tab),
#             ("Three Address Code", self.create_tac_tab),
#             ("Target Code", self.create_target_tab),
#             ("Errors", self.create_errors_tab)
#         ]
        
#         for name, creator in tabs:
#             tab = ttk.Frame(self.notebook)
#             self.notebook.add(tab, text=name)
#             creator(tab)
    
#     def create_tokens_tab(self, parent):
#         self.tokens_text = scrolledtext.ScrolledText(
#             parent, wrap=tk.WORD, font=('Consolas', 10))
#         self.tokens_text.pack(fill=tk.BOTH, expand=True)
    
#     def create_parse_tree_tab(self, parent):
#         self.parse_tree_text = scrolledtext.ScrolledText(
#             parent, wrap=tk.WORD, font=('Consolas', 10))
#         self.parse_tree_text.pack(fill=tk.BOTH, expand=True)
    
#     def create_ast_tab(self, parent):
#         self.ast_text = scrolledtext.ScrolledText(
#             parent, wrap=tk.WORD, font=('Consolas', 10))
#         self.ast_text.pack(fill=tk.BOTH, expand=True)
    
#     def create_semantic_tab(self, parent):
#         self.semantic_text = scrolledtext.ScrolledText(
#             parent, wrap=tk.WORD, font=('Consolas', 10))
#         self.semantic_text.pack(fill=tk.BOTH, expand=True)
    
#     def create_tac_tab(self, parent):
#         self.tac_text = scrolledtext.ScrolledText(
#             parent, wrap=tk.WORD, font=('Consolas', 10))
#         self.tac_text.pack(fill=tk.BOTH, expand=True)
    
#     def create_target_tab(self, parent):
#         self.target_text = scrolledtext.ScrolledText(
#             parent, wrap=tk.WORD, font=('Consolas', 10))
#         self.target_text.pack(fill=tk.BOTH, expand=True)
    
#     def create_errors_tab(self, parent):
#         self.errors_text = scrolledtext.ScrolledText(
#             parent, wrap=tk.WORD, font=('Consolas', 10), foreground='red')
#         self.errors_text.pack(fill=tk.BOTH, expand=True)
    
#     def load_file(self):
#         file_path = filedialog.askopenfilename(
#             filetypes=[("HindiPython Files", "*.hp"), ("All Files", "*.*")])
#         if file_path:
#             with open(file_path, 'r', encoding='utf-8') as file:
#                 self.source_text.delete(1.0, tk.END)
#                 self.source_text.insert(tk.END, file.read())
    
#     def clear_outputs(self):
#         for widget in [self.tokens_text, self.parse_tree_text, 
#                       self.ast_text, self.semantic_text,
#                       self.tac_text, self.target_text,
#                       self.errors_text]:
#             widget.delete(1.0, tk.END)
    
#     def tokenize(self):
#         self.clear_outputs()
#         try:
#             source_code = self.source_text.get(1.0, tk.END)
#             tokens = tokenize(source_code)
#             self.tokens_text.insert(tk.END, "\n".join(str(t) for t in tokens))
#             messagebox.showinfo("Success", "Tokenization completed successfully!")
#         except Exception as e:
#             self.errors_text.insert(tk.END, f"Tokenization error: {str(e)}")
#             messagebox.showerror("Error", "Tokenization failed!")
    
#     def parse(self):
#         try:
#             source_code = self.source_text.get(1.0, tk.END)
#             tokens = tokenize(source_code)
#             parser = Parser(tokens)
#             parse_tree, ast = parser.parse()
            
#             self.parse_tree_text.insert(tk.END, str(parse_tree))
#             self.ast_text.insert(tk.END, str(ast))
            
#             if parser.errors:
#                 self.errors_text.insert(tk.END, "\n".join(
#                     f"Line {e['line']}, Column {e['column']}: {e['message']}"
#                     for e in parser.errors
#                 ))
#                 messagebox.showwarning("Warning", "Parsing completed with errors!")
#             else:
#                 messagebox.showinfo("Success", "Parsing completed successfully!")
#         except Exception as e:
#             self.errors_text.insert(tk.END, f"Parsing error: {str(e)}")
#             messagebox.showerror("Error", "Parsing failed!")
    
#     def semantic_analysis(self):
#         try:
#             source_code = self.source_text.get(1.0, tk.END)
#             tokens = tokenize(source_code)
#             parser = Parser(tokens)
#             parse_tree, ast = parser.parse()
            
#             if parser.errors:
#                 self.errors_text.insert(tk.END, "\n".join(
#                     f"Line {e['line']}, Column {e['column']}: {e['message']}"
#                     for e in parser.errors
#                 ))
#                 messagebox.showerror("Error", "Cannot perform semantic analysis with syntax errors!")
#                 return
            
#             analyzer = SemanticAnalyzer()
#             errors = analyzer.analyze(ast)
            
#             if errors:
#                 self.errors_text.insert(tk.END, "\n".join(
#                     f"Line {e['line']}, Column {e['column']}: {e['message']}"
#                     for e in errors
#                 ))
#                 messagebox.showwarning("Warning", "Semantic analysis completed with errors!")
#             else:
#                 self.semantic_text.insert(tk.END, "No semantic errors found!")
#                 messagebox.showinfo("Success", "Semantic analysis completed successfully!")
#         except Exception as e:
#             self.errors_text.insert(tk.END, f"Semantic analysis error: {str(e)}")
#             messagebox.showerror("Error", "Semantic analysis failed!")
    
#     def generate_tac(self):
#         try:
#             source_code = self.source_text.get(1.0, tk.END)
#             tokens = tokenize(source_code)
#             parser = Parser(tokens)
#             parse_tree, ast = parser.parse()
            
#             if parser.errors:
#                 self.errors_text.insert(tk.END, "\n".join(
#                     f"Line {e['line']}, Column {e['column']}: {e['message']}"
#                     for e in parser.errors
#                 ))
#                 messagebox.showerror("Error", "Cannot generate TAC with syntax errors!")
#                 return
            
#             analyzer = SemanticAnalyzer()
#             errors = analyzer.analyze(ast)
            
#             if errors:
#                 self.errors_text.insert(tk.END, "\n".join(
#                     f"Line {e['line']}, Column {e['column']}: {e['message']}"
#                     for e in errors
#                 ))
#                 messagebox.showerror("Error", "Cannot generate TAC with semantic errors!")
#                 return
            
#             tac_gen = ThreeAddressCodeGenerator()
#             tac = tac_gen.generate(ast)
            
#             self.tac_text.delete(1.0, tk.END)
#             self.tac_text.insert(tk.END, "\n".join(tac))
#             messagebox.showinfo("Success", "Three Address Code generated successfully!")
#         except Exception as e:
#             self.errors_text.insert(tk.END, f"TAC generation error: {str(e)}")
#             messagebox.showerror("Error", "TAC generation failed!")
    
#     def generate_target(self):
#         try:
#             tac = self.tac_text.get(1.0, tk.END)
#             if not tac.strip():
#                 messagebox.showwarning("Warning", "Generate TAC first!")
#                 return
                
#             target_gen = TargetCodeGenerator()
#             target_code = target_gen.generate(tac)
            
#             self.target_text.delete(1.0, tk.END)
#             self.target_text.insert(tk.END, target_code)
#             messagebox.showinfo("Success", "Target code generated successfully!")
#         except Exception as e:
#             self.errors_text.insert(tk.END, f"Target code generation error: {str(e)}")
#             messagebox.showerror("Error", "Target code generation failed!")
    
#     def run_code(self):
#         messagebox.showinfo("Info", "Execution feature coming soon!")
#         # TODO: Implement code execution

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = CompilerGUI(root)
#     root.mainloop()


import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from lexer import tokenize
from parser import Parser
from semantic import SemanticAnalyzer
from tac import ThreeAddressCodeGenerator
from target import TargetCodeGenerator
from executor import Executor
from translator import PythonTranslator

class CompilerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("HindiPython Compiler")
        self.root.geometry("1200x800")
        self.create_widgets()
    
    def create_widgets(self):
        # Source Code Frame
        self.source_frame = ttk.LabelFrame(self.root, text="Source Code", padding=10)
        self.source_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.source_text = scrolledtext.ScrolledText(
            self.source_frame, wrap=tk.WORD, width=80, height=15, 
            font=('Consolas', 11))
        self.source_text.pack(fill=tk.BOTH, expand=True)
        
        # Button Frame
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        buttons = [
            ("Load", self.load_file),
            ("Tokenize", self.tokenize),
            ("Parse", self.parse),
            ("Semantic", self.semantic_analysis),
            ("Generate TAC", self.generate_tac),
            ("Generate Target", self.generate_target),
            ("Execute", self.execute_code)
        ]
        
        for text, cmd in buttons:
            ttk.Button(self.button_frame, text=text, command=cmd).pack(side=tk.LEFT, padx=2)
        
        # Notebook with Tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create Tabs
        self.create_tab("Tokens")
        self.create_tab("Parse Tree") 
        self.create_tab("AST")
        self.create_tab("Semantic")
        self.create_tab("Three Address Code")
        self.create_tab("Target Code")
        self.create_tab("Execution")
        self.create_tab("Errors", foreground='red')
        
        # Load sample code
        self.source_text.insert(tk.END, """Rakho Ginti x = 10;
Rakho Ginti y = 20;
Rakho Ginti z = x + y;
Dikhao z;""")
    
    def create_tab(self, name, **kwargs):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=name)
        
        text_widget = scrolledtext.ScrolledText(
            tab, wrap=tk.WORD, font=('Consolas', 10), **kwargs)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        # Store reference to the text widget
        setattr(self, f"{name.lower().replace(' ', '_')}_text", text_widget)
    
    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("HindiPython", "*.hp")])
        if file_path:
            with open(file_path, 'r') as f:
                self.source_text.delete(1.0, tk.END)
                self.source_text.insert(tk.END, f.read())
    
    def clear_outputs(self):
        for widget in [self.tokens_text, self.parse_tree_text, 
                      self.ast_text, self.semantic_text,
                      self.three_address_code_text, self.target_code_text,
                      self.execution_text, self.errors_text]:
            widget.delete(1.0, tk.END)
    
    def tokenize(self):
        self.clear_outputs()
        try:
            code = self.source_text.get(1.0, tk.END)
            tokens = tokenize(code)
            self.tokens_text.insert(tk.END, "\n".join(str(t) for t in tokens))
            messagebox.showinfo("Success", "Tokenization completed!")
        except Exception as e:
            self.show_error(f"Tokenization error: {str(e)}")
    
    def parse(self):
        try:
            code = self.source_text.get(1.0, tk.END)
            tokens = tokenize(code)
            parser = Parser(tokens)
            parse_tree, ast = parser.parse()
            
            self.parse_tree_text.insert(tk.END, str(parse_tree))
            self.ast_text.insert(tk.END, str(ast))
            
            if parser.errors:
                self.show_errors(parser.errors)
                messagebox.showwarning("Warning", "Parsing completed with errors")
            else:
                messagebox.showinfo("Success", "Parsing completed successfully")
        except Exception as e:
            self.show_error(f"Parsing error: {str(e)}")
    
    def semantic_analysis(self):
        try:
            code = self.source_text.get(1.0, tk.END)
            tokens = tokenize(code)
            parser = Parser(tokens)
            parse_tree, ast = parser.parse()
            
            if parser.errors:
                self.show_errors(parser.errors)
                messagebox.showerror("Error", "Cannot analyze with syntax errors")
                return
            
            analyzer = SemanticAnalyzer()
            errors = analyzer.analyze(ast)
            
            if errors:
                self.show_errors(errors)
                messagebox.showwarning("Warning", "Semantic analysis completed with errors")
            else:
                self.semantic_text.insert(tk.END, "No semantic errors found")
                messagebox.showinfo("Success", "Semantic analysis passed")
        except Exception as e:
            self.show_error(f"Semantic error: {str(e)}")
    
    def generate_tac(self):
        try:
            code = self.source_text.get(1.0, tk.END)
            tokens = tokenize(code)
            parser = Parser(tokens)
            parse_tree, ast = parser.parse()
            
            if parser.errors:
                self.show_errors(parser.errors)
                return
            
            analyzer = SemanticAnalyzer()
            if analyzer.analyze(ast):
                self.show_errors(analyzer.errors)
                return
            
            tac_gen = ThreeAddressCodeGenerator()
            tac = tac_gen.generate(ast)
            self.three_address_code_text.insert(tk.END, "\n".join(tac))
            messagebox.showinfo("Success", "TAC generation completed")
        except Exception as e:
            self.show_error(f"TAC generation error: {str(e)}")
    
    def generate_target(self):
        try:
            tac = self.three_address_code_text.get(1.0, tk.END)
            if not tac.strip():
                messagebox.showwarning("Warning", "Generate TAC first")
                return
            
            target_gen = TargetCodeGenerator()
            target = target_gen.generate(tac)
            self.target_code_text.insert(tk.END, target)
            messagebox.showinfo("Success", "Target code generated")
        except Exception as e:
            self.show_error(f"Target generation error: {str(e)}")
    
    def execute_code(self):
        try:
            executor = Executor()
            
            # Try executing TAC first
            tac = self.three_address_code_text.get(1.0, tk.END)
            if tac.strip():
                output = executor.execute_tac(tac)
                self.execution_text.insert(tk.END, "=== TAC Execution ===\n" + output + "\n")
            
            # Try executing target code
            target = self.target_code_text.get(1.0, tk.END)
            if target.strip():
                # Alternative: Use Python translation
                py_code = PythonTranslator.tac_to_python(tac)
                self.execution_text.insert(tk.END, "\n=== Python Translation ===\n" + py_code + "\n")
                
                # Execute the translated Python
                loc = {}
                try:
                    exec(py_code, {}, loc)
                    self.execution_text.insert(tk.END, "\n=== Execution Output ===\n" + loc.get('result', 'No output'))
                except Exception as e:
                    self.execution_text.insert(tk.END, f"\n=== Execution Error ===\n{str(e)}")
            
            messagebox.showinfo("Success", "Execution completed")
        except Exception as e:
            self.show_error(f"Execution error: {str(e)}")
    
    def show_error(self, message):
        self.errors_text.insert(tk.END, message + "\n")
        messagebox.showerror("Error", message)
    
    def show_errors(self, errors):
        for error in errors:
            self.errors_text.insert(tk.END, 
                f"Line {error['line']}, Column {error['column']}: {error['message']}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = CompilerGUI(root)
    root.mainloop()