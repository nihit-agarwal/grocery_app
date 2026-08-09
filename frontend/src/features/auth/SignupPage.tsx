import {
    Alert,
    Paper,
    PasswordInput,
    Stack,
    Text,
    TextInput,
    Title,
    Button,
    useRandomClassName
} from "@mantine/core";import { useContext, useState } from "react";
import type { SubmitEvent } from "react";
import { AuthContext } from "./AuthContext"
import { useNavigate } from "react-router-dom";

export default function SignupPage() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [repPassword, setRepPassword] = useState("");
    const [error, setError] = useState("");
    const [submitting, setSubmitting] = useState<boolean>(false);
    const { signup } = useContext(AuthContext);
    const navigate = useNavigate();

    async function handleSubmit(e: SubmitEvent<HTMLFormElement>) {
        e.preventDefault();
        if (password !== repPassword) {
            setError("Passwords do not match !");
            return;
        }
        setSubmitting(true);
        try {
            await signup(username.trim(), password);
            navigate("/households", { replace: true});
        } catch (err: any) {
            const detail = err?.response?.data?.detail;
            if (Array.isArray(detail)) {
                setError(detail.join(" "));
            } else if (typeof detail === "string") {
                setError(detail);
            } else {
                setError("Signup failed.");
            }
        } finally {
            setSubmitting(false);
        }
    }
    return(
        <main className="page">
            <Paper radius="xl" shadow="md" p="xl" withBorder maw={480} mx="auto">
                <Stack gap="lg">
                    <div>
                        <Text c="green.7" fw={700} tt="uppercase" size="sm" mb="xs"> 
                            Grocery App
                        </Text>
                        <Title order={1}>
                            Sign Up
                        </Title>
                        <Text c="dimmed" mt="xs">
                            Sign up to start solving your inventory issues.
                        </Text>
                    </div>

                    <form onSubmit={handleSubmit}>
                        <Stack gap="md">
                            <TextInput
                            label="Username"
                            size="md"
                            radius="md"
                            value={username}
                            onChange={(e) => setUsername(e.currentTarget.value)}
                            required
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
                            <PasswordInput
                                label="Repeat Password"
                                value={repPassword}
                                onChange={(e) => setRepPassword(e.currentTarget.value)}
                                autoComplete="repeat-password"
                                required
                                size="md"
                                radius="md"
                            />

                            {error ? (
                                <Alert color="red" variant="light"  title="Singup Failure">
                                    {error}
                                </Alert>
                            ) : null}

                            <Button type="submit" loading={submitting} size="md" radius="xl" >
                                {submitting ? "Singing Up ... " : "Sign Up"}
                            </Button>

                        </Stack>
                        


                    </form>
                </Stack>
            </Paper>
        </main>

    ) 
}