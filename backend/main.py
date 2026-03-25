from fastapi import FastAPI

app = FastAPI(
    title="API Universidad EDEM",
    description="API completa para gestión académica, calendario, notas, asistencia y reservas.",
    version="1.0.0"
)

# ==========================================
# 0. ENDPOINT DE ESTADO (Para Google Cloud)
# ==========================================
@app.get("/health", tags=["Sistema"])
def health_check():
    """Endpoint vital para que GCP (Cloud Run/App Engine) sepa que la API está viva."""
    return {"status": "ok", "message": "API funcionando correctamente en GCP"}

# ==========================================
# 1. PERFIL Y ROL (Datos de Usuario)
# ==========================================
@app.get("/api/v1/users/me", tags=["Perfil y Roles"])
def get_my_profile():
    return {"mensaje": "Obtener perfil propio (Nombre, Grado, Contacto, LinkedIn)"}

@app.put("/api/v1/users/me", tags=["Perfil y Roles"])
def update_profile():
    return {"mensaje": "Actualizar datos del perfil"}

@app.put("/api/v1/users/me/photo", tags=["Perfil y Roles"])
def upload_profile_photo():
    return {"mensaje": "Subir foto de perfil (se conectaría con Google Cloud Storage)"}

@app.get("/api/v1/users/{user_id}", tags=["Perfil y Roles"])
def get_user_profile(user_id: str):
    return {"mensaje": f"Ver perfil público del usuario {user_id}"}

# ==========================================
# 2. CALENDARIO
# ==========================================
@app.get("/api/v1/calendar/events", tags=["Calendario"])
def list_events(type: str = None):
    return {"mensaje": f"Listar eventos. Filtro aplicado: {type}"}

@app.post("/api/v1/calendar/events", tags=["Calendario"])
def create_event():
    return {"mensaje": "Crear evento (Asignatura, Aula, Profe, Horario)"}

@app.get("/api/v1/calendar/events/{event_id}", tags=["Calendario"])
def get_event_detail(event_id: str):
    return {"mensaje": f"Detalle del evento {event_id}"}

@app.put("/api/v1/calendar/events/{event_id}", tags=["Calendario"])
def update_event(event_id: str):
    return {"mensaje": f"Actualizar evento {event_id}"}

@app.delete("/api/v1/calendar/events/{event_id}", tags=["Calendario"])
def delete_event(event_id: str):
    return {"mensaje": f"Eliminar evento {event_id}"}

# ==========================================
# 3. ASIGNATURAS
# ==========================================
@app.get("/api/v1/subjects", tags=["Asignaturas"])
def list_subjects():
    return {"mensaje": "Listar todas las asignaturas"}

@app.get("/api/v1/subjects/{subject_id}", tags=["Asignaturas"])
def get_subject_detail(subject_id: str):
    return {"mensaje": f"Detalle de la asignatura {subject_id}"}

@app.get("/api/v1/subjects/{subject_id}/students", tags=["Asignaturas"])
def get_enrolled_students(subject_id: str):
    return {"mensaje": f"Listar alumnos matriculados en la asignatura {subject_id}"}

# ==========================================
# 4. NOTAS
# ==========================================
@app.get("/api/v1/grades/me", tags=["Notas"])
def get_my_grades():
    return {"mensaje": "Obtener todas mis notas"}

@app.get("/api/v1/grades/me/subjects/{subject_id}", tags=["Notas"])
def get_my_grades_by_subject(subject_id: str):
    return {"mensaje": f"Mis notas de la asignatura {subject_id}"}

@app.post("/api/v1/grades", tags=["Notas"])
def register_grade():
    return {"mensaje": "Registrar una nueva nota (Profe)"}

@app.put("/api/v1/grades/{grade_id}", tags=["Notas"])
def update_grade(grade_id: str):
    return {"mensaje": f"Actualizar nota {grade_id}"}

# ==========================================
# 5. ASISTENCIA
# ==========================================
@app.get("/api/v1/attendance/me", tags=["Asistencia"])
def get_my_attendance():
    return {"mensaje": "Mi historial de asistencia"}

@app.get("/api/v1/attendance/me/metrics", tags=["Asistencia"])
def get_attendance_metrics():
    return {"mensaje": "Obtener % de asistencia por asignatura"}

@app.post("/api/v1/attendance", tags=["Asistencia"])
def mark_attendance():
    return {"mensaje": "Registrar sesión de asistencia"}

@app.get("/api/v1/attendance/subjects/{subject_id}", tags=["Asistencia"])
def get_class_attendance(subject_id: str):
    return {"mensaje": f"Ver asistencia de la clase {subject_id}"}

# ==========================================
# 6. RESERVAS Y TUTORÍAS
# ==========================================
@app.get("/api/v1/reservations", tags=["Reservas y Tutorías"])
def list_my_reservations():
    return {"mensaje": "Ver mis reservas"}

@app.post("/api/v1/reservations", tags=["Reservas y Tutorías"])
def request_tutoring():
    return {"mensaje": "Solicitar una reserva/tutoría"}

@app.put("/api/v1/reservations/{reservation_id}", tags=["Reservas y Tutorías"])
def update_reservation(reservation_id: str):
    return {"mensaje": f"Confirmar/Rechazar reserva {reservation_id} (Profe)"}

@app.get("/api/v1/tutorings/slots", tags=["Reservas y Tutorías"])
def get_tutoring_slots(teacher_id: str = None):
    return {"mensaje": f"Ver franjas de disponibilidad. Profe: {teacher_id}"}

@app.post("/api/v1/tutorings/slots", tags=["Reservas y Tutorías"])
def create_tutoring_slot():
    return {"mensaje": "Crear nueva franja de disponibilidad (Profe)"}

# ==========================================
# 7. NOTIFICACIONES
# ==========================================
@app.get("/api/v1/notifications", tags=["Notificaciones"])
def get_notifications(read: bool = None):
    return {"mensaje": f"Listar mis notificaciones. Leídas={read}"}

@app.put("/api/v1/notifications/{notis_id}/read", tags=["Notificaciones"])
def mark_noti_as_read(notis_id: str):
    return {"mensaje": f"Marcar notificación {notis_id} como leída"}

@app.get("/api/v1/notifications/settings", tags=["Notificaciones"])
def get_notification_settings():
    return {"mensaje": "Ver mis preferencias de avisos (15min, 1 semana, etc.)"}

# ==========================================
# 8. CORREOS INTERNOS
# ==========================================
@app.get("/api/v1/emails", tags=["Correos"])
def list_emails(folder: str = "inbox"):
    return {"mensaje": f"Listar bandeja de correos: {folder}"}

@app.post("/api/v1/emails", tags=["Correos"])
def send_email():
    return {"mensaje": "Enviar correo interno"}

@app.get("/api/v1/emails/{email_id}", tags=["Correos"])
def read_email(email_id: str):
    return {"mensaje": f"Leer correo {email_id}"}