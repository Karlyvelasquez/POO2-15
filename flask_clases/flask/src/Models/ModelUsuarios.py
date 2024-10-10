from sqlalchemy import text
from .entities.Usuarios import usuarios


class modeluser:



    @classmethod
    def registrar(cls, db, usuario):
        try:
            consulta = text("SELECT registrar_usuario(:p_cedula, :p_nombre, :p_email, :p_contraseña)")
            db.session.execute(consulta, {
                "p_cedula": usuario.cedula,
                "p_nombre": usuario.nombre,
                "p_email": usuario.email,
                "p_contraseña": usuario.contraseña
            })
            db.session.commit()
            return True
        except Exception as ex:
            raise Exception(ex)

    
    @classmethod
    def login(cls, db, usuario):
        try:
            consulta = text("SELECT * FROM login_usuario(:p_email, :p_contraseña)")
            result = db.session.execute(consulta, {"p_email": usuario.email, "p_contraseña": usuario.contraseña}).fetchone()
            if result:
                return usuarios(result[0], result[1], result[2], result[3])
            return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def actualizar(cls, db, usuario):
        try:
            consulta = text("CALL actualizar_usuario(:cedula, :nombre, :email)")
            db.session.execute(consulta, {
                "cedula": usuario.cedula,
                "nombre": usuario.nombre,
                "email": usuario.email
            })
            db.session.commit()
            return True
        except Exception as ex:
            db.session.rollback() 
            raise Exception(ex)

    @classmethod
    def cambiar_contraseña(cls, db, cedula, nueva_contraseña):
        try:
            consulta = text("CALL cambiar_contraseña_usuario(:cedula, :nueva_contraseña)")
            db.session.execute(consulta, {"cedula": cedula, "nueva_contraseña": nueva_contraseña})
            db.session.commit()
            return True
        except Exception as ex:
            db.session.rollback()  
            raise Exception(ex)
        
    @staticmethod
    def buscar_usuario_por_cedula(db, cedula):
        usuario = db.session.query(usuarios).filter(usuarios.cedula == cedula).first()
        return usuario
