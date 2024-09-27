from flask import Flask, request, render_template
import spacy
from collections import Counter

app = Flask(__name__)

# Cargar el modelo de spaCy para inglés o español
nlp = spacy.load('en_core_web_sm')  # Cambia a 'es_core_news_sm' para español

# Función para generar resumen
def generar_resumen(texto, num_oraciones=6):
    doc = nlp(texto)
    oraciones = list(doc.sents)
    palabras_importantes = [token.text.lower() for token in doc if not token.is_stop and not token.is_punct]
    frecuencias = Counter(palabras_importantes)
    puntuacion_oraciones = {}
    for i, oracion in enumerate(oraciones):
        oracion_puntaje = 0
        for palabra in oracion:
            if palabra.text.lower() in frecuencias:
                oracion_puntaje += frecuencias[palabra.text.lower()]
        puntuacion_oraciones[i] = oracion_puntaje
    oraciones_resumidas = sorted(puntuacion_oraciones, key=puntuacion_oraciones.get, reverse=True)[:num_oraciones]
    resumen = ' '.join([oraciones[i].text for i in sorted(oraciones_resumidas)])
    return resumen

# Ruta principal
@app.route('/', methods=['GET', 'POST'])
def home():
    resumen = ""
    if request.method == 'POST':
        texto = request.form['texto']
        resumen = generar_resumen(texto)
    return render_template('index1.html', resumen=resumen)

if __name__ == '__main__':
    app.run(debug=True)
