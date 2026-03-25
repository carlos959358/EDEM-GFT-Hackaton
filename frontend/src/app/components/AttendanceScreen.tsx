import { ChevronLeft, CheckCircle, XCircle, Clock, Users } from 'lucide-react';
import { useNavigate } from 'react-router';

interface AttendanceRecord {
  name: string;
  code: string;
  attended: number;
  total: number;
  lastAbsence?: string;
}

const records: AttendanceRecord[] = [
  { name: 'Big Data & Analytics',   code: 'BDA-301', attended: 18, total: 20, lastAbsence: '10 Mar' },
  { name: 'Marketing Digital',      code: 'MKT-201', attended: 17, total: 20, lastAbsence: '17 Mar' },
  { name: 'Finanzas Corporativas',  code: 'FIN-302', attended: 15, total: 15 },
  { name: 'Estrategia Empresarial', code: 'EST-401', attended: 14, total: 18, lastAbsence: '3 Mar'  },
  { name: 'Análisis de Datos',      code: 'ADA-303', attended: 19, total: 20, lastAbsence: '5 Mar'  },
  { name: 'Coaching y Liderazgo',   code: 'COA-201', attended: 14, total: 16, lastAbsence: '20 Mar' },
];

const overallAttended = records.reduce((a, r) => a + r.attended, 0);
const overallTotal    = records.reduce((a, r) => a + r.total, 0);
const overallPct      = Math.round((overallAttended / overallTotal) * 100);

const getStatus = (pct: number) => {
  if (pct >= 90) return { label: 'Excelente',  color: 'text-green-600',  bg: 'bg-green-50',  bar: 'bg-green-500'  };
  if (pct >= 80) return { label: 'Bien',        color: 'text-blue-600',   bg: 'bg-blue-50',   bar: 'bg-blue-500'   };
  if (pct >= 70) return { label: 'Regular',     color: 'text-amber-600',  bg: 'bg-amber-50',  bar: 'bg-amber-500'  };
  return              { label: 'Riesgo',       color: 'text-red-600',    bg: 'bg-red-50',    bar: 'bg-red-500'    };
};

// Mini radial ring via SVG
function RingChart({ pct, size = 56 }: { pct: number; size?: number }) {
  const r = (size - 8) / 2;
  const circ = 2 * Math.PI * r;
  const dash = (pct / 100) * circ;
  const gap  = circ - dash;
  const color = pct >= 90 ? '#22c55e' : pct >= 80 ? '#3b82f6' : pct >= 70 ? '#f59e0b' : '#ef4444';

  return (
    <svg width={size} height={size} className="-rotate-90" style={{ display: 'block' }}>
      <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="#e5e7eb" strokeWidth={6} />
      <circle
        cx={size / 2} cy={size / 2} r={r}
        fill="none"
        stroke={color}
        strokeWidth={6}
        strokeDasharray={`${dash} ${gap}`}
        strokeLinecap="round"
      />
    </svg>
  );
}

export function AttendanceScreen() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-[#008899] pb-20">
      {/* ── Header ── */}
      <div className="px-5 pt-12 pb-6">
        <div className="flex items-center gap-3 mb-6">
          <button onClick={() => navigate(-1)} className="p-1">
            <ChevronLeft className="text-white" size={24} />
          </button>
          <div>
            <h1 className="text-white text-xl" style={{ fontWeight: 300, fontFamily: 'Didot, Bodoni, serif' }}>EDEM</h1>
            <p className="text-white text-xs opacity-80">EDEM STUDENT HUB</p>
          </div>
        </div>

        {/* Global metric */}
        <div className="bg-white/15 rounded-2xl p-4 flex items-center gap-4">
          <div className="relative flex-shrink-0">
            <RingChart pct={overallPct} size={64} />
            <div className="absolute inset-0 flex items-center justify-center">
              <span className="text-white text-xs" style={{ fontWeight: 800 }}>{overallPct}%</span>
            </div>
          </div>
          <div className="flex-1">
            <p className="text-white/70 text-xs mb-0.5">Asistencia Global</p>
            <p className="text-white text-base" style={{ fontWeight: 700 }}>
              {overallAttended}/{overallTotal} clases
            </p>
            <p className="text-white/60 text-xs">Curso 2025–26 · Grado ADE + DATA</p>
          </div>
        </div>

        {/* Quick stats */}
        <div className="grid grid-cols-3 gap-2 mt-3">
          {[
            { icon: CheckCircle, label: 'Asistidas',  value: overallAttended, color: 'text-green-300' },
            { icon: XCircle,     label: 'Faltas',     value: overallTotal - overallAttended, color: 'text-red-300' },
            { icon: Clock,       label: 'Restantes',  value: Math.max(0, Math.round(overallTotal * 0.1)), color: 'text-amber-300' },
          ].map(({ icon: Icon, label, value, color }, i) => (
            <div key={i} className="bg-white/10 rounded-xl py-2 px-3 text-center">
              <Icon size={16} className={`mx-auto mb-0.5 ${color}`} />
              <p className="text-white text-sm" style={{ fontWeight: 700 }}>{value}</p>
              <p className="text-white/60 text-xs">{label}</p>
            </div>
          ))}
        </div>
      </div>

      {/* ── Content ── */}
      <div className="bg-white rounded-t-3xl px-5 pt-5 pb-6 min-h-[60vh]">
        <div className="flex items-center gap-2 mb-5">
          <Users size={18} className="text-[#008899]" />
          <h2 className="text-[#008899]" style={{ fontWeight: 700 }}>ASISTENCIA POR ASIGNATURA</h2>
        </div>

        <div className="space-y-3">
          {records.map((r, i) => {
            const pct    = Math.round((r.attended / r.total) * 100);
            const status = getStatus(pct);
            const absences = r.total - r.attended;

            return (
              <div key={i} className="bg-gray-50 rounded-2xl p-4">
                <div className="flex items-center gap-3 mb-2">
                  {/* Ring */}
                  <div className="relative flex-shrink-0">
                    <RingChart pct={pct} size={44} />
                    <div className="absolute inset-0 flex items-center justify-center">
                      <span className="text-gray-700 text-xs" style={{ fontWeight: 700 }}>{pct}%</span>
                    </div>
                  </div>

                  <div className="flex-1 min-w-0">
                    <p className="text-gray-800 text-sm truncate" style={{ fontWeight: 600 }}>
                      {r.name}
                    </p>
                    <div className="flex items-center gap-2 mt-0.5">
                      <span className="text-xs text-gray-400">{r.code}</span>
                      {r.lastAbsence && (
                        <>
                          <span className="text-xs text-gray-300">·</span>
                          <span className="text-xs text-gray-400">Última falta: {r.lastAbsence}</span>
                        </>
                      )}
                    </div>
                  </div>

                  <span
                    className={`text-xs px-2 py-0.5 rounded-full flex-shrink-0 ${status.bg} ${status.color}`}
                    style={{ fontWeight: 600 }}
                  >
                    {status.label}
                  </span>
                </div>

                <div className="flex justify-between mt-1">
                  <span className="text-xs text-gray-400">
                    {r.attended}/{r.total} clases
                  </span>
                  <span className={`text-xs ${absences > 0 ? 'text-red-400' : 'text-green-500'}`}>
                    {absences === 0 ? '¡Sin faltas!' : `${absences} ${absences === 1 ? 'falta' : 'faltas'}`}
                  </span>
                </div>
              </div>
            );
          })}
        </div>

        {/* Warning banner */}
        {records.some(r => (r.attended / r.total) < 0.80) && (
          <div className="mt-4 bg-amber-50 border border-amber-200 rounded-2xl p-4 flex items-start gap-3">
            <XCircle size={18} className="text-amber-500 flex-shrink-0 mt-0.5" />
            <div>
              <p className="text-amber-700 text-sm" style={{ fontWeight: 600 }}>Atención</p>
              <p className="text-amber-600 text-xs mt-0.5">
                Estrategia Empresarial está por debajo del 80% mínimo requerido. Contacta con tu tutor.
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
