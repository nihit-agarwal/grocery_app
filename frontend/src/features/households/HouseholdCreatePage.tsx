import { Paper, Stack, Text, Title, TextInput, Button, Alert } from "@mantine/core";
import type { SubmitEvent } from "react";
import { useState } from "react";
import { http } from "../../services/http";
import { Navigate, replace, useNavigate } from "react-router-dom";

export default function HouseholdCreatePage() {
    const [error, setError] = useState("");
    const [houseName, setHouseName] = useState("");
    const [submitting, setSubmitting] = useState(false);
    const navigate = useNavigate();
    async function handleSubmit(e: SubmitEvent<HTMLFormElement>) {
        e.preventDefault();
        setError("")
        setSubmitting(true);

        try {
            await http.post("/households", {"house_name": houseName});
            navigate("/households", { replace: true})
        } catch {
            setError("Invalid house name.");
        } finally {
            setSubmitting(false);
        }
    }

    async function cancelCreation() {
        navigate("/households", {replace:true})

    }
    return (
        <main className="page">
            <Paper withBorder shadow="md" radius="xl" p="xl" maw={760} mx="auto">
                <Stack gap="lg">
                    <div>
                        <Text c="green.7" fw={700} tt="uppercase" size="sm">
                            Grocery App
                        </Text>
                        <Title order={1}> Create a Household</Title>
                        <Text c="dimmed">
                            Enter details to create a new household.
                        </Text>
                    </div>
                    <form onSubmit={handleSubmit}>
                        <Stack gap="lg">

                            <TextInput
                            label="House Name"
                            value={houseName}
                            onChange={(e) => setHouseName(e.currentTarget.value)}
                            autoComplete="House Name"
                            required
                            size="md"
                            radius="md"
                            />
                            
                            {error ? (
                            <Alert color="red" variant="light"  title="Failed to create household">
                                {error}
                            </Alert>
                            ) : null}

                            <Stack gap="md" justify="flex-end" style={{ flexDirection: "row" }}>
                                <Button onClick={cancelCreation} size="sm" radius="md" color="red">Cancel</Button>
                                <Button type="submit" loading={submitting} size="sm" radius="md">
                                    {submitting ? "Creating": "Create"}
                                </Button>
                            </Stack>

                        </Stack> 

                    </form>



                </Stack>
            </Paper>
        </main>
    )
}