# Хорошая практика: брать порты из конфига
app.run(port=config['port'])
connect(listen_port=app.config.PORT)
api_url = config['api_base_url'] + "/v1"

# Случайные числа, не связанные с портами
count = 8080
items = [80, 443] # В списке без контекста допустимо
