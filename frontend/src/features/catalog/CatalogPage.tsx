import { useEffect, useState } from "react";
import { http } from "../../services/http";
import { replace, useNavigate, useParams } from "react-router-dom";
import { Paper, Stack, Title, Text, Group, Loader, Alert, Card, Button, ActionIcon } from "@mantine/core";
import { IconArrowLeft } from "@tabler/icons-react";


export type catalogItem = {
    item_id: string,
    item_name: string;
    item_type: string;
    created_at: string;
    updated_at: string;
};

export type itemListResponse = {
    items: catalogItem[];
};

export default function CatalogPage() {
    const { householdid } = useParams();
    const [error, setError] = useState("");
    const [items, setItems] = useState<catalogItem[]>([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    // Retreive items from catalog for display
    useEffect(() => {
        async function loadCatalog() {
            try {
                setError("");
                const response = await http.get<itemListResponse>("/households/" + householdid + "/catalog/all");
                setItems(response.data.items);
            } catch {
                setError("Could not load your catalog right now")
            } finally {
                setLoading(false);
            }
        }
        loadCatalog();
    }, [])

    // Add button to create new item
    async function createItem() {
        try {
            setError("")
            navigate("/households/" + householdid + "/catalog/create")
        } catch {
            setError("Could not load create new item page")
        }
    }
    // Add button to delete an item
    return (
        <main className="page">
            <Paper withBorder shadow="md" radius="xl" p="xl" maw={760} mx="auto">
                <Stack gap="lg">
                    <Group justify="space-between" align="center">
                        <ActionIcon
                        variant="light"
                        color="gray"
                        radius="xl"
                        aria-label="Back to household"
                        onClick={() => navigate(`/households/${householdid}`, {replace: true})}
                        >
                            <IconArrowLeft size={18} />
                        </ActionIcon>
                    </Group>
                    <div>
                        <Text c="green.7" fw={700} tt="uppercase" size="sm">
                            Grocery App
                        </Text>
                        <Title order={1}> Catalog </Title>
                        <Text c="dimmed">
                            Select an item for more details.
                        </Text>
                    </div>

                    {loading ? (
                        <Group>
                            <Loader size="sm"/>
                            <Text c="dimmed">Loading items...</Text>
                        </Group>
                    ): null}

                    {error ? (
                        <Alert color="red" title="Could not load catalog">
                            {error}
                        </Alert>
                    ): null}

                    {!loading && !error && items.length === 0 ? (
                        <Card withBorder radius="lg" p="lg">
                            <Text c="dimmed" mt={4}>
                                Create an item to start making cart, updating inventory.
                            </Text>
                        </Card>
                    ): null}

                    <Stack gap="sm">
                        {items.map((item) => 
                        <Card
                        key={item.item_name}
                        withBorder
                        radius="lg"
                        p="md"
                        >
                            <Group justify="space-between" align="center">
                                <div>
                                    <Text fw={700}>{item.item_name}</Text>
                                    <Text size="sm" c="dimmed">
                                        {item.item_type}
                                    </Text>
                                </div>
                            </Group>


                        </Card>)}
                    </Stack>

                    <Button 
                    fullWidth
                    radius="xl"
                    variant="filled"
                    color="green"
                    onClick={createItem}>
                        Create new item
                    </Button>
                </Stack>
            </Paper>
        </main>
    )
}