from model import isMain, app

# TÊN ỨNG DỤNG
app.setApplicationName("Pixel Browser")
# TÊN CÔNG TY
app.setOrganizationName("Pixel")
# TÊN MIỀN
app.setOrganizationDomain("https://github.com/KWalkerNNK/maple-leaf")

window = isMain()
app.exec_()

