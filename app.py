# タイトル: app.py
# Flask 電卓アプリ（安全な式評価・履歴管理・Render対応）

import os
import math
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

@app.before_request
def initialize_session():
    """新しいセッションごとに履歴を初期化"""
    if "initialized" not in session:
        session.clear()
        session["initialized"] = True
        session["history"] = []

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    expression = ""

    if "history" not in session:
        session["history"] = []

    if request.method == "POST":
        expression = request.form.get("expression", "")

        try:
            allowed_chars = "0123456789+-*/().sqrt"
            if not all(c in allowed_chars for c in expression.replace("sqrt", "")):
                raise ValueError("不正な文字が含まれています")

            allowed_names = {"sqrt": math.sqrt}
            result = eval(expression, {"__builtins__": None}, allowed_names)

            session["history"].append(f"{expression} = {result}")
            session["history"] = session["history"][-10:]
            session.modified = True

            expression = ""  # 入力欄を毎回リセット

        except ZeroDivisionError:
            result = "エラー：0で割ることはできません"
        except Exception:
            result = "エラー：式が不正です"

    return render_template("index.html", result=result, expression=expression, history=session.get("history", []))

@app.route("/clear_history")
def clear_history():
    session.pop("history", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
