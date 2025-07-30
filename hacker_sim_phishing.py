from PIL import ImageGrab, Image, PngImagePlugin, ImageFilter
from time import sleep
import pytesseract  # OCR, extrae texto (str) desde un objeto PIL.ImageGrab.
clipboard = None  # Variable global para el portapapeles. Solo guarda imágenes si son del tipo PngImageFile.

intereses = {
    "Family and Relationships": ['Dating','Family','Fatherhood','Friendship','Marriage','Motherhood','Parenting','Weddings'],
    "Shopping and Fashion": ['Clothing','Cosmetics','Coupons','Dresses','Fragrances','Handbags','Jewelry','Malls','Shoes','Sunglasses','Tattoos','Toys'],
    'Food and Drink': ['Baking','Barbecue','Beer','Chocolate','Coffee','Coffeehouses','Desserts','Juice','Pizza','Recipes','Tea','Veganism','Wine'],
    "Business": ['Advertising','Agriculture','Architecture','Aviation','Banking','Business','Construction','Design','Economics','Engineering','Design','Entrepreneurship','Finance','Investment','Insurance','Management','Marketing','Online','Retail','Sales','Science'],
    "Entertainment": ['Bars','Books','Comics','Concerts','Dancehalls','Documentary','Festivals','Games','Literature','Magazines','Manga','Movies','Music','Newspapers','Nightclubs','Parties','Plays','Poker','Talkshows','Theatre']
}
# Lista de intereses extraída de una guía de Steam:
# https://steamcommunity.com/sharedfiles/filedetails/?id=2645422003


def obtener_tipo_de_cuenta(interest_list):
    conteo_intereses = {}
    for tipo in intereses:
        conteo_intereses[tipo] = 0  # Inicializa con cero
        for interes in intereses[tipo]:
            if interes in interest_list:
                conteo_intereses[tipo] += 1  # Suma si hay coincidencia
    mayor_interes = [tipo for tipo in sorted(conteo_intereses, key=conteo_intereses.get, reverse=True)][0]
    print("Necesitas una cuenta de tipo: " + mayor_interes)


def procesar_imagen(imagen):  # Aquí ejecutamos el OCR.
    imagen_mejorada = imagen.filter(ImageFilter.SHARPEN)
    resultado = [linea for linea in pytesseract.image_to_string(imagen_mejorada).split("\n") if len(linea) > 1]
    obtener_tipo_de_cuenta(resultado)

def imagenes_son_iguales(im1, im2):
    if type(im1) == PngImagePlugin.PngImageFile and type(im2) == type(im1):
        if list(im1.getdata()) == list(im2.getdata()):  # Compara datos de píxeles
            return True
    return False

while True:
    clip = ImageGrab.grabclipboard()  # Captura el portapapeles
    if type(clip) == PngImagePlugin.PngImageFile:
        if not imagenes_son_iguales(clip, clipboard):
            clipboard = clip  # Guarda nueva imagen
            procesar_imagen(clip)  # Ejecuta el OCR
    sleep(4)  # Espera 4 segundos antes de revisar nuevamente el portapapeles
