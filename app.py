import os
import queue
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


def build_command(executable: str, input_path: str, output_dir: str, language: str, ocr: bool, device: str, extra_args: str) -> list[str]:
    cmd = [executable, "--input", input_path, "--output", output_dir]

    if language and language != "auto":
        cmd.extend(["--lang", language])

    if ocr:
        cmd.append("--ocr")

    if device and device != "auto":
        cmd.extend(["--device", device])

    if extra_args.strip():
        cmd.extend(extra_args.strip().split())

    return cmd


class MinerUGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MinerU 可视化工具")
        self.geometry("900x600")

        self.log_queue: queue.Queue[str] = queue.Queue()
        self.running_process: subprocess.Popen | None = None

        self._build_ui()
        self.after(100, self._flush_logs)

    def _build_ui(self):
        frame = ttk.Frame(self, padding=12)
        frame.pack(fill=tk.BOTH, expand=True)

        for i in range(3):
            frame.columnconfigure(i, weight=1 if i == 1 else 0)

        row = 0
        ttk.Label(frame, text="MinerU 可执行命令:").grid(row=row, column=0, sticky="w", pady=4)
        self.executable_var = tk.StringVar(value="mineru")
        ttk.Entry(frame, textvariable=self.executable_var).grid(row=row, column=1, sticky="ew", pady=4)
        ttk.Button(frame, text="浏览", command=self._browse_executable).grid(row=row, column=2, padx=6)

        row += 1
        ttk.Label(frame, text="输入文件:").grid(row=row, column=0, sticky="w", pady=4)
        self.input_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.input_var).grid(row=row, column=1, sticky="ew", pady=4)
        ttk.Button(frame, text="选择文件", command=self._browse_input).grid(row=row, column=2, padx=6)

        row += 1
        ttk.Label(frame, text="输出目录:").grid(row=row, column=0, sticky="w", pady=4)
        self.output_var = tk.StringVar(value=os.path.join(os.getcwd(), "output"))
        ttk.Entry(frame, textvariable=self.output_var).grid(row=row, column=1, sticky="ew", pady=4)
        ttk.Button(frame, text="选择目录", command=self._browse_output).grid(row=row, column=2, padx=6)

        row += 1
        ttk.Label(frame, text="语言:").grid(row=row, column=0, sticky="w", pady=4)
        self.language_var = tk.StringVar(value="auto")
        lang_box = ttk.Combobox(frame, textvariable=self.language_var, values=["auto", "zh", "en", "ja", "ko"], state="readonly")
        lang_box.grid(row=row, column=1, sticky="w", pady=4)

        row += 1
        ttk.Label(frame, text="设备:").grid(row=row, column=0, sticky="w", pady=4)
        self.device_var = tk.StringVar(value="auto")
        device_box = ttk.Combobox(frame, textvariable=self.device_var, values=["auto", "cpu", "cuda", "mps"], state="readonly")
        device_box.grid(row=row, column=1, sticky="w", pady=4)

        row += 1
        self.ocr_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame, text="启用 OCR", variable=self.ocr_var).grid(row=row, column=1, sticky="w", pady=4)

        row += 1
        ttk.Label(frame, text="附加参数:").grid(row=row, column=0, sticky="w", pady=4)
        self.extra_args_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.extra_args_var).grid(row=row, column=1, sticky="ew", pady=4)

        row += 1
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=row, column=0, columnspan=3, sticky="w", pady=8)

        self.start_btn = ttk.Button(btn_frame, text="开始处理", command=self.start_processing)
        self.start_btn.pack(side=tk.LEFT)
        self.stop_btn = ttk.Button(btn_frame, text="停止", command=self.stop_processing, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=8)

        row += 1
        ttk.Label(frame, text="运行日志:").grid(row=row, column=0, sticky="w", pady=(8, 4))

        row += 1
        self.log_text = tk.Text(frame, height=20)
        self.log_text.grid(row=row, column=0, columnspan=3, sticky="nsew")
        frame.rowconfigure(row, weight=1)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.log_text.yview)
        scrollbar.grid(row=row, column=3, sticky="ns")
        self.log_text.configure(yscrollcommand=scrollbar.set)

    def _browse_executable(self):
        path = filedialog.askopenfilename(title="选择 MinerU 可执行文件")
        if path:
            self.executable_var.set(path)

    def _browse_input(self):
        path = filedialog.askopenfilename(title="选择输入文件", filetypes=[("Document", "*.pdf *.png *.jpg *.jpeg *.bmp"), ("All Files", "*.*")])
        if path:
            self.input_var.set(path)

    def _browse_output(self):
        path = filedialog.askdirectory(title="选择输出目录")
        if path:
            self.output_var.set(path)

    def _append_log(self, text: str):
        self.log_text.insert(tk.END, text + "\n")
        self.log_text.see(tk.END)

    def _flush_logs(self):
        while True:
            try:
                line = self.log_queue.get_nowait()
            except queue.Empty:
                break
            self._append_log(line)
        self.after(100, self._flush_logs)

    def start_processing(self):
        input_path = self.input_var.get().strip()
        output_dir = self.output_var.get().strip()

        if not input_path:
            messagebox.showerror("错误", "请先选择输入文件")
            return

        if not os.path.exists(input_path):
            messagebox.showerror("错误", "输入文件不存在")
            return

        os.makedirs(output_dir, exist_ok=True)

        cmd = build_command(
            executable=self.executable_var.get().strip(),
            input_path=input_path,
            output_dir=output_dir,
            language=self.language_var.get(),
            ocr=self.ocr_var.get(),
            device=self.device_var.get(),
            extra_args=self.extra_args_var.get(),
        )

        self._append_log(f"开始执行: {' '.join(cmd)}")
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)

        thread = threading.Thread(target=self._run_command, args=(cmd,), daemon=True)
        thread.start()

    def _run_command(self, cmd: list[str]):
        try:
            self.running_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )

            assert self.running_process.stdout is not None
            for line in self.running_process.stdout:
                self.log_queue.put(line.rstrip())

            code = self.running_process.wait()
            self.log_queue.put(f"执行结束，退出码: {code}")
        except FileNotFoundError:
            self.log_queue.put("找不到 MinerU 可执行程序，请检查命令路径。")
        except Exception as e:  # noqa: BLE001
            self.log_queue.put(f"运行失败: {e}")
        finally:
            self.running_process = None
            self.after(0, lambda: self.start_btn.config(state=tk.NORMAL))
            self.after(0, lambda: self.stop_btn.config(state=tk.DISABLED))

    def stop_processing(self):
        if self.running_process and self.running_process.poll() is None:
            self.running_process.terminate()
            self._append_log("已发送停止信号。")


if __name__ == "__main__":
    app = MinerUGUI()
    app.mainloop()
