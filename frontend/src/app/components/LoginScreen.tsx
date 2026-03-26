import { Eye, EyeOff } from 'lucide-react';
import { useState } from 'react';
import { useNavigate } from 'react-router';
import { login } from '../api';

export function LoginScreen() {
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const tokenResponse = await login(email, password);
      localStorage.setItem('authToken', tokenResponse.access_token);
      navigate('/dashboard');
    } catch (err) {
      setError('Email o contraseña incorrectos. Por favor, inténtalo de nuevo.');
      setLoading(false);
    // Mock role detection based on email
    if (email.includes('admin')) {
      localStorage.setItem('userRole', 'admin');
    } else if (email.includes('profesor')) {
      localStorage.setItem('userRole', 'professor');
    } else {
      localStorage.setItem('userRole', 'student');
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-[#f5f5f5] px-6">
      <div className="w-full max-w-sm">
        {/* Logo */}
        <div className="text-center mb-12">
          <h1 className="text-5xl text-[#008899] mb-2" style={{ fontWeight: 300, fontFamily: 'Didot, Bodoni, serif' }}>EDEM</h1>
          <p className="text-sm text-gray-600">EDEM STUDENT HUB</p>
        </div>

        {/* Form */}
        <form onSubmit={handleLogin} className="space-y-4">
          {/* Email Input */}
          <div>
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-3 border-b-2 border-gray-300 bg-transparent focus:outline-none focus:border-[#008899] placeholder:text-gray-400"
            />
          </div>

          {/* Password Input */}
          <div className="relative">
            <input
              type={showPassword ? 'text' : 'password'}
              placeholder="Contraseña"
              className="w-full px-4 py-3 border-b-2 border-gray-300 bg-transparent focus:outline-none focus:border-[#008899] placeholder:text-gray-400 pr-10"
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400"
            >
              {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
            </button>
          </div>

          {/* Error Message */}
          {error && (
            <div className="text-red-600 text-sm text-center py-2">
              {error}
            </div>
          )}
          {/* Remember Me Toggle */}
          <div className="flex items-center justify-between py-2">
            <span className="text-sm text-gray-600">Recordarme</span>
            <button
              type="button"
              onClick={() => setRememberMe(!rememberMe)}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                rememberMe ? 'bg-[#008899]' : 'bg-gray-300'
              }`}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  rememberMe ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          </div>

          {/* Login Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-[#008899] text-white py-3 rounded-lg mt-6 hover:bg-[#007788] transition-colors disabled:bg-gray-400"
          >
            {loading ? 'Iniciando sesión...' : 'Login'}
          </button>
        </form>
      </div>
    </div>
  );
}
