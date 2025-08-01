# タイトル: app.py
# 履歴管理と式末尾の削除機能を含むFlask電卓

from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # セッション用の秘密鍵（任意の文字列）

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    expression = ""

    if "history" not in session:
        session["history"] = []

    if request.method == "POST":
        expression = request.form.get("expression", "")
        try:
            if not expression or not all(c in "0123456789+-*/.()" for c in expression):
                raise ValueError("不正な文字が含まれています")
            result = eval(expression)

            # 履歴を追加（最大10件まで）
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

if __name__ == "__main__":
    app.run(debug=True)
