// ==========================================
// API Client — Capa centralizada de conexión con el backend
// ==========================================
// En producción (Cloud Run): VITE_API_URL = "https://backend-xxxxx.run.app"
// En desarrollo local: VITE_API_URL vacío → usa el proxy de Vite (/api/v1/...)

const API_BASE = import.meta.env.VITE_API_URL
  ? `${import.meta.env.VITE_API_URL}/api/v1`
  : '/api/v1';

// ── Helper genérico ──
async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const token = localStorage.getItem('authToken');
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...options?.headers,
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE}${path}`, {
    headers,
    ...options,
  });
  if (!res.ok) {
    throw new Error(`API error ${res.status}: ${res.statusText}`);
  }
  // 204 No Content
  if (res.status === 204) return undefined as unknown as T;
  return res.json();
}

// ==========================================
// AUTENTICACIÓN
// ==========================================
interface TokenResponse {
  access_token: string;
  token_type: string;
}

export async function login(email: string, password: string): Promise<TokenResponse> {
  const params = new URLSearchParams();
  params.append('username', email);
  params.append('password', password);

  const res = await fetch(`${API_BASE}/token`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: params,
  });
  if (!res.ok) throw new Error('Credenciales incorrectas');
  return res.json();
}

// ==========================================
// PERFIL
// ==========================================
export interface UserProfile {
  id: string;
  nombre: string;
  apellido: string;
  correo: string;
  rol: string;
  url_foto: string | null;
}

export function fetchMyProfile(): Promise<UserProfile> {
  return apiFetch<UserProfile>('/users/me');
}

export function updateMyProfile(data: { nombre?: string; apellido?: string; correo?: string }): Promise<unknown> {
  return apiFetch('/users/me', { method: 'PUT', body: JSON.stringify(data) });
}

// ==========================================
// CALENDARIO
// ==========================================
export interface CalendarEvent {
  id: string;
  tipo: string;       // 'class', 'exam', 'delivery'
  titulo: string;
  id_asignatura: string;
  aula: string | null;
  id_profesor: string | null;
  fecha_inicio: string; // ISO datetime
  fecha_fin: string;    // ISO datetime
  descripcion: string | null;
}

export function fetchCalendarEvents(tipo?: string): Promise<CalendarEvent[]> {
  const params = tipo ? `?tipo=${tipo}` : '';
  return apiFetch<CalendarEvent[]>(`/calendar/events${params}`);
}

// ==========================================
// NOTAS
// ==========================================
export interface Grade {
  id_tarea: number;
  nombre_tarea: string;
  id_asignatura: string;
  nota: number;
}

export function fetchMyGrades(): Promise<Grade[]> {
  return apiFetch<Grade[]>('/grades/me');
}

export function fetchMyGradesBySubject(subjectId: string): Promise<Grade[]> {
  return apiFetch<Grade[]>(`/grades/me/subjects/${subjectId}`);
}

// ==========================================
// ASISTENCIA
// ==========================================
export interface AttendanceRecord {
  id_asistencia: number;
  id_alumno: string;
  id_asignatura: string;
  fecha: string;
  presente: boolean;
}

export interface AttendanceMetrics {
  total_clases: number;
  clases_asistidas: number;
  porcentaje_asistencia: number;
}

export function fetchMyAttendance(): Promise<AttendanceRecord[]> {
  return apiFetch<AttendanceRecord[]>('/attendance/me');
}

export function fetchAttendanceMetrics(): Promise<AttendanceMetrics> {
  return apiFetch<AttendanceMetrics>('/attendance/me/metrics');
}

// ==========================================
// NOTIFICACIONES
// ==========================================
export interface Notification {
  id: string;
  tipo: string;
  titulo: string;
  mensaje: string;
  leida: boolean;
  fecha_creacion: string;
}

export function fetchNotifications(): Promise<Notification[]> {
  return apiFetch<Notification[]>('/notifications');
}

export function markNotificationRead(id: string): Promise<Notification> {
  return apiFetch<Notification>(`/notifications/${id}/read`, { method: 'PUT' });
}

// ==========================================
// ASIGNATURAS
// ==========================================
export interface Subject {
  id_asignatura: string;
  nombre: string;
}

export function fetchSubjects(): Promise<Subject[]> {
  return apiFetch<Subject[]>('/subjects');
}

// ==========================================
// CORREOS
// ==========================================
export interface Email {
  id: string;
  id_remitente: string;
  id_destinatario: string;
  asunto: string;
  cuerpo: string;
  leido: boolean;
  fecha_envio: string;
}

export function fetchEmails(folder: 'inbox' | 'sent' = 'inbox'): Promise<Email[]> {
  return apiFetch<Email[]>(`/emails?folder=${folder}`);
}
