# ============================================================================
# MODELOS SQLALCHEMY - DEFINICIÓN DE TABLAS
# ============================================================================
# Estos modelos definen la estructura de las tablas en la base de datos.
# SQLAlchemy convierte estas clases en tablas SQL automáticamente.
# ============================================================================

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

# MODELO 1: CLIENTE (Usuario del banco)
# =====================================================
class Cliente(Base):
    """
    Tabla 'clientes' - Información de cada usuario del banco.
    Estructura adaptada a la tabla existente en proyecto_fin_grado.
    """
    
    __tablename__ = "clientes"
    
    # COLUMNAS (coinciden exactamente con la tabla clientes en la BD)
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    apellidos = Column(String(100), nullable=False)
    fecha_nacimiento = Column(DateTime, nullable=False)
    dni = Column(String(20), unique=True, nullable=False, index=True)
    telefono = Column(String(20), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    nacionalidad = Column(String(50), nullable=False)
    direccion = Column(String(150), nullable=False)
    provincia = Column(String(50), nullable=False)
    ciudad = Column(String(50), nullable=False)
    codigo_postal = Column(String(10), nullable=False)
    pais_residencia = Column(String(50), nullable=False)
    situacion_laboral = Column(String(50), nullable=False)
    saldo = Column(Float, default=0.00, nullable=False)
    ultimo_inicio_sesion = Column(DateTime, default=datetime.utcnow, nullable=False)
    password = Column(String(255), nullable=False)
    
    # RELACIÓN CON TRANSACCIONES
    # backreference = permite acceder a las transacciones del cliente directamente
    transacciones_enviadas = relationship(
        "Transaccion",
        foreign_keys="Transaccion.id_emisor",
        back_populates="emisor",
        cascade="all, delete-orphan"  # Si se borra el cliente, se borran sus transacciones
    )
    
    transacciones_recibidas = relationship(
        "Transaccion",
        foreign_keys="Transaccion.id_receptor",
        back_populates="receptor"
    )
    
    def __repr__(self):
        """Representación útil para debugging"""
        return f"<Cliente(id={self.id}, email={self.email}, saldo={self.saldo})>"


# MODELO 2: TRANSACCIÓN (Bizum)
# =====================================================
class Transaccion(Base):
    """
    Tabla 'transacciones' - Historial de todos los movimientos bancarios.
    
    Campos:
    - id: Identificador único de la transacción
    - id_emisor: Cliente que envía dinero (Foreign Key a clientes.id)
    - id_receptor: Cliente que recibe dinero (Foreign Key a clientes.id)
    - cantidad: Dinero transferido (siempre positivo)
    - concepto: Motivo de la transferencia (p.ej. "Pago de cena")
    - fecha: Cuándo se hizo la transacción
    """
    
    __tablename__ = "transacciones"
    
    # COLUMNAS
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_emisor = Column(Integer, ForeignKey("clientes.id"), nullable=False)  # Foreign Key = referencia a clientes.id
    id_receptor = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    cantidad = Column(Float, nullable=False)
    concepto = Column(String(255), nullable=True)  # Opcional: "Bizum para café"
    fecha = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # RELACIONES (para acceder fácilmente a los datos del emisor/receptor)
    emisor = relationship(
        "Cliente",
        foreign_keys=[id_emisor],
        back_populates="transacciones_enviadas"
    )
    
    receptor = relationship(
        "Cliente",
        foreign_keys=[id_receptor],
        back_populates="transacciones_recibidas"
    )
    
    def __repr__(self):
        """Representación útil para debugging"""
        return f"<Transaccion(id={self.id}, emisor={self.id_emisor}, receptor={self.id_receptor}, cantidad={self.cantidad})>"
