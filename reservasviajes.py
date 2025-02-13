from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
import jwt
import bcrypt
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List
from pydantic import BaseModel, EmailStr
import re

# Configuración de la base de datos
DATABASE_URL = "sqlite:///./reservas.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Configuración JWT
SECRET_KEY = "secret"
ALGORITHM = "HS256"

# Modelos de base de datos con roles
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String, default="user")  # Nuevo campo de roles (user, admin)

class Trip(Base):
    __tablename__ = "trips"
    id = Column(Integer, primary_key=True, index=True)
    destination = Column(String)
    price = Column(Float)
    date = Column(String)
    available = Column(Boolean, default=True)

class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    trip_id = Column(Integer, ForeignKey("trips.id"))
    status = Column(String, default="Confirmed")
    user = relationship("User")
    trip = relationship("Trip")
    refund_issued = Column(Boolean, default=False)  # Nuevo campo para reembolsos

# Modelos Pydantic
class TripResponse(BaseModel):
    id: int
    destination: str
    price: float
    date: str
    available: bool
    class Config:
        from_attributes = True

class PaymentDetails(BaseModel):
    card_number: str
    cvv: str
    expiration_date: str

# Creación de las tablas
Base.metadata.create_all(bind=engine)

# Dependencia de sesión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Instancia de FastAPI
app = FastAPI()

# Funciones de seguridad y autenticación
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Endpoint de autenticación con roles
@app.post("/register/")
def register(username: str, email: EmailStr, password: str, role: str = "user", db: Session = Depends(get_db)):
    hashed_pw = hash_password(password)
    user = User(username=username, email=email, password=hashed_pw, role=role)
    db.add(user)
    db.commit()
    return {"message": "User registered successfully"}

@app.post("/login/")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_token({"user_id": user.id, "role": user.role})
    return {"access_token": token}

# Validación de entrada en búsqueda de viajes
@app.get("/trips/", response_model=List[TripResponse])
def get_trips(db: Session = Depends(get_db)):
    return db.query(Trip).filter(Trip.available == True).all()

# Endpoint de reserva con validación de pago
@app.post("/reserve/")
def reserve_trip(user_id: int, trip_id: int, payment: PaymentDetails, db: Session = Depends(get_db)):
    if not re.match(r'^[0-9]{16}$', payment.card_number):
        raise HTTPException(status_code=400, detail="Invalid card number")
    trip = db.query(Trip).filter(Trip.id == trip_id, Trip.available == True).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not available")
    reservation = Reservation(user_id=user_id, trip_id=trip_id)
    db.add(reservation)
    db.commit()
    send_notification(user_id, trip.destination, "confirmed")
    return {"message": "Trip reserved successfully"}

# Endpoint de cancelación con política de reembolso
@app.post("/cancel/")
def cancel_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    if reservation.status == "Cancelled":
        raise HTTPException(status_code=400, detail="Reservation already cancelled")
    reservation.status = "Cancelled"
    reservation.refund_issued = True  # Marca reembolso emitido
    db.commit()
    send_notification(reservation.user_id, reservation.trip.destination, "cancelled")
    return {"message": "Reservation cancelled with refund issued"}

# Envío de correos electrónicos
def send_notification(user_email: str, destination: str, status: str):
    sender_email = "your_email@example.com"
    password = "your_password"
    msg = MIMEText(f"Your trip to {destination} has been {status}.")
    msg['Subject'] = "Reservation Update"
    msg['From'] = sender_email
    msg['To'] = user_email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, user_email, msg.as_string())
