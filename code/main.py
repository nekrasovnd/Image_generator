import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
from engine import ImageGeneratorEngine

class AppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Generator - Курсовая работа")
        self.root.geometry("600x800")
        
        self.engine = ImageGeneratorEngine()
        self.setup_ui()

    def setup_ui(self):
        # Заголовок
        tk.Label(self.root, text="Генератор на базе Stable Diffusion", font=("Arial", 14, "bold")).pack(pady=10)

        # Кнопка инициализации
        self.btn_init = ttk.Button(self.root, text="1. Инициализировать систему", command=self.run_init)
        self.btn_init.pack(pady=5)

        # Поле ввода промпта
        tk.Label(self.root, text="Введите промпт (English):").pack(pady=10)
        self.prompt_txt = tk.Text(self.root, height=4, width=60)
        self.prompt_txt.insert("1.0", "photorealistic black Lada Priora car, night city...")
        self.prompt_txt.pack(padx=20)

        # Выбор шагов
        tk.Label(self.root, text="Количество шагов (Steps):").pack(pady=5)
        self.steps_var = tk.IntVar(value=20)
        self.steps_spin = tk.Spinbox(self.root, from_=5, to=100, textvariable=self.steps_var)
        self.steps_spin.pack()

        # Кнопка старта
        self.btn_gen = ttk.Button(self.root, text="2. Сгенерировать", state="disabled", command=self.run_gen)
        self.btn_gen.pack(pady=20)

        # Статус
        self.status_var = tk.StringVar(value="Система не готова")
        tk.Label(self.root, textvariable=self.status_var, fg="blue").pack()

        # Холст для картинки
        self.canvas = tk.Label(self.root, text="Картинка появится здесь", bg="lightgrey", width=50, height=20)
        self.canvas.pack(pady=10)

    def run_init(self):
        self.status_var.set("Загрузка модели... Ждите.")
        self.btn_init.config(state="disabled")
        # Поток, чтобы GUI не завис (раздел 2.3 курсовой)
        threading.Thread(target=self._init_task, daemon=True).start()

    def _init_task(self):
        if self.engine.initialize_model():
            self.root.after(0, lambda: self.status_var.set("Готов к работе"))
            self.root.after(0, lambda: self.btn_gen.config(state="normal"))

    def run_gen(self):
        prompt = self.prompt_txt.get("1.0", tk.END).strip()
        steps = self.steps_var.get()
        self.status_var.set(f"Генерация... (CPU загружен)")
        self.btn_gen.config(state="disabled")
        threading.Thread(target=lambda: self._gen_task(prompt, steps), daemon=True).start()

    def _gen_task(self, prompt, steps):
        res = self.engine.generate_image(prompt, steps)
        if res:
            img, t = res
            img.save("last_result.png")
            
            # Подготовка для отображения
            img.thumbnail((400, 400))
            tk_img = ImageTk.PhotoImage(img)
            
            self.root.after(0, lambda: self._update_ui_result(tk_img, t))

    def _update_ui_result(self, tk_img, t):
        self.canvas.config(image=tk_img, text="")
        self.canvas.image = tk_img
        self.status_var.set(f"Готово! Время: {t} сек. Сохранено в last_result.png")
        self.btn_gen.config(state="normal")

if __name__ == "__main__":
    window = tk.Tk()
    app = AppGUI(window)
    window.mainloop()