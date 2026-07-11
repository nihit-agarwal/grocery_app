import { Paper, Stack, Text, Title, TextInput, Button, Alert, Select } from "@mantine/core";
import type { SubmitEvent } from "react";
import { useState } from "react";
import { http } from "../../services/http";
import { useNavigate, useParams } from "react-router-dom";

export default function ItemCreatePage() {
    const [error, setError] = useState("");
    const [itemName, setItemName] = useState("");
    const [itemType, setItemType] = useState("miscellaneous");

    const [submitting, setSubmitting] = useState(false);
    const navigate = useNavigate();
    const { householdid } = useParams();
    async function handleSubmit(e: SubmitEvent<HTMLFormElement>) {
        e.preventDefault();
        setError("")
        setSubmitting(true);

        try {
            await http.post(`/households/${householdid}/catalog`, {"item_name": itemName, "item_type": itemType});
            navigate(`/households/${householdid}/catalog`, { replace: true})
        } catch {
            setError("Invalid house name.");
        } finally {
            setSubmitting(false);
        }
    }

    async function cancelCreation() {
        navigate(`/households/${householdid}/catalog`, {replace:true})

    }
    return (
        <main className="page">
            <Paper withBorder shadow="md" radius="xl" p="xl" maw={760} mx="auto">
                <Stack gap="lg">
                    <div>
                        <Text c="green.7" fw={700} tt="uppercase" size="sm">
                            Grocery App
                        </Text>
                        <Title order={1}> Create an Item</Title>
                        <Text c="dimmed">
                            Enter details to create a new item in catalog.
                        </Text>
                    </div>
                    <form onSubmit={handleSubmit}>
                        <Stack gap="lg">

                            <TextInput
                            label="Item Name"
                            value={itemName}
                            onChange={(e) => setItemName(e.currentTarget.value)}
                            autoComplete="Item Name"
                            required
                            size="md"
                            radius="md"
                            />

                            <Select
                            label="Item Type"
                            data={[
                                { value: "frozen", label: "Frozen" },
                                { value: "dairy", label: "Dairy" },
                                { value: "pulses", label: "Pulses" },
                                { value: "miscellaneous", label: "Miscellaneous" },
                            ]}
                            value={itemType}
                            onChange={(value) => setItemType(value ?? "miscellaneous")}
                            allowDeselect={false}
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