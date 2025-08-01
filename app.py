# タイトル: app.py
# Flask 電卓アプリ（Render用）- 安全な式評価・履歴管理・テーマ切替対応

import os
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # 必ず変更すること（任意の長い文字列）

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    expression = ""

    # 履歴セッションがなければ初期化
    if "history" not in session:
        session["history"] = []

    # POSTされたときの処理（=ボタンが押されたとき）
    if request.method == "POST":
        expression = request.form.get("expression", "")
        try:
            # 式に使用できる文字のみ許可（セキュリティ対策）
            if not expression or not all(c in "0123456789+-*/.()" for c in expression):
                raise ValueError("不正な文字が含まれています")

            result = eval(expression)  # 式評価（安全対策済）

            # 履歴に追加（最新10件）
            session["history"].append(f"{expression} = {result}")
            session["history"] = session["history"][-10:]

        except ZeroDivisionError:
            result = "エラー：0で割ることはできません"
        except Exception:
            result = "エラー：式が不正です"

        session.modified = True  # セッション更新フラグ

    return render_template("index.html", result=result, expression=expression, history=session["history"])

@app.route("/clear_history")
def clear_history():
    session.pop("history", None)
    return redirect(url_for("index"))

# Render環境用：ポートとホストを環境変数から取得
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # RenderではPORT環境変数が指定される
    app.run(host="0.0.0.0", port=port, debug=False)
