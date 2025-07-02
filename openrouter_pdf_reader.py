import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import PyPDF2
import requests
import json

class PDFQAApp:
    def __init__(self, master):
        self.master = master
        master.title("PDF QA with OpenRouter")
        master.geometry("700x800") # Set initial window size

        self.pdf_text = ""
        self.chat_history = []
        self.api_key = "" # This will be read from the input field

        # --- API Key Input ---
        self.api_key_frame = tk.Frame(master)
        self.api_key_frame.pack(pady=5)

        self.api_key_label = tk.Label(self.api_key_frame, text="OpenRouter API Key:")
        self.api_key_label.pack(side=tk.LEFT, padx=5)

        self.api_key_entry = tk.Entry(self.api_key_frame, width=50, show="*") # show="*" for password-like input
        self.api_key_entry.pack(side=tk.LEFT, padx=5)

        # --- PDF Selection ---
        self.pdf_frame = tk.Frame(master)
        self.pdf_frame.pack(pady=10)

        self.select_pdf_button = tk.Button(self.pdf_frame, text="Select PDF", command=self.select_pdf)
        self.select_pdf_button.pack(side=tk.LEFT, padx=5)

        self.pdf_path_label = tk.Label(self.pdf_frame, text="No PDF selected")
        self.pdf_path_label.pack(side=tk.LEFT, padx=5)

        self.process_pdf_button = tk.Button(self.pdf_frame, text="Process PDF", command=self.process_pdf)
        self.process_pdf_button.pack(side=tk.LEFT, padx=5)

        # --- Parsed PDF Content Display (Optional, but good for feedback) ---
        self.pdf_content_label = tk.Label(master, text="Parsed PDF Content (first 500 chars):")
        self.pdf_content_label.pack(pady=5)
        self.pdf_content_display = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=90, height=10, state='disabled')
        self.pdf_content_display.pack(pady=5)

        # --- Conversation Area ---
        self.conversation_label = tk.Label(master, text="Conversation:")
        self.conversation_label.pack(pady=5)
        self.conversation_display = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=90, height=15, state='disabled')
        self.conversation_display.pack(pady=5)

        # --- Question Input ---
        self.question_frame = tk.Frame(master)
        self.question_frame.pack(pady=10)

        self.question_label = tk.Label(self.question_frame, text="Your Question:")
        self.question_label.pack(side=tk.LEFT, padx=5)

        self.question_entry = tk.Entry(self.question_frame, width=60)
        self.question_entry.pack(side=tk.LEFT, padx=5)
        self.question_entry.bind("<Return>", self.ask_question_event) # Allows pressing Enter to ask

        self.ask_button = tk.Button(self.question_frame, text="Ask", command=self.ask_question)
        self.ask_button.pack(side=tk.LEFT, padx=5)

        # --- Control Buttons ---
        self.control_frame = tk.Frame(master)
        self.control_frame.pack(pady=10)

        self.clear_chat_button = tk.Button(self.control_frame, text="Clear Chat", command=self.clear_chat)
        self.clear_chat_button.pack(side=tk.LEFT, padx=5)

        self.status_label = tk.Label(master, text="Ready", fg="blue")
        self.status_label.pack(pady=5)

    def select_pdf(self):
        """Opens a file dialog to select a PDF file."""
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            self.pdf_path_label.config(text=file_path)
            self.status_label.config(text="PDF selected. Click 'Process PDF' to extract text.", fg="blue")
            self.pdf_text = "" # Clear previous text
            self.pdf_content_display.config(state='normal')
            self.pdf_content_display.delete(1.0, tk.END)
            self.pdf_content_display.config(state='disabled')

    def parse_pdf(self, file_path):
        """Parses the text content from a PDF file."""
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    text += page.extract_text() or "" # Handle pages with no extractable text
            return text
        except Exception as e:
            messagebox.showerror("PDF Parsing Error", f"Failed to parse PDF: {e}")
            return None

    def process_pdf(self):
        """Processes the selected PDF: parses it and prepares the initial chat history."""
        pdf_path = self.pdf_path_label.cget("text")
        if pdf_path == "No PDF selected":
            messagebox.showwarning("No PDF", "Please select a PDF file first.")
            return

        self.api_key = self.api_key_entry.get().strip()
        if not self.api_key:
            messagebox.showwarning("API Key Missing", "Please enter your OpenRouter API Key.")
            return

        self.status_label.config(text="Parsing PDF...", fg="orange")
        self.master.update_idletasks() # Update GUI to show status

        self.pdf_text = self.parse_pdf(pdf_path)

        if self.pdf_text:
            # Display a snippet of the parsed text
            display_text = self.pdf_text[:500] + ("..." if len(self.pdf_text) > 500 else "")
            self.pdf_content_display.config(state='normal')
            self.pdf_content_display.delete(1.0, tk.END)
            self.pdf_content_display.insert(tk.END, display_text)
            self.pdf_content_display.config(state='disabled')

            # Initialize chat history with the PDF content as system context
            self.chat_history = [
                {"role": "system", "content": "You are a helpful assistant. The following document content is provided for your reference:\n\n" + self.pdf_text}
            ]
            self.status_label.config(text="PDF processed. You can now ask questions.", fg="green")
            self.update_conversation_display("System: PDF content loaded. Ready for questions.")
        else:
            self.status_label.config(text="PDF processing failed.", fg="red")

    def ask_question_event(self, event):
        """Event handler for pressing Enter in the question entry."""
        self.ask_question()

    def ask_question(self):
        """Sends the user's question to the OpenRouter API and displays the response."""
        question = self.question_entry.get().strip()
        if not question:
            messagebox.showwarning("Empty Question", "Please enter a question.")
            return

        if not self.pdf_text:
            messagebox.showwarning("No PDF Content", "Please process a PDF first.")
            return

        if not self.api_key:
            messagebox.showwarning("API Key Missing", "Please enter your OpenRouter API Key.")
            return

        self.status_label.config(text="Asking question...", fg="orange")
        self.master.update_idletasks()

        self.update_conversation_display(f"You: {question}")
        self.question_entry.delete(0, tk.END) # Clear question input

        # Add user's question to chat history
        self.chat_history.append({"role": "user", "content": question})

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        # OpenRouter API endpoint for chat completions
        url = "https://openrouter.ai/api/v1/chat/completions"
        payload = {
            "model": "deepseek/deepseek-r1-0528:free",
            "messages": self.chat_history,
            "stream": False # We want a single response, not a stream
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
            data = response.json()

            if data and data.get("choices"):
                model_response = data["choices"][0]["message"]["content"]
                self.update_conversation_display(f"AI: {model_response}")
                # Add AI's response to chat history
                self.chat_history.append({"role": "assistant", "content": model_response})
                self.status_label.config(text="Response received.", fg="green")
            else:
                self.update_conversation_display("AI: No valid response received.")
                self.status_label.config(text="Error: No valid response.", fg="red")

        except requests.exceptions.RequestException as e:
            messagebox.showerror("API Error", f"Network or API request failed: {e}")
            self.status_label.config(text="Error: Network/API issue.", fg="red")
        except json.JSONDecodeError:
            messagebox.showerror("API Error", "Failed to decode JSON response from API.")
            self.status_label.config(text="Error: Invalid API response.", fg="red")
        except Exception as e:
            messagebox.showerror("An Error Occurred", f"An unexpected error occurred: {e}")
            self.status_label.config(text="Error: Unexpected issue.", fg="red")

    def update_conversation_display(self, message):
        """Appends a message to the conversation display area."""
        self.conversation_display.config(state='normal')
        self.conversation_display.insert(tk.END, message + "\n\n")
        self.conversation_display.see(tk.END) # Scroll to the end
        self.conversation_display.config(state='disabled')

    def clear_chat(self):
        """Clears the conversation history and display."""
        self.chat_history = [
            {"role": "system", "content": "You are a helpful assistant. The following document content is provided for your reference:\n\n" + self.pdf_text}
        ] if self.pdf_text else [] # Re-initialize with PDF content if available
        self.conversation_display.config(state='normal')
        self.conversation_display.delete(1.0, tk.END)
        self.conversation_display.config(state='disabled')
        self.status_label.config(text="Chat cleared.", fg="blue")
        if self.pdf_text:
            self.update_conversation_display("System: PDF content reloaded. Ready for new questions.")
        else:
            self.update_conversation_display("Chat cleared. Please process a PDF to start a new conversation.")


if __name__ == "__main__":
    root = tk.Tk()
    app = PDFQAApp(root)
    root.mainloop()
