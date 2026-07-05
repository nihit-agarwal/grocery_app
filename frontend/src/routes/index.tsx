import {Routes, Route, Navigate} from "react-router-dom";
import { useContext } from "react";
import type { JSX } from "react/jsx-runtime";
import LoginPage from "../features/auth/LoginPage";
import HouseholdListPage from "../features/households/HouseholdListPage";
import SignupPage from "../features/auth/SignupPage";
import { AuthContext } from "../features/auth/AuthContext";



function HomeRedirect() {
    const { isAuthenticated, loading } = useContext(AuthContext);
    if (loading) return <div>Loading ...</div>;
    return isAuthenticated ? (
        <Navigate to="/households" replace />
    ) : (
        <Navigate to="/login" replace />
    )
}

function RequireAuth({children} : {children: JSX.Element}) {
    const { isAuthenticated, loading } = useContext(AuthContext);
    if (loading) return <div>Loading ...</div>;
    return isAuthenticated ? children : <Navigate to="/login" replace />

}

function RedirectIfAuth({children} : {children: JSX.Element}) {
    const { isAuthenticated, loading } = useContext(AuthContext);
    if (loading) return <div>Loading ...</div>;
    return isAuthenticated ? <Navigate to="/households" replace/> : children;
    

}
export function AppRoutes() {
    return (
        <Routes>
            
            <Route path="/" element={<HomeRedirect />} />

            <Route path="/login"
            element={
                <RedirectIfAuth>
                    <LoginPage />
                </RedirectIfAuth>
            } />

            <Route path="/signup"
            element={
                <RedirectIfAuth>
                    <SignupPage />
                </RedirectIfAuth>
            } />

            <Route path="/households"
            element={
                <RequireAuth>
                    <HouseholdListPage />
                </RequireAuth>
            } />


            <Route path="*"
            element={
                <Navigate to="/" replace />
            } />





        </Routes>
    )
}