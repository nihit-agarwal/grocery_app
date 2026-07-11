import { useContext, useState } from "react"
import type { SubmitEvent } from "react";
import {
    Alert,
    Paper,
    PasswordInput,
    Stack,
    Text,
    TextInput,
    Title,
    Button
} from "@mantine/core";
import { AuthContext } from "./AuthContext"
import { useNavigate } from "react-router-dom";

export default function LoginPage() {

    const { login } = useContext(AuthContext);
    const navigate = useNavigate();

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [submitting, setSubmitting] = useState(false);
    const [error, setError] = useState("");

    async function handleSubmit(e: SubmitEvent<HTMLFormElement>) {
        e.preventDefault()
        setError("");
        setSubmitting(true);

        try {
            await login(username.trim(), password);
            navigate("/households", { replace: true})
        } catch {
            setError("Invalid username or password.")
        } finally {
            setSubmitting(false)
        }
    }

    return (
        <main className="page">
            <Paper radius="xl" shadow="md" p="xl" withBorder maw={480} mx="auto">
                <Stack gap="lg">
                    <div>
                        <Text c="green.7" fw={700} tt="uppercase" size="sm" mb="xs"> 
                            Grocery App
                        </Text>
                        <Title order={1}>
                            Welcome Back
                        </Title>
                        <Text c="dimmed" mt="xs">
                            Sign in to access your household, inventory, and shopping lists.
                        </Text>
                    </div>
        
                    <form onSubmit={handleSubmit}>
                        <Stack gap="md">
                            <TextInput
                            label="Username"
                            value={username}
                            onChange={(e) => setUsername(e.currentTarget.value)}
                            autoComplete="username"
                            required
                            size="md"
                            radius="md"
                            />

                            <PasswordInput
                            label="Password"
                            value={password}
                            onChange={(e) => setPassword(e.currentTarget.value)}
                            autoComplete="current-password"
                            required
                            size="md"
                            radius="md"
                            />

                        
                            {error ? (
                                <Alert color="red" variant="light"  title="Login Failure">
                                    {error}
                                </Alert>
                                ) : null}

                            <Button type="submit" loading={submitting} size="md" radius="xl" fullWidth>
                                {submitting ? "Logging in ..." : "Log in"}
                            </Button>

                        </Stack>

                    </form>
                </Stack>
            </Paper>
            
            
        </main>
    );
}