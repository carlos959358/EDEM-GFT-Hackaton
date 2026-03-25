import { Eye, EyeOff } from 'lucide-react';
import { useState } from 'react';
import { useNavigate } from 'react-router';

export function LoginScreen() {
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);
  const navigate = useNavigate();

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    navigate('/dashboard');
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-[#f5f5f5] px-6">
      <div className="w-full max-w-sm">
        {/* Logo */}
        <div className="text-center mb-12">
          <h1 className="text-5xl text-[#008899] mb-2" style={{ fontWeight: 300 }}>EDEM</h1>
          <p className="text-sm text-gray-600">EDEM STUDENT HUB</p>
        </div>

        {/* Form */}
        <form onSubmit={handleLogin} className="space-y-4">
          {/* Email Input */}
          <div>
            <input
              type="email"
              placeholder="Email"
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
            className="w-full bg-[#008899] text-white py-3 rounded-lg mt-6 hover:bg-[#007788] transition-colors"
          >
            Login
          </button>
        </form>
      </div>
    </div>
  );
}
