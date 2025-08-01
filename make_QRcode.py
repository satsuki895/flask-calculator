import qrcode

# 対象URL
url = 'https://flask-calculator-nw0r.onrender.com'

# QRコード作成
qr = qrcode.QRCode(
    version=1,
    box_size=10,
    border=4
)
qr.add_data(url)
qr.make(fit=True)

# 画像を作成して保存
img = qr.make_image(fill_color='black', back_color='white')
img.save('flask_calculator_qr.png')  # 保存

# 表示（ローカルPCの画像ビューアで開く）
img.show()
