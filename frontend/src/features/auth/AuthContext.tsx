import { createContext, useState, useEffect, useCallback } from "react";
import type {ReactNode} from "react";
import { http } from "../../services/http";

type AuthContextType = {
  isAuthenticated: boolean | null;
  loading: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  refreshAuth: () => Promise<void>;
};

export const AuthContext = createContext<AuthContextType>({
  isAuthenticated: null,
  loading: true,
  login: async () => {},
  logout: async() => {},
  refreshAuth: async() => {},
});

export function AuthProvider({ children }: { children: ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);
  const [loading, setLoading] = useState(true);

  const refreshAuth = useCallback(async () => {
    try {
      await http.get("/auth/session");
      setIsAuthenticated(true);
    } catch {
      setIsAuthenticated(false);
    }
  }, []);

  const login = useCallback(async (username: string, password: string) => {
    await http.get("/auth/csrf");
    await http.post("/auth/login", { username, password});
    setIsAuthenticated(true);
  }, []);

  const logout = useCallback(async () => {
    await http.post("/auth/logout");
    setIsAuthenticated(false);
  }, [])





  useEffect(() => {
    refreshAuth().finally(() => setLoading(false));
  }, []);

  return (
    <AuthContext.Provider value={{ isAuthenticated, loading, login, logout, refreshAuth }}>
      {children}
    </AuthContext.Provider>
  );
}