from Converter import Converter

filepath = "resources/Test.abc"
converter = Converter(filepath)
converter.convert_song()
print(converter.get_left("1"))
print(converter.get_right("1"))