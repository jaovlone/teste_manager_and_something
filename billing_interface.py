import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter import filedialog
from database import *
from datetime import datetime
import os
from fpdf import FPDF

class BillingSystem:
    def __init__(self, root, current_user):
        self.root = root
        self.current_user = current_user
        self.root.title("Sistema de Cobrança")
        
        # Variáveis da venda
        self.cart = []
        self.customer_name = ""
        self.customer_doc = ""
        self.payment_method = "Dinheiro"
        
        # Configurar tamanho e centralizar
        self.root.state('zoomed')  # Maximiza a janela
        
        # Criar widgets
        self.create_widgets()
        
        # Carregar produtos disponíveis
        self.load_products()
    
    def create_widgets(self):
        # Frame principal
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame superior (produtos e carrinho)
        top_frame = ttk.Frame(self.main_frame)
        top_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame de produtos disponíveis
        products_frame = ttk.LabelFrame(top_frame, text="Produtos Disponíveis", padding="10")
        products_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview para produtos
        self.products_tree = ttk.Treeview(products_frame, columns=("ID", "Nome", "Preço", "Estoque"), show="headings")
        self.products_tree.heading("ID", text="ID")
        self.products_tree.heading("Nome", text="Nome")
        self.products_tree.heading("Preço", text="Preço (R$)")
        self.products_tree.heading("Estoque", text="Estoque")
        
        self.products_tree.column("ID", width=50, anchor=tk.CENTER)
        self.products_tree.column("Nome", width=150)
        self.products_tree.column("Preço", width=80, anchor=tk.E)
        self.products_tree.column("Estoque", width=80, anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(products_frame, orient=tk.VERTICAL, command=self.products_tree.yview)
        self.products_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.products_tree.pack(fill=tk.BOTH, expand=True)
        
        # Frame do carrinho
        cart_frame = ttk.LabelFrame(top_frame, text="Carrinho de Compras", padding="10")
        cart_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview para carrinho
        self.cart_tree = ttk.Treeview(cart_frame, columns=("ID", "Nome", "Qtd", "Preço", "Total"), show="headings")
        self.cart_tree.heading("ID", text="ID")
        self.cart_tree.heading("Nome", text="Nome")
        self.cart_tree.heading("Qtd", text="Qtd")
        self.cart_tree.heading("Preço", text="Preço (R$)")
        self.cart_tree.heading("Total", text="Total (R$)")
        
        self.cart_tree.column("ID", width=50, anchor=tk.CENTER)
        self.cart_tree.column("Nome", width=150)
        self.cart_tree.column("Qtd", width=60, anchor=tk.CENTER)
        self.cart_tree.column("Preço", width=80, anchor=tk.E)
        self.cart_tree.column("Total", width=80, anchor=tk.E)
        
        # Scrollbar
        cart_scrollbar = ttk.Scrollbar(cart_frame, orient=tk.VERTICAL, command=self.cart_tree.yview)
        self.cart_tree.configure(yscroll=cart_scrollbar.set)
        cart_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.cart_tree.pack(fill=tk.BOTH, expand=True)
        
        # Frame de botões
        buttons_frame = ttk.Frame(top_frame)
        buttons_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5)
        
        self.add_button = ttk.Button(buttons_frame, text="Adicionar →", command=self.add_to_cart)
        self.add_button.pack(pady=5, fill=tk.X)
        
        self.remove_button = ttk.Button(buttons_frame, text="← Remover", command=self.remove_from_cart)
        self.remove_button.pack(pady=5, fill=tk.X)
        
        self.clear_button = ttk.Button(buttons_frame, text="Limpar Carrinho", command=self.clear_cart)
        self.clear_button.pack(pady=5, fill=tk.X)
        
        # Frame inferior (informações da venda)
        bottom_frame = ttk.LabelFrame(self.main_frame, text="Informações da Venda", padding="10")
        bottom_frame.pack(fill=tk.X, pady=5)
        
        # Cliente
        ttk.Label(bottom_frame, text="Cliente:").grid(row=0, column=0, sticky=tk.W)
        self.customer_entry = ttk.Entry(bottom_frame, width=30)
        self.customer_entry.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(bottom_frame, text="CPF/CNPJ:").grid(row=0, column=2, sticky=tk.W)
        self.doc_entry = ttk.Entry(bottom_frame, width=20)
        self.doc_entry.grid(row=0, column=3, sticky=tk.W, padx=5)
        
        # Forma de pagamento
        ttk.Label(bottom_frame, text="Pagamento:").grid(row=1, column=0, sticky=tk.W)
        self.payment_var = tk.StringVar(value="Dinheiro")
        payment_options = ["Dinheiro", "Cartão Débito", "Cartão Crédito", "PIX", "Transferência"]
        self.payment_combobox = ttk.Combobox(bottom_frame, textvariable=self.payment_var, values=payment_options, width=15)
        self.payment_combobox.grid(row=1, column=1, sticky=tk.W, padx=5)
        
        # Totais
        ttk.Label(bottom_frame, text="Subtotal:").grid(row=2, column=0, sticky=tk.W)
        self.subtotal_label = ttk.Label(bottom_frame, text="R$ 0.00", font=('Helvetica', 10, 'bold'))
        self.subtotal_label.grid(row=2, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(bottom_frame, text="Desconto:").grid(row=2, column=2, sticky=tk.W)
        self.discount_entry = ttk.Entry(bottom_frame, width=10)
        self.discount_entry.insert(0, "0.00")
        self.discount_entry.grid(row=2, column=3, sticky=tk.W, padx=5)
        
        ttk.Label(bottom_frame, text="Total:").grid(row=3, column=0, sticky=tk.W)
        self.total_label = ttk.Label(bottom_frame, text="R$ 0.00", font=('Helvetica', 12, 'bold'))
        self.total_label.grid(row=3, column=1, sticky=tk.W, padx=5)
        
        # Botões de ação
        action_frame = ttk.Frame(bottom_frame)
        action_frame.grid(row=4, column=0, columnspan=4, pady=10)
        
        self.finalize_button = ttk.Button(action_frame, text="Finalizar Venda", command=self.finalize_sale, style='Accent.TButton')
        self.finalize_button.pack(side=tk.LEFT, padx=5)
        
        self.print_button = ttk.Button(action_frame, text="Imprimir Nota", command=self.print_receipt)
        self.print_button.pack(side=tk.LEFT, padx=5)
        
        self.pdf_button = ttk.Button(action_frame, text="Salvar como PDF", command=self.save_as_pdf)
        self.pdf_button.pack(side=tk.LEFT, padx=5)
        
        # Configurar estilo
        style = ttk.Style()
        style.configure('Accent.TButton', font=('Helvetica', 10, 'bold'), foreground='green')
        
        # Bind events
        self.discount_entry.bind('<KeyRelease>', self.update_totals)
        
        # Barra de status
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.status_label = ttk.Label(
            self.status_frame, 
            text=f"Atendente: {self.current_user[3]} | Carrinho: 0 itens"
        )
        self.status_label.pack(side=tk.LEFT, padx=10)
    
    def load_products(self):
        # Limpar treeview
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        # Carregar produtos do banco de dados
        conn = create_connection()
        if conn is not None:
            products = get_all_products(conn)
            conn.close()
            
            for product in products:
                if product[5] > 0:  # Só mostra produtos com estoque > 0
                    self.products_tree.insert("", tk.END, values=(
                        product[0],  # ID
                        product[1],  # Nome
                        f"{product[4]:.2f}",  # Preço
                        product[5]   # Quantidade
                    ))
    
    def add_to_cart(self):
        selected_item = self.products_tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Por favor, selecione um produto para adicionar")
            return
        
        product_id = self.products_tree.item(selected_item[0], "values")[0]
        product_name = self.products_tree.item(selected_item[0], "values")[1]
        price = float(self.products_tree.item(selected_item[0], "values")[2])
        stock = int(self.products_tree.item(selected_item[0], "values")[3])
        
        # Pedir quantidade
        quantity = simpledialog.askinteger("Quantidade", f"Quantidade de '{product_name}':", minvalue=1, maxvalue=stock)
        if quantity is None or quantity <= 0:
            return
        
        # Verificar se o produto já está no carrinho
        for item in self.cart:
            if item["id"] == product_id:
                item["quantity"] += quantity
                item["total"] = item["quantity"] * price
                self.update_cart_display()
                self.update_totals()
                return
        
        # Adicionar novo item ao carrinho
        self.cart.append({
            "id": product_id,
            "name": product_name,
            "quantity": quantity,
            "price": price,
            "total": quantity * price
        })
        
        self.update_cart_display()
        self.update_totals()
    
    def remove_from_cart(self):
        selected_item = self.cart_tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Por favor, selecione um item para remover")
            return
        
        product_id = self.cart_tree.item(selected_item[0], "values")[0]
        
        # Remover item do carrinho
        self.cart = [item for item in self.cart if item["id"] != product_id]
        
        self.update_cart_display()
        self.update_totals()
    
    def clear_cart(self):
        if not self.cart:
            return
            
        if messagebox.askyesno("Confirmar", "Deseja limpar todo o carrinho?"):
            self.cart = []
            self.update_cart_display()
            self.update_totals()
    
    def update_cart_display(self):
        # Limpar treeview
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        
        # Adicionar itens do carrinho
        for item in self.cart:
            self.cart_tree.insert("", tk.END, values=(
                item["id"],
                item["name"],
                item["quantity"],
                f"{item['price']:.2f}",
                f"{item['total']:.2f}"
            ))
        
        # Atualizar status
        self.status_label.config(text=f"Atendente: {self.current_user[3]} | Carrinho: {len(self.cart)} itens")
    
    def update_totals(self, event=None):
        subtotal = sum(item["total"] for item in self.cart)
        
        try:
            discount = float(self.discount_entry.get())
        except ValueError:
            discount = 0.0
            self.discount_entry.delete(0, tk.END)
            self.discount_entry.insert(0, "0.00")
        
        total = max(0, subtotal - discount)  # Garante que o total não seja negativo
        
        self.subtotal_label.config(text=f"R$ {subtotal:.2f}")
        self.total_label.config(text=f"R$ {total:.2f}")
    
    def finalize_sale(self):
        if not self.cart:
            messagebox.showwarning("Aviso", "O carrinho está vazio")
            return
        
        # Obter informações do cliente
        self.customer_name = self.customer_entry.get().strip()
        self.customer_doc = self.doc_entry.get().strip()
        self.payment_method = self.payment_var.get()
        
        # Calcular totais
        subtotal = sum(item["total"] for item in self.cart)
        try:
            discount = float(self.discount_entry.get())
        except ValueError:
            discount = 0.0
        total = max(0, subtotal - discount)
        
        # Confirmar venda
        if not messagebox.askyesno("Confirmar Venda", f"Total da venda: R$ {total:.2f}\n\nConfirmar venda?"):
            return
        
        # Registrar venda no banco de dados
        conn = create_connection()
        if conn is not None:
            try:
                # Iniciar transação
                conn.execute("BEGIN TRANSACTION")
                
                # Adicionar venda
                sale_id = add_sale(
                    conn,
                    self.customer_name if self.customer_name else "Consumidor Final",
                    self.customer_doc,
                    subtotal,
                    discount,
                    total,
                    self.payment_method,
                    self.current_user[0]  # user_id
                )
                
                if sale_id:
                    # Adicionar itens da venda e atualizar estoque
                    for item in self.cart:
                        add_sale_item(
                            conn,
                            sale_id,
                            item["id"],
                            item["quantity"],
                            item["price"],
                            item["total"]
                        )
                        
                        # Atualizar estoque
                        update_product_quantity(conn, item["id"], item["quantity"])
                    
                    # Commit da transação
                    conn.commit()
                    
                    messagebox.showinfo("Sucesso", f"Venda finalizada com sucesso!\nNúmero da nota: {sale_id}")
                    
                    # Limpar carrinho e campos
                    self.cart = []
                    self.customer_entry.delete(0, tk.END)
                    self.doc_entry.delete(0, tk.END)
                    self.discount_entry.delete(0, tk.END)
                    self.discount_entry.insert(0, "0.00")
                    self.update_cart_display()
                    self.update_totals()
                    self.load_products()  # Atualizar estoque
                    
                    # Gerar nota fiscal
                    self.generate_receipt(sale_id)
                else:
                    conn.rollback()
                    messagebox.showerror("Erro", "Não foi possível registrar a venda")
                
            except Error as e:
                conn.rollback()
                messagebox.showerror("Erro", f"Ocorreu um erro ao registrar a venda:\n{str(e)}")
            
            finally:
                conn.close()
    
    def generate_receipt(self, sale_id):
        """Gera os dados da nota fiscal"""
        conn = create_connection()
        if conn is not None:
            sale, items = get_sale_by_id(conn, sale_id)
            conn.close()
            
            if sale and items:
                receipt_data = {
                    "sale_id": sale[0],
                    "date": sale[1],
                    "customer_name": sale[2],
                    "customer_doc": sale[3],
                    "subtotal": sale[4],
                    "discount": sale[5],
                    "total": sale[6],
                    "payment_method": sale[7],
                    "cashier": self.current_user[3],
                    "items": []
                }
                
                for item in items:
                    receipt_data["items"].append({
                        "name": item[6],  # product name
                        "quantity": item[3],
                        "unit_price": item[4],
                        "total_price": item[5]
                    })
                
                return receipt_data
        return None
    
    def print_receipt(self):
        """Imprime a nota fiscal"""
        if not self.cart:
            messagebox.showwarning("Aviso", "Não há itens no carrinho para gerar nota")
            return
        
        # Para impressão real, você precisaria de uma impressora configurada
        # Aqui vamos apenas mostrar uma prévia
        receipt_data = {
            "sale_id": "PRÉVIA",
            "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "customer_name": self.customer_entry.get() or "Consumidor Final",
            "customer_doc": self.doc_entry.get() or "",
            "subtotal": sum(item["total"] for item in self.cart),
            "discount": float(self.discount_entry.get()),
            "total": float(self.total_label.cget("text").replace("R$ ", "")),
            "payment_method": self.payment_var.get(),
            "cashier": self.current_user[3],
            "items": self.cart
        }
        
        self.show_receipt_preview(receipt_data)
    
    def save_as_pdf(self):
        """Salva a nota fiscal como PDF"""
        if not self.cart:
            messagebox.showwarning("Aviso", "Não há itens no carrinho para gerar nota")
            return
        
        # Gerar dados da nota
        receipt_data = {
            "sale_id": "PRÉVIA",
            "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "customer_name": self.customer_entry.get() or "Consumidor Final",
            "customer_doc": self.doc_entry.get() or "",
            "subtotal": sum(item["total"] for item in self.cart),
            "discount": float(self.discount_entry.get()),
            "total": float(self.total_label.cget("text").replace("R$ ", "")),
            "payment_method": self.payment_var.get(),
            "cashier": self.current_user[3],
            "items": self.cart
        }
        
        # Pedir local para salvar
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            title="Salvar Nota Fiscal como PDF",
            initialfile=f"NotaFiscal_{receipt_data['sale_id']}.pdf"
        )
        
        if file_path:
            self.create_pdf(receipt_data, file_path)
            messagebox.showinfo("Sucesso", f"Nota fiscal salva como:\n{file_path}")
    
    def show_receipt_preview(self, receipt_data):
        """Mostra uma prévia da nota fiscal"""
        preview_window = tk.Toplevel(self.root)
        preview_window.title(f"Prévia da Nota Fiscal - Nº {receipt_data['sale_id']}")
        
        # Frame principal
        frame = ttk.Frame(preview_window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Cabeçalho
        ttk.Label(frame, text="NOTA FISCAL", font=('Helvetica', 14, 'bold')).pack(pady=5)
        ttk.Label(frame, text=f"Nº: {receipt_data['sale_id']}").pack()
        ttk.Label(frame, text=f"Data: {receipt_data['date']}").pack()
        
        # Linha divisória
        ttk.Separator(frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # Cliente
        ttk.Label(frame, text="CLIENTE:", font=('Helvetica', 10, 'bold')).pack(anchor=tk.W)
        ttk.Label(frame, text=receipt_data['customer_name']).pack(anchor=tk.W)
        if receipt_data['customer_doc']:
            ttk.Label(frame, text=f"CPF/CNPJ: {receipt_data['customer_doc']}").pack(anchor=tk.W)
        
        # Linha divisória
        ttk.Separator(frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # Itens
        ttk.Label(frame, text="ITENS", font=('Helvetica', 10, 'bold')).pack(anchor=tk.W)
        
        items_frame = ttk.Frame(frame)
        items_frame.pack(fill=tk.X)
        
        # Cabeçalho dos itens
        ttk.Label(items_frame, text="Descrição", width=30, anchor=tk.W).grid(row=0, column=0)
        ttk.Label(items_frame, text="Qtd", width=5, anchor=tk.CENTER).grid(row=0, column=1)
        ttk.Label(items_frame, text="Unit.", width=10, anchor=tk.E).grid(row=0, column=2)
        ttk.Label(items_frame, text="Total", width=10, anchor=tk.E).grid(row=0, column=3)
        
        # Adicionar itens
        for i, item in enumerate(receipt_data['items'], start=1):
            ttk.Label(items_frame, text=item['name'], anchor=tk.W).grid(row=i, column=0, sticky=tk.W)
            ttk.Label(items_frame, text=str(item['quantity']), anchor=tk.CENTER).grid(row=i, column=1)
            ttk.Label(items_frame, text=f"R$ {item['unit_price']:.2f}", anchor=tk.E).grid(row=i, column=2)
            ttk.Label(items_frame, text=f"R$ {item['total_price']:.2f}", anchor=tk.E).grid(row=i, column=3)
        
        # Linha divisória
        ttk.Separator(frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # Totais
        ttk.Label(frame, text=f"Subtotal: R$ {receipt_data['subtotal']:.2f}", anchor=tk.E).pack(fill=tk.X)
        ttk.Label(frame, text=f"Desconto: R$ {receipt_data['discount']:.2f}", anchor=tk.E).pack(fill=tk.X)
        ttk.Label(frame, text=f"TOTAL: R$ {receipt_data['total']:.2f}", font=('Helvetica', 12, 'bold'), anchor=tk.E).pack(fill=tk.X)
        
        # Pagamento
        ttk.Separator(frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        ttk.Label(frame, text=f"Forma de Pagamento: {receipt_data['payment_method']}").pack(anchor=tk.W)
        
        # Atendente
        ttk.Label(frame, text=f"Atendente: {receipt_data['cashier']}").pack(anchor=tk.W)
        
        # Botões
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Imprimir", command=lambda: self.print_receipt_to_printer(receipt_data)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Salvar como PDF", command=lambda: self.save_receipt_as_pdf(receipt_data)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Fechar", command=preview_window.destroy).pack(side=tk.LEFT, padx=5)
    
    def create_pdf(self, receipt_data, file_path):
        """Cria um PDF da nota fiscal"""
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Cabeçalho
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "NOTA FISCAL", 0, 1, 'C')
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"Nº: {receipt_data['sale_id']}", 0, 1)
        pdf.cell(0, 10, f"Data: {receipt_data['date']}", 0, 1)
        pdf.ln(5)
        
        # Cliente
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "CLIENTE:", 0, 1)
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, receipt_data['customer_name'], 0, 1)
        if receipt_data['customer_doc']:
            pdf.cell(0, 10, f"CPF/CNPJ: {receipt_data['customer_doc']}", 0, 1)
        pdf.ln(5)
        
        # Itens
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "ITENS", 0, 1)
        pdf.set_font("Arial", size=10)
        
        # Cabeçalho da tabela
        pdf.cell(100, 10, "Descrição", 1)
        pdf.cell(20, 10, "Qtd", 1, 0, 'C')
        pdf.cell(30, 10, "Unit. (R$)", 1, 0, 'R')
        pdf.cell(30, 10, "Total (R$)", 1, 0, 'R')
        pdf.ln()
        
        # Itens
        for item in receipt_data['items']:
            pdf.cell(100, 10, item['name'], 1)
            pdf.cell(20, 10, str(item['quantity']), 1, 0, 'C')
            pdf.cell(30, 10, f"{item['unit_price']:.2f}", 1, 0, 'R')
            pdf.cell(30, 10, f"{item['total_price']:.2f}", 1, 0, 'R')
            pdf.ln()
        
        # Totais
        pdf.set_font("Arial", size=12)
        pdf.cell(150, 10, "Subtotal:", 0, 0, 'R')
        pdf.cell(30, 10, f"R$ {receipt_data['subtotal']:.2f}", 0, 1, 'R')
        
        pdf.cell(150, 10, "Desconto:", 0, 0, 'R')
        pdf.cell(30, 10, f"R$ {receipt_data['discount']:.2f}", 0, 1, 'R')
        
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(150, 10, "TOTAL:", 0, 0, 'R')
        pdf.cell(30, 10, f"R$ {receipt_data['total']:.2f}", 0, 1, 'R')
        pdf.ln(10)
        
        # Pagamento e atendente
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"Forma de Pagamento: {receipt_data['payment_method']}", 0, 1)
        pdf.cell(0, 10, f"Atendente: {receipt_data['cashier']}", 0, 1)
        
        # Rodapé
        pdf.set_y(-15)
        pdf.set_font("Arial", 'I', 8)
        pdf.cell(0, 10, "Sistema de Gerenciamento de Estoque", 0, 0, 'C')
        
        # Salvar PDF
        pdf.output(file_path)
    
    def print_receipt_to_printer(self, receipt_data):
        """Envia a nota fiscal para a impressora"""
        # Esta é uma implementação simplificada
        # Em um sistema real, você precisaria configurar a impressora
        
        # Primeiro criamos um PDF temporário
        temp_path = os.path.join(os.getenv("TEMP"), f"temp_receipt_{receipt_data['sale_id']}.pdf")
        self.create_pdf(receipt_data, temp_path)
        
        try:
            # Abrir o PDF com o visualizador padrão (que pode ter opção de impressão)
            os.startfile(temp_path, 'print')
            messagebox.showinfo("Impressão", "Nota fiscal enviada para impressão")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível imprimir:\n{str(e)}")
    
    def save_receipt_as_pdf(self, receipt_data):
        """Salva a nota fiscal como PDF"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            title="Salvar Nota Fiscal como PDF",
            initialfile=f"NotaFiscal_{receipt_data['sale_id']}.pdf"
        )
        
        if file_path:
            self.create_pdf(receipt_data, file_path)
            messagebox.showinfo("Sucesso", f"Nota fiscal salva como:\n{file_path}")