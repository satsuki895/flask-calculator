# タイトル: app.py
# Flask 電卓アプリ（Render用）- セッションごとに履歴初期化、演算子の連続入力制御

import os
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # 本番ではランダムな長い文字列に変更してください

@app.before_request
def initialize_session():
    # セッションが新規なら履歴を初期化
    if "initialized" not in session:
        session["history"] = []
        session["initialized"] = True

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    expression = ""

    if request.method == "POST":
        expression = request.form.get("expression", "")

        # 四則演算子が連続している場合、最後の1つだけに置き換え
        while len(expression) >= 2 and expression[-1] in "+-*/" and expression[-2] in "+-*/":
            expression = expression[:-2] + expression[-1]

        try:
            # セキュリティ対策：使用可能な文字のみに制限
            if not all(c in "0123456789+-*/.()" for c in expression):
                raise ValueError("不正な文字が含まれています")

            result = eval(expression)

            # 履歴に追加（最大10件）
            session["history"].append(f"{expression} = {result}")
            session["history"] = session["history"][-10:]

        except ZeroDivisionError:
            result = "エラー：0で割ることはできません"
        except Exception:
            result = "エラー：式が不正です"

        session.modified = True

    return render_template("index.html", result=result, expression=expression, history=session["history"])

@app.route("/clear_history")
def clear_history():
    session.pop("history", None)
    return redirect(url_for("index"))

# Render対応（環境変数 PORT に対応）
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
