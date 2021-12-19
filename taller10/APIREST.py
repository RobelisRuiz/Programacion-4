from flask import Flask, jsonify, request

app = Flask(__name__)

from p import p

# Testing Route


# Get Data Routes
@app.route('/palabras')
def getPalabras():
    # return jsonify(palabras)
    return jsonify({'palabras': p})


@app.route('/palabras/<string:palabra_significado>')
def getPalabra(palabra_significado):
    palabrasFound = [
        palabra for palabra in p if palabra['palabra'] == palabra_significado.lower()]
    if (len(palabrasFound) > 0):
        return jsonify({'palabra': palabrasFound[0]})
    return jsonify({'message': ''})

# Create Data Routes
@app.route('/palabras', methods=['POST'])
def addPalabra():
    nueva_palabra = {
        'palabra': request.json['palabra'],
        'significado': request.json['significado'],
    }
    p.append(nueva_palabra)
    return jsonify({'palabras': p})

# Update Data Route
@app.route('/palabras/<string:palabra_significado>', methods=['PUT'])
def editarpalabra(palabra_significado):
    palabrasFound = [palabra for palabra in p if palabra['palabra'] == palabra_significado]
    if (len(palabrasFound) > 0):
        palabrasFound[0]['palabra'] = request.json['palara']
        palabrasFound[0]['significado'] = request.json['significado']
        return jsonify({
            'message': 'Palabra Actualizada',
            'palabra': palabrasFound[0]
        })
    return jsonify({'message': 'Palabra no encontrada'})

# DELETE Data Route
@app.route('/palabras/<string:palabra_significado>', methods=['DELETE'])
def eliminarpalabra(palabra_significado):
    palabrasFound = [palabra for palabra in p if palabra['palabra'] == palabra_significado]
    if len(palabrasFound) > 0:
        p.remove([palabrasFound])
        return jsonify({
            'message': 'Palabra Eliminada',
            'palabras': p
        })

if __name__ == '__main__':
    app.run(debug=True, port=4000)