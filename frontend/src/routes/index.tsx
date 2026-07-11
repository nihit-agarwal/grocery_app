import {Routes, Route, Navigate} from "react-router-dom";
import { useContext } from "react";
import type { JSX } from "react/jsx-runtime";
import LoginPage from "../features/auth/LoginPage";
import HouseholdListPage from "../features/households/HouseholdListPage";
import HouseholdCreatePage from "../features/households/HouseholdCreatePage";
import HouseholdDetailPage from "../features/households/HouseholdDetailPage";
import SignupPage from "../features/auth/SignupPage";
import  CatalogPage  from "../features/catalog/CatalogPage";
import  ItemCreatePage  from "../features/catalog/ItemCreatePage";
import  InventoryPage  from "../features/inventory/InventoryPage";
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

            <Route path="/households/create"
            element={
                <RequireAuth>
                    <HouseholdCreatePage />
                </RequireAuth>
            } />

            <Route path="/households/:householdid"
            element={
                <RequireAuth>
                    <HouseholdDetailPage />
                </RequireAuth>
            } />

            <Route path="/households/:householdid/catalog"
            element={
                <RequireAuth>
                    <CatalogPage />
                </RequireAuth>
            } />

            <Route path="/households/:householdid/catalog/create"
            element={
                <RequireAuth>
                    <ItemCreatePage />
                </RequireAuth>

            } />

            <Route path="/household/:householdid/inventory"
            element={
                <RequireAuth>
                    <InventoryPage />
                </RequireAuth>
            } />





            <Route path="*"
            element={
                <Navigate to="/" replace />
            } />





        </Routes>
    )
}