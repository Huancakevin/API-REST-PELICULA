from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///peliculas.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Pelicula(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False, unique=True)
    genero = db.Column(db.String(50), nullable=False)
    calificacion = db.Column(db.Float, nullable=False)
    director = db.Column(db.String(100))
    anio = db.Column(db.Integer)
    duracion = db.Column(db.Integer)
    descripcion = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {"id": self.id, "titulo": self.titulo, "genero": self.genero,
                "calificacion": self.calificacion, "director": self.director,
                "anio": self.anio, "duracion": self.duracion,
                "descripcion": self.descripcion}

@app.route("/")
def home():
    return jsonify({"message": "API REST de Películas"})

@app.route("/peliculas", methods=["GET"])
def get_peliculas():
    genero = request.args.get("genero")
    orden = request.args.get("orden", "titulo")
    query = Pelicula.query
    if genero:
        query = query.filter_by(genero=genero)
    if orden == "calificacion":
        peliculas = query.order_by(Pelicula.calificacion.desc()).all()
    else:
        peliculas = query.order_by(Pelicula.titulo).all()
    return jsonify([p.to_dict() for p in peliculas])

@app.route("/peliculas/<int:id>", methods=["GET"])
def get_pelicula(id):
    pelicula = Pelicula.query.get(id)
    if pelicula:
        return jsonify(pelicula.to_dict())
    return jsonify({"error": "No encontrado"}), 404

@app.route("/peliculas", methods=["POST"])
def crear_pelicula():
    data = request.get_json()
    if not data or not all(k in data for k in ["titulo", "genero", "calificacion"]):
        return jsonify({"error": "Campos requeridos"}), 400
    if not (0 <= data["calificacion"] <= 10):
        return jsonify({"error": "Calificación 0-10"}), 400
    if Pelicula.query.filter_by(titulo=data["titulo"]).first():
        return jsonify({"error": "Título duplicado"}), 409
    nueva = Pelicula(titulo=data["titulo"], genero=data["genero"],
                     calificacion=data["calificacion"], director=data.get("director"),
                     anio=data.get("anio"), duracion=data.get("duracion"))
    db.session.add(nueva)
    db.session.commit()
    return jsonify(nueva.to_dict()), 201

@app.route("/peliculas/<int:id>", methods=["PUT"])
def actualizar_pelicula(id):
    pelicula = Pelicula.query.get(id)
    if not pelicula:
        return jsonify({"error": "No encontrado"}), 404
    data = request.get_json()
    if "calificacion" in data and not (0 <= data["calificacion"] <= 10):
        return jsonify({"error": "Calificación 0-10"}), 400
    pelicula.titulo = data.get("titulo", pelicula.titulo)
    pelicula.genero = data.get("genero", pelicula.genero)
    pelicula.calificacion = data.get("calificacion", pelicula.calificacion)
    pelicula.director = data.get("director", pelicula.director)
    pelicula.anio = data.get("anio", pelicula.anio)
    pelicula.duracion = data.get("duracion", pelicula.duracion)
    db.session.commit()
    return jsonify(pelicula.to_dict())

@app.route("/peliculas/<int:id>", methods=["DELETE"])
def eliminar_pelicula(id):
    pelicula = Pelicula.query.get(id)
    if not pelicula:
        return jsonify({"error": "No encontrado"}), 404
    db.session.delete(pelicula)
    db.session.commit()
    return jsonify({"message": "Eliminado"})

@app.route("/peliculas/estadisticas/resumen", methods=["GET"])
def estadisticas():
    total = Pelicula.query.count()
    if total == 0:
        return jsonify({"total": 0, "promedio": 0})
    promedio = db.session.query(db.func.avg(Pelicula.calificacion)).scalar() or 0
    mejor = Pelicula.query.order_by(Pelicula.calificacion.desc()).first()
    peor = Pelicula.query.order_by(Pelicula.calificacion.asc()).first()
    generos = db.session.query(Pelicula.genero, db.func.count(Pelicula.id)).group_by(Pelicula.genero).all()
    return jsonify({"total": total, "promedio": round(promedio, 2),
                    "mejor": mejor.to_dict() if mejor else None,
                    "peor": peor.to_dict() if peor else None,
                    "generos": [{"genero": g[0], "cantidad": g[1]} for g in generos]})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=5000)
