import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from lexer import tokenize
from parser import Parser
from semantic import SemanticAnalyzer
from tac import ThreeAddressCodeGenerator
from interme_code import IntermediateCodeGenerator
from target import TargetCodeGenerator
from executor import Executor
from translator import PythonTranslator
from optimizer import Optimizer
from output import generate_output_from_ast  # ✅ New import

class CompilerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("HindiPython Compiler")
        self.root.geometry("1200x800")
        self.create_widgets()

    def create_widgets(self):
        self.source_frame = ttk.LabelFrame(self.root, text="Source Code", padding=10)
        self.source_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.source_text = scrolledtext.ScrolledText(
            self.source_frame, wrap=tk.WORD, width=80, height=15,
            font=('Consolas', 11))
        self.source_text.pack(fill=tk.BOTH, expand=True)

        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(fill=tk.X, padx=10, pady=5)

        buttons = [
            ("Load", self.load_file),
            ("Tokenize", self.tokenize),
            ("Parse", self.parse),
            ("Semantic", self.semantic_analysis),
            ("Generate Intermediate", self.generate_intermediate),
            ("Generate TAC", self.generate_tac),
            ("Optimize TAC", self.optimize_code),
            ("Generate Target", self.generate_target),
            ("Generate Output", self.generate_source_output),  # ✅ New button
            ("Execute", self.execute_code)
        ]

        for text, cmd in buttons:
            ttk.Button(self.button_frame, text=text, command=cmd).pack(side=tk.LEFT, padx=2)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Tabs
        self.create_tab("Tokens")
        self.create_tab("Parse Tree")
        self.create_tab("AST")
        self.create_tab("Semantic")
        self.create_tab("Intermediate Code")
        self.create_tab("Three Address Code")
        self.create_tab("Optimized Code")
        self.create_tab("Target Code")
        self.create_tab("Execution")
        self.create_tab("Output")  # ✅ New Output Tab
        self.create_tab("Symbol Table")
        self.create_tab("Errors", foreground='red')

        # Default code
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

        setattr(self, f"{name.lower().replace(' ', '_')}_text", text_widget)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("HindiPython", "*.hp")])
        if file_path:
            with open(file_path, 'r') as f:
                self.source_text.delete(1.0, tk.END)
                self.source_text.insert(tk.END, f.read())

    def clear_outputs(self):
        for attr in [
            'tokens_text', 'parse_tree_text', 'ast_text', 'semantic_text',
            'intermediate_code_text', 'three_address_code_text', 'optimized_code_text',
            'target_code_text', 'execution_text', 'symbol_table_text', 'errors_text',
            'output_text'  # ✅ clear Output tab
        ]:
            getattr(self, attr).delete(1.0, tk.END)

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
            self.parse_tree, self.ast = parser.parse()

            self.parse_tree_text.insert(tk.END, str(self.parse_tree))
            self.ast_text.insert(tk.END, str(self.ast))

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
            self.parse_tree, self.ast = parser.parse()

            if parser.errors:
                self.show_errors(parser.errors)
                messagebox.showerror("Error", "Cannot analyze with syntax errors")
                return

            self.analyzer = SemanticAnalyzer()
            errors = self.analyzer.analyze(self.ast)

            if errors:
                self.show_errors(errors)
                messagebox.showwarning("Warning", "Semantic analysis completed with errors")
            else:
                self.semantic_text.insert(tk.END, "No semantic errors found")
                symbol_table_output = self.display_symbol_table(self.analyzer.root_scope)
                self.symbol_table_text.insert(tk.END, "\n".join(symbol_table_output))
                messagebox.showinfo("Success", "Semantic analysis passed")
        except Exception as e:
            self.show_error(f"Semantic error: {str(e)}")

    def display_symbol_table(self, symbol_table, indent=0):
        lines = []
        prefix = "  " * indent
        for name, entry in symbol_table.symbols.items():
            if entry['is_function']:
                params = ", ".join([f"{ptype} {pname}" for ptype, pname in entry['params']])
                lines.append(f"{prefix}Function: {name}({params}) -> {entry['return_type']}")
            else:
                lines.append(f"{prefix}Variable: {name} : {entry['type']} (Scope Level {entry['scope_level']})")
        for child in symbol_table.children:
            lines.extend(self.display_symbol_table(child, indent + 1))
        return lines

    def generate_intermediate(self):
        try:
            code = self.source_text.get(1.0, tk.END)
            tokens = tokenize(code)
            parser = Parser(tokens)
            _, ast = parser.parse()

            analyzer = SemanticAnalyzer()
            if analyzer.analyze(ast):
                self.show_errors(analyzer.errors)
                return

            generator = IntermediateCodeGenerator()
            intermediate = generator.generate(ast)
            self.intermediate_code_text.insert(tk.END, "\n".join(intermediate))
            messagebox.showinfo("Success", "Intermediate code generated")
        except Exception as e:
            self.show_error(f"Intermediate code error: {str(e)}")

    def generate_tac(self):
        try:
            code = self.source_text.get(1.0, tk.END)
            tokens = tokenize(code)
            parser = Parser(tokens)
            _, ast = parser.parse()

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

    def optimize_code(self):
        try:
            tac = self.three_address_code_text.get(1.0, tk.END).strip().splitlines()
            if not tac:
                messagebox.showwarning("Warning", "Please generate TAC first")
                return

            optimizer = Optimizer(tac)
            optimized = optimizer.optimize()

            self.optimized_code_text.delete(1.0, tk.END)
            self.optimized_code_text.insert(tk.END, "\n".join(optimized))
            messagebox.showinfo("Success", "TAC optimized successfully")
        except Exception as e:
            self.show_error(f"Optimization error: {str(e)}")

    def generate_target(self):
        try:
            tac = self.optimized_code_text.get(1.0, tk.END).strip()
            if not tac:
                messagebox.showwarning("Warning", "Please optimize TAC first")
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
            tac = self.optimized_code_text.get(1.0, tk.END)
            if tac.strip():
                output = executor.execute_tac(tac)
                self.execution_text.insert(tk.END, "=== TAC Execution ===\n" + output + "\n")

            target = self.target_code_text.get(1.0, tk.END)
            if target.strip():
                py_code = PythonTranslator.tac_to_python(tac)
                self.execution_text.insert(tk.END, "\n=== Python Translation ===\n" + py_code + "\n")
                loc = {}
                try:
                    exec(py_code, {}, loc)
                    self.execution_text.insert(tk.END, "\n=== Execution Output ===\n" + loc.get('result', 'No output'))
                except Exception as e:
                    self.execution_text.insert(tk.END, f"\n=== Execution Error ===\n{str(e)}")

            messagebox.showinfo("Success", "Execution completed")
        except Exception as e:
            self.show_error(f"Execution error: {str(e)}")

    def generate_source_output(self):
        try:
            code = self.source_text.get(1.0, tk.END)
            tokens = tokenize(code)
            parser = Parser(tokens)
            _, ast = parser.parse()

            output = generate_output_from_ast(ast)
            self.output_text.insert(tk.END, output or "No output")
            messagebox.showinfo("Success", "Source output generated")
        except Exception as e:
            self.show_error(f"Output generation error: {str(e)}")

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
