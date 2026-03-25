import { ChevronLeft, TrendingUp, Award, BookOpen } from 'lucide-react';
import { useNavigate } from 'react-router';

interface Subject {
  name: string;
  code: string;
  grade: number;
  credits: number;
  period: string;
}

const subjects: Subject[] = [
  { name: 'Big Data & Analytics',    code: 'BDA-301', grade: 8.5, credits: 6, period: 'Q1' },
  { name: 'Marketing Digital',       code: 'MKT-201', grade: 7.2, credits: 5, period: 'Q1' },
  { name: 'Finanzas Corporativas',   code: 'FIN-302', grade: 9.0, credits: 6, period: 'Q1' },
  { name: 'Estrategia Empresarial',  code: 'EST-401', grade: 6.8, credits: 5, period: 'Q2' },
  { name: 'Análisis de Datos',       code: 'ADA-303', grade: 8.0, credits: 6, period: 'Q2' },
  { name: 'Coaching y Liderazgo',    code: 'COA-201', grade: 7.5, credits: 4, period: 'Q2' },
];

const average = subjects.reduce((acc, s) => acc + s.grade, 0) / subjects.length;

const getGradeLabel = (g: number) => {
  if (g >= 9)    return { label: 'Sobresaliente', color: 'text-purple-600', bg: 'bg-purple-50' };
  if (g >= 7)    return { label: 'Notable',       color: 'text-blue-600',   bg: 'bg-blue-50'   };
  if (g >= 6)    return { label: 'Bien',           color: 'text-green-600',  bg: 'bg-green-50'  };
  if (g >= 5)    return { label: 'Aprobado',       color: 'text-amber-600',  bg: 'bg-amber-50'  };
  return              { label: 'Suspenso',        color: 'text-red-600',    bg: 'bg-red-50'    };
};

const getBarColor = (g: number) => {
  if (g >= 9)  return 'bg-purple-500';
  if (g >= 7)  return 'bg-blue-500';
  if (g >= 6)  return 'bg-green-500';
  if (g >= 5)  return 'bg-amber-500';
  return 'bg-red-500';
};

export function GradesScreen() {
  const navigate = useNavigate();
  const { label: avgLabel, color: avgColor, bg: avgBg } = getGradeLabel(average);

  return (
    <div className="min-h-screen bg-[#008899] pb-20">
      {/* ── Header ── */}
      <div className="px-5 pt-12 pb-6">
        <div className="flex items-center gap-3 mb-6">
          <button onClick={() => navigate(-1)} className="p-1">
            <ChevronLeft className="text-white" size={24} />
          </button>
          <div>
            <h1 className="text-white text-xl" style={{ fontWeight: 300 }}>EDEM</h1>
            <p className="text-white text-xs opacity-80">EDEM STUDENT HUB</p>
          </div>
        </div>

        {/* Average summary */}
        <div className="bg-white/15 rounded-2xl p-4 flex items-center gap-4">
          <div className="w-14 h-14 rounded-2xl bg-white flex items-center justify-center shadow">
            <span className="text-[#008899] text-xl" style={{ fontWeight: 800 }}>
              {average.toFixed(1)}
            </span>
          </div>
          <div>
            <p className="text-white/70 text-xs mb-0.5">Nota Media Global</p>
            <p className="text-white text-base" style={{ fontWeight: 700 }}>{avgLabel}</p>
            <p className="text-white/60 text-xs">{subjects.length} asignaturas · Curso 2025–26</p>
          </div>
          <TrendingUp className="text-white/60 ml-auto" size={28} />
        </div>
      </div>

      {/* ── Content ── */}
      <div className="bg-white rounded-t-3xl px-5 pt-5 pb-6 min-h-[70vh]">
        <div className="flex items-center gap-2 mb-5">
          <BookOpen size={18} className="text-[#008899]" />
          <h2 className="text-[#008899]" style={{ fontWeight: 700 }}>MIS NOTAS</h2>
        </div>

        {/* Subjects list */}
        <div className="space-y-3">
          {subjects.map((subject, i) => {
            const { label, color, bg } = getGradeLabel(subject.grade);
            const barColor = getBarColor(subject.grade);
            const pct = (subject.grade / 10) * 100;

            return (
              <div key={i} className="bg-gray-50 rounded-2xl p-4">
                <div className="flex items-start justify-between mb-2">
                  <div className="flex-1 min-w-0 mr-3">
                    <p className="text-gray-800 text-sm truncate" style={{ fontWeight: 600 }}>
                      {subject.name}
                    </p>
                    <div className="flex items-center gap-2 mt-0.5">
                      <span className="text-xs text-gray-400">{subject.code}</span>
                      <span className="text-xs text-gray-300">·</span>
                      <span className="text-xs text-gray-400">{subject.credits} ECTS</span>
                      <span className="text-xs text-gray-300">·</span>
                      <span className="text-xs text-gray-400">{subject.period}</span>
                    </div>
                  </div>
                  <div className="text-right flex-shrink-0">
                    <p className="text-gray-800 text-lg" style={{ fontWeight: 800 }}>
                      {subject.grade.toFixed(1)}
                    </p>
                    <span className={`text-xs px-2 py-0.5 rounded-full ${bg} ${color}`} style={{ fontWeight: 600 }}>
                      {label}
                    </span>
                  </div>
                </div>

                {/* Grade bar */}
                <div className="h-1.5 bg-gray-200 rounded-full overflow-hidden">
                  <div
                    className={`h-full rounded-full transition-all ${barColor}`}
                    style={{ width: `${pct}%` }}
                  />
                </div>
              </div>
            );
          })}
        </div>

        {/* Stats row */}
        <div className="grid grid-cols-3 gap-3 mt-5">
          {[
            { icon: Award,    label: 'Mejor nota',  value: '9.0', sub: 'Finanzas' },
            { icon: TrendingUp, label: 'Media',     value: average.toFixed(2), sub: 'Global' },
            { icon: BookOpen, label: 'ECTS',        value: subjects.reduce((a, s) => a + s.credits, 0).toString(), sub: 'Créditos' },
          ].map(({ icon: Icon, label, value, sub }, i) => (
            <div key={i} className="bg-[#008899]/5 rounded-2xl p-3 text-center">
              <Icon size={18} className="text-[#008899] mx-auto mb-1" />
              <p className="text-[#008899] text-base" style={{ fontWeight: 800 }}>{value}</p>
              <p className="text-gray-500 text-xs">{label}</p>
              <p className="text-gray-400 text-xs">{sub}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
